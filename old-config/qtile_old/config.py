import os
import subprocess

# from qtile_extras.widget import StatusNotifier
import colors
from libqtile import bar, extension, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
from libqtile.widget.battery import Battery, BatteryState

# Make sure 'qtile-extras' is installed or this config will not work.
from qtile_extras import widget
from qtile_extras.widget.decorations import (
    BorderDecoration,
    PowerLineDecoration,
    RectDecoration,
)

mod = "mod4"  # Sets mod key to SUPER/WINDOWS
myTerm = "alacritty"  # default terminal
myBrowser = "firefox"  # default browser
# myEmacs = "emacsclient -c -a 'emacs' # The space at the end is IMPORTANT!


# Allows you to input a name when adding treetab section.
@lazy.layout.function
def add_treetab_section(layout):
    prompt = qtile.widgets_map["prompt"]
    prompt.start_input("Section name: ", layout.cmd_add_section)


# A function for hide/show all the windows in a group
@lazy.function
def minimize_all(qtile):
    for win in qtile.current_group.windows:
        if hasattr(win, "toggle_minimize"):
            win.toggle_minimize()


# A function for toggling between MAX and MONADTALL layouts
@lazy.function
def maximize_by_switching_layout(qtile):
    current_layout_name = qtile.current_group.layout.name
    if current_layout_name == "monadtall":
        qtile.current_group.layout = "max"
    elif current_layout_name == "max":
        qtile.current_group.layout = "monadtall"


keys = [
    # The essentials
    Key([mod], "Return", lazy.spawn(myTerm), desc="Terminal"),
    Key([mod], "p", lazy.spawn("rofi -show drun"), desc="Run Launcher"),
    Key([mod], "b", lazy.spawn(myBrowser), desc="Default Browser"),
    Key([mod], "g", lazy.spawn("gimp"), desc="Gimp"),
    Key([mod], "v", lazy.spawn("vscodium"), desc="VsCodium"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    # Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    # Key([mod, "shift"], "q", lazy.spawn("dm-logout -r"), desc="Logout menu"),
    # Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    # Switch between windows
    # Some layouts like 'monadtall' only need to use j/k to move
    # through the stack, but other layouts like 'columns' will
    # require all four directions h/j/k/l to move around.
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"],
        "h",
        lazy.layout.shuffle_left(),
        lazy.layout.move_left().when(layout=["treetab"]),
        desc="Move window to the left/move tab left in treetab",
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        lazy.layout.move_right().when(layout=["treetab"]),
        desc="Move window to the right/move tab right in treetab",
    ),
    Key(
        [mod, "shift"],
        "j",
        lazy.layout.shuffle_down(),
        lazy.layout.section_down().when(layout=["treetab"]),
        desc="Move window down/move down a section in treetab",
    ),
    Key(
        [mod, "shift"],
        "k",
        lazy.layout.shuffle_up(),
        lazy.layout.section_up().when(layout=["treetab"]),
        desc="Move window downup/move up a section in treetab",
    ),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "space",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    # Treetab prompt
    Key(
        [mod, "shift"],
        "a",
        add_treetab_section,
        desc="Prompt to add new section in treetab",
    ),
    # Grow/shrink windows left/right.
    # This is mainly for the 'monadtall' and 'monadwide' layouts
    # although it does also work in the 'bsp' and 'columns' layouts.
    Key(
        [mod],
        "equal",
        lazy.layout.grow_left().when(layout=["bsp", "columns"]),
        lazy.layout.grow().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the left",
    ),
    Key(
        [mod],
        "minus",
        lazy.layout.grow_right().when(layout=["bsp", "columns"]),
        lazy.layout.shrink().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the left",
    ),
    # Grow windows up, down, left, right.  Only works in certain layouts.
    # Works in 'bsp' and 'columns' layout.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    #    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    #    Key([mod], "m", lazy.layout.maximize(), desc='Toggle between min and max sizes'),
    Key([mod], "t", lazy.window.toggle_floating(), desc="toggle floating"),
    Key(
        [mod],
        "f",
        maximize_by_switching_layout(),
        lazy.window.toggle_fullscreen(),
        desc="toggle fullscreen",
    ),
    Key(
        [mod, "shift"],
        "m",
        minimize_all(),
        desc="Toggle hide/show all windows on current group",
    ),
    # Switch focus of monitors
    Key([mod], "period", lazy.next_screen(), desc="Move focus to next monitor"),
    Key([mod], "comma", lazy.prev_screen(), desc="Move focus to prev monitor"),
    # Dmenu/rofi scripts launched using the key chord SUPER+p followed by 'key'
    # KeyChord([mod], "p", [
    #     Key([], "h", lazy.spawn("dm-hub -r"), desc='List all dmscripts'),
    #     Key([], "a", lazy.spawn("dm-sounds -r"), desc='Choose ambient sound'),
    #     Key([], "b", lazy.spawn("dm-setbg -r"), desc='Set background'),
    #     Key([], "c", lazy.spawn("dtos-colorscheme -r"), desc='Choose color scheme'),
    #     Key([], "e", lazy.spawn("dm-confedit -r"), desc='Choose a config file to edit'),
    #     Key([], "i", lazy.spawn("dm-maim -r"), desc='Take a screenshot'),
    #     Key([], "k", lazy.spawn("dm-kill -r"), desc='Kill processes '),
    #     Key([], "m", lazy.spawn("dm-man -r"), desc='View manpages'),
    #     Key([], "n", lazy.spawn("dm-note -r"), desc='Store and copy notes'),
    #     Key([], "o", lazy.spawn("dm-bookman -r"), desc='Browser bookmarks'),
    #     Key([], "p", lazy.spawn("rofi-pass"), desc='Logout menu'),
    #     Key([], "q", lazy.spawn("dm-logout -r"), desc='Logout menu'),
    #     Key([], "r", lazy.spawn("dm-radio -r"), desc='Listen to online radio'),
    #     Key([], "s", lazy.spawn("dm-websearch -r"), desc='Search various engines'),
    #     Key([], "t", lazy.spawn("dm-translate -r"), desc='Translate text')
    # ])
]

###Groups

groups = []
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

group_labels = [" ", " ", " ", " ", " ", "󰻧 ", " ", "󰎇", " "]
group_layouts = [
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
]
# group_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9",]
# group_labels = ["DEV", "WWW", "SYS", "DOC", "VBOX", "CHAT", "MUS", "VID", "GFX",]
# group_labels = ["", "", "", "", "", "", "", "", "",]

# group_layouts = ["monadtall", "monadtall", "tile", "tile", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall"]
# groups= [
#     Group("1",
#           label="",
#           ),
#
#     Group("2",
#           label="",
#           # spawn='vivaldi',
#           matches=[Match(wm_class=["Vivaldi-stable"]),
#                    Match(wm_class=["Icecat"]),
#                    Match(wm_class=["Brave-browser"]),
#                    Match(wm_class=["firefox"]),
#                    ],
#           ),
#
#     Group("3",
#           label="",
#           matches=[Match(wm_class=["Zathura"]),
#                    Match(wm_class=["Evince"]),
#                    ],
#           ),
#
#     Group("4",
#           label="",
#           matches=[Match(wm_class=["discord"]),
#                    Match(wm_class=["Signal Beta"]),
#                    ],
#           ),
#
#     Group("5",
#           label="",
#           layout="max",
#           matches=[Match(wm_class=["Firefox"]),
#                    Match(wm_class=["Mplayer"]),
#                    ],
#           ),
#
#     Group("6",
#           label="",
#           matches=[Match(wm_class=["pcmanfm"]),
#                    Match(wm_class=["Org.gnome.Nautilus"]),
#                    Match(wm_class=["qBittorrent"]),
#                    ],
#           ),
#
#     Group("7",
#           label="",
#           layout="bsp",
#           matches=[Match(wm_class=["pavucontrol"]),
#                    ],
#           ),
#
#     Group("8",
#           label="",
#           matches=[Match(wm_class=["emacs"]),
#                    ],
#           ),
#
#     Group("9",
#           label="",
#           layout="max",
#           matches=[Match(wm_class=["zoom"]),
#                    Match(wm_class=["Microsoft Teams - Preview"]),
#                    ],
#           ),
#
#     Group("0",
#           label=""),
#           # label=""),
# ]
#
# groups = [
#         Group("1",label= "-"),
#         Group("2",label= "="),
#         Group("3",label= "≡"),
#         Group("4",label= "△"),
#         Group("5",label= "□"),
#         ]
# group_names = [
#     "a",
#     "s",
#     "f",
#     "t",
#     "z",
#     "u",
#     "i",
#     "o",
#     "p",
# ]
# groups = [
#     Group(
#         '1',
#         label=" ",
#         layout="monadtall",
#         # spawn="firefox"
#     ),  Group("2",
#            label=" ",
#         layout="monadtall",
#               # spawn= myBrowser,
#            # matches=[ Match(wm_class=["Brave-browser"]),
#            #          Match(wm_class=["firefox"]),
#            #          ],
#          ),
#     Group('3', label=" ", layout="monadtall"),
#
#
#     Group(
#         '4',
#         label=" ",
#         #    spawn="firefox",
#         layout="monadtall"
#     ),
#     Group(
#         '5',
#         label=" ",
#         layout="monadtall"
#     ),
#     Group('6', label="󰎇",  layout="monadtall"),
#     # Group('7', label="七", layout="monadtall"),
#     # Group('8', label="八", layout="monadtall"),
#     # Group('9', label="九", layout="monadtall"),
# ]
#
for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        )
    )

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Move focused window to group {}".format(i.name),
            ),
        ]
    )

colors = colors.Catppuccin

layout_theme = {
    "border_width": 2,
    "margin": 8,
    "border_focus": colors[7],
    "border_normal": colors[0],
}

layouts = [
    # layout.Bsp(**layout_theme),
    # layout.Floating(**layout_theme)
    # layout.RatioTile(**layout_theme),
    # layout.VerticalTile(**layout_theme),
    # layout.Matrix(**layout_theme),
    layout.MonadTall(**layout_theme),
    # layout.MonadWide(**layout_theme),
    layout.Tile(
        shift_windows=True,
        border_width=0,
        margin=0,
        ratio=0.335,
    ),
    layout.Max(
        border_width=0,
        margin=0,
    ),
    # layout.Stack(**layout_theme, num_stacks=2),
    # layout.Columns(**layout_theme),
    # layout.TreeTab(
    #     font = "Ubuntu Bold",
    #     fontsize = 11,
    #     border_width = 0,
    #     bg_color = colors[0],
    #     active_bg = colors[8],
    #     active_fg = colors[2],
    #     inactive_bg = colors[1],
    #     inactive_fg = colors[0],
    #     padding_left = 8,
    #     padding_x = 8,
    #     padding_y = 6,
    #     sections = ["ONE", "TWO", "THREE"],
    #     section_fontsize = 10,
    #     section_fg = colors[7],
    #     section_top = 15,
    #     section_bottom = 15,
    #     level_shift = 8,
    #     vspace = 3,
    #     panel_width = 240
    #     ),
    # layout.Zoomy(**layout_theme),
]

widget_defaults = dict(
    font="JetBrainsMono Nerd Font Bold",
    fontsize=15,
    padding=5,
    margin=5,
    background="#00000000",
)
icon_font_size = 5
extension_defaults = widget_defaults.copy()


## BATTERY CONFIG

# class MyBattery(Battery):
#     """
#     This is basically the Battery widget except it uses some icons, and if you click it
#     it will show the percentage numerically for 1 second.
#     """
#
#     def build_string(self, status):
#         if self.layout is not None:
#             self.layout.colour = self.foreground
#             if (
#                 status.state == BatteryState.DISCHARGING
#                 and status.percent < self.low_percentage
#             ):
#                 self.background = self.low_background
#             else:
#                 self.background = self.normal_background
#         if status.state == BatteryState.DISCHARGING:
#             if status.percent > 0.75:
#                 char = ""
#             elif status.percent > 0.45:
#                 char = ""
#             elif status.percent > 0.25:
#                 char = ""
#             else:
#                 char = ""
#         elif status.percent >= 1 or status.state == BatteryState.FULL:
#             char = ""
#         elif status.state == BatteryState.EMPTY or (
#             status.state == BatteryState.UNKNOWN and status.percent == 0
#         ):
#             char = ""
#         else:
#             char = ""
#         return self.format.format(char=char, percent=status.percent)
#
#     def restore(self):
#         self.format = "{char}"
#         self.font = "Font Awesome 5 Free"
#         self.timer_setup()
#
#     def button_press(self, x, y, button):
#         self.format = "{percent:2.0%}"
#         self.font = "TamzenForPowerline Bold"
#         self.timer_setup()
#         self.timeout_add(1, self.restore)
#
#
# battery = MyBattery(
#     format="{char}  {percent:2.0%}",
#     low_background=colors[1],
#     show_short_text=True,
#     low_percentage=0.12,
#     notify_below=12,
#     foreground=colors[1],
#     fontsize=icon_font_size + 10,
# )
#


def init_widgets_list():
    widgets_list = [
        #  widget.Spacer(length = 8),
        # widget.TextBox(
        #             text= "",
        #             padding=5,
        #             fontsize=17,
        #             foreground=colors[6],
        #         ),
        widget.Image(
            filename="~/.config/qtile/arch.svg",
            mask=True,
            margin=1,
            scale=True,
            #   adjust_x=4,
            colour=colors[6],
        ),
        widget.Spacer(length=10),
        widget.Clock(
            padding=0, fontsize=15, foreground=colors[1], format="%d-%m %a %I:%M:%S %p"
        ),
        widget.Spacer(),
        widget.GroupBox(
            fontsize=20,
            margin_y=5,
            margin_x=5,
            padding_y=0,
            padding_x=1,
            borderwidth=3,
            active=colors[7],
            inactive=colors[1],
            rounded=False,
            highlight_color=colors[0],
            highlight_method="line",
            this_current_screen_border=colors[1],
            this_screen_border=colors[7],
            other_current_screen_border=colors[7],
            other_screen_border=colors[4],
        ),
        widget.Spacer(),
        widget.ThermalSensor(
            format=" {temp:.1f}{unit}",
            fontsize=15,
            foreground=colors[1],
            foreground_alert=colors[3],
            metric=True,
            tag_sensor="Tctl",
            threshold=80,
        ),
        widget.Spacer(length=10),
        # battery,
        widget.BatteryIcon(
            theme_path="~/.config/qtile/images", scale=1.4, colour=colors[1]
        ),
        widget.Battery(
            format="{percent:2.0%}",
            fontsize=15,
            foreground=colors[1],
            # full_char='󰁹',
            # charge_char='󰂄',
            # discharge_char='󱟞',
            # empty_char='󰂃',
            # # not_charging_char='󰚥',
            low_foreground=colors[3],
            show_short_text=True,
            low_percentage=0.12,
            notify_below=12,
        ),
        widget.Systray(
            padding=10,
            icon_size=15,
            foreground=colors[1],
        ),
        widget.Spacer(length=8),
        #
    ]
    return widgets_list


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1


# All other monitors' bars will display everything but widgets 22 (systray) and 23 (spacer).
def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    del widgets_screen2[22:24]
    return widgets_screen2


# For adding transparency to your bar, add (background="#00000000") to the "Screen" line(s)
# For ex: Screen(top=bar.Bar(widgets=init_widgets_screen2(), background="#00000000", size=24)),


def init_screens():
    return [
        Screen(
            top=bar.Bar(
                widgets=init_widgets_screen1(),
                size=28,  # background="#00000000",
                opacity=1,
                background="#00000000",
                margin=[4, 8, 0, 8],
            )
        ),
        Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=26)),
        Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=26)),
    ]


if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()


def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)


def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)


def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)


def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)


def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)


mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]


# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
@hook.subscribe.client_new
def assign_app_group(client):

    d = {}
    d[group_names[0]] = [
        "Alacritty",
        "vim",
        "nvim",
    ]
    d[group_names[1]] = [
        "Navigator",
        "Firefox",
        "Vivaldi-stable",
        "Vivaldi-snapshot",
        "Brave",
        "Brave-browser",
        "navigator",
        "firefox",
        "vivaldi-stable",
        "vivaldi-snapshot",
        "brave",
        "brave-browser",
        "librewolf",
        "librewolf-bin",
        "bitwarden",
        "Bitwarden",
        "persepolis",
        "Firefox",
        "Vivaldi-stable",
        "Vivaldi-snapshot",
        "Brave",
        "Brave-browser",
        "navigator",
        "firefox",
        "vivaldi-stable",
        #     "vivaldi-snapshot",
        "brave",
        "brave-browser",
        "bitwarden",
        "Bitwarden",
        "persepolis",
    ]
    d[group_names[2]] = ["vscode", "vscodium"]
    d[group_names[3]] = [
        "Thunar",
        "Nemo",
        "Caja",
        "Nautilus",
        "org.gnome.Nautilus",
        "Pcmanfm",
        "Pcmanfm-qt",
        "thunar",
        "nemo",
        "caja",
        "nautilus",
        "org.gnome.nautilus",
        "pcmanfm",
        "pcmanfm-qt",
    ]
    d[group_names[4]] = [
        "Okular",
        "okular",
        "libreoffice",
        "Libreoffice",
        "soffice",
        "eog",
        "Eog",
        "DesktopEditors",
        "ONLYOFFICE Desktop Editors",
        "libreoffice-writer",
        "libreoffice-calc",
        # "libreoffice-impress",
        "libreoffice-draw",
        "libreoffice-base",
        "simple-scan",
    ]
    d[group_names[5]] = (
        [
            "Mail",
            "Thunderbird",
            "evolution",
            "geary",
            "mail",
            "thunderbird",
            "Msgcompose",
        ],
    )
    d[group_names[6]] = [
        "Gimp",
        "gimp",
        "Inkscape",
        "krita",
        "Nomacs",
        "Ristretto",
        "Nitrogen",
        "Feh",
        "inkscape",
        "nomacs",
        "ristretto",
        "nitrogen",
        "feh",
        "telegram-desktop",
        "TelegramDesktop",
        "Zoom",
        "zoom",
        "zoom ",
        "discord",
        "Discord",
    ]
    d[group_names[7]] = []
    d[group_names[8]] = []

    allowToBeInGroup = [
        # "Alacritty",
        "xfce4-terminal",
        "Xfce4-terminal",
        "gnome-calculator",
        "xfce4-notifyd",
        "Xfce4-notifyd",
        "gsimplecal",
        "spectacle",
        "polkit-gnome-authentication-agent-1",
        "Toolkit",
        "notification",
        "toolbar",
        "splash",
        "dialog",
        "speedcrunch",
    ]

    wm_class = client.window.get_wm_class()
    if len(wm_class) >= 1:
        wm_class = wm_class[0]
        if wm_class not in allowToBeInGroup:
            for i in range(len(d)):
                if wm_class in list(d.values())[i]:
                    group = list(d.keys())[i]
                    client.togroup(group)
                    client.group.cmd_toscreen(toggle=False)
                    break
                else:
                    client.togroup("9")
                    client.group.cmd_toscreen(toggle=False)


dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    border_focus=colors[8],
    border_width=2,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="dialog"),  # dialog boxes
        Match(wm_class="download"),  # downloads
        Match(wm_class="error"),  # error msgs
        Match(wm_class="file_progress"),  # file progress boxes
        Match(wm_class="kdenlive"),  # kdenlive
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="notification"),  # notifications
        Match(wm_class="pinentry-gtk-2"),  # GPG key password entry
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(wm_class="toolbar"),  # toolbars
        Match(wm_class="Yad"),  # yad boxes
        Match(title="branchdialog"),  # gitk
        Match(title="Confirmation"),  # tastyworks exit box
        Match(title="Qalculate!"),  # qalculate-gtk
        Match(title="pinentry"),  # GPG key password entry
        Match(title="tastycharts"),  # tastytrade pop-out charts
        Match(title="tastytrade"),  # tastytrade pop-out side gutter
        Match(title="tastytrade - Portfolio Report"),  # tastytrade pop-out allocation
        Match(wm_class="tasty.javafx.launcher.LauncherFxApp"),  # tastytrade settings
    ],
)
auto_fullscreen = True
focus_on_window_activation = "focus"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/scripts/autostart.sh"])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
