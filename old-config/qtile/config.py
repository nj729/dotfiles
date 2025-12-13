#####################################
# Qtile Configuration
# Author: rude
# ~/.config/qtile/config.py
####################################

# Make sure 'qtile-extras' is installed or this config will not work.

import os
import subprocess

from libqtile import bar, extension, hook, layout, qtile
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
from libqtile.log_utils import logger
from libqtile.widget.battery import Battery, BatteryState
from qtile_extras import widget
from qtile_extras.widget import decorations
from qtile_extras.widget.decorations import RectDecoration

import colors

### Default variables

mod = "mod4"
terminal = "alacritty"
browser = "librewolf"
filemanager = "pcmanfm"

### Functions required for some keymaps


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


# Allows you to input a name when adding treetab section.
@lazy.layout.function
def add_treetab_section(layout):
    prompt = qtile.widgets_map["prompt"]
    prompt.start_input("Section name: ", layout.cmd_add_section)


### Keymaps

keys = [
    # The essentials
    Key([mod], "Return", lazy.spawn(terminal), desc="Terminal"),
    Key([mod], "p", lazy.spawn("rofi -show drun"), desc="Run Launcher"),
    Key([mod], "b", lazy.spawn(browser), desc="Default Browser"),
    Key([mod], "g", lazy.spawn("gimp"), desc="Gimp"),
    Key([mod], "v", lazy.spawn("vscodium"), desc="VsCodium"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    # Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "return", lazy.spawn(filemanager), desc="Pcmanfm"),
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    # volume keys
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c 0 sset Master 1- unmute")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c 0 sset Master 1+ unmute")),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
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
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "m", lazy.layout.maximize(), desc="Toggle between min and max sizes"),
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

layout_defaults = {
    "border_width": 2,
    "margin": 8,
    "border_focus": colors[7],
    "border_normal": colors[0],
}

layouts = [
    layout.Bsp(**layout_defaults),
    layout.Floating(**layout_defaults),
    # layout.RatioTile(**layout_defaults),
    layout.VerticalTile(**layout_defaults),
    # layout.Matrix(**layout_defaults),
    layout.MonadTall(**layout_defaults),
    layout.MonadWide(**layout_defaults),
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
    layout.Stack(**layout_defaults, num_stacks=2),
    layout.Columns(**layout_defaults),
]

widget_defaults = dict(
    font="CaskaydiaCove Nerd Font Bold",
    fontsize=15,
    padding=5,
    margin=5,
    foreground=colors[2],
    background="#00000000",
)

extension_defaults = widget_defaults.copy()


def init_widgets_list():
    widgets_list = [
        # widget.TextBox(
        #             text= "",
        #             padding=5,
        #             fontsize=17,
        #             foreground=colors[6],
        #         ),
        widget.Image(
            filename="~/.config/qtile/arch.svg",
            mask=False,
            margin=1,
            scale=True,
            background=colors[6],
            #   adjust_x=4,
        ),
        widget.Spacer(length=5),
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
            highlight_color=colors[6],
            highlight_method="line",
            this_current_screen_border=colors[1],
            this_screen_border=colors[7],
            other_current_screen_border=colors[7],
            other_screen_border=colors[4],
        ),
        widget.Spacer(length=5),
        widget.WindowName(padding=10, background=colors[6], foreground=colors[2]),
        widget.Spacer(length=5),
        # widget.Spacer(background=colors[6]),
        widget.TextBox(
            text="󰘚",
            fontsize=17,
            background=colors[6],
        ),
        widget.Memory(
            background=colors[6],
            format="{MemUsed:.0f}MB ",
        ),
        widget.Spacer(length=5),
        widget.ThermalSensor(
            format=" {temp:.1f}{unit}",
            fontsize=15,
            background=colors[6],
            foreground_alert=colors[9],
            metric=True,
            tag_sensor="Tctl",
            threshold=80,
        ),
        widget.Spacer(length=5),
        widget.TextBox(
            text="󰕾",
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("pavucontrol")},
            fontsize=20,
            background=colors[6],
        ),
        widget.Volume(fontsize=15, background=colors[6]),
        widget.Spacer(length=5),
        # widget.Spacer(length=5),
        # battery,
        widget.Battery(
            format="{percent:2.0%} {char}",
            fontsize=15,
            background=colors[6],
            full_char="charged",
            charge_char="ﮣ",
            discharge_char="discharging",
            empty_char="󰂃",
            not_charging_char="charging paused",
            low_foreground=colors[9],
            show_short_text=True,
            low_percentage=0.12,
            notify_below=12,
        ),
        widget.Spacer(length=5),
        widget.TextBox(text=" ", fontsize=17, background=colors[6]),
        widget.Clock(
            padding=0,
            fontsize=15,
            background=colors[6],
            format="%d %a %I:%M %p ",
        ),
        widget.Spacer(length=5),
        widget.Systray(
            icon_size=15,
            # background=colors[6],
            padding=10,
            theme_path="rose-pine-gtk",
            decorations=[RectDecoration(radius=0, extrawidth=5)],
        ),
        widget.Spacer(length=5),
        #     widget.Spacer(),
        widget.CurrentLayoutIcon(
            scale=0.8,
            background=colors[6],
            use_mask=True,
        ),
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
            ),
            wallpaper="~/0063.jpg",
            wallpaper_mode="fill",
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
        "LibreWolf",
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
        "nsxiv",
        "Nsxiv",
        "inkscape",
        "nomacs",
        "ristretto",
        "nitrogen",
        "feh",
        "telegram-desktop",
        "TelegramDesktop",
        "discord",
        "Discord",
    ]
    d[group_names[7]] = [
        "youtube music",
        "YouTube Music",
    ]

    d[group_names[8]] = []

    allowToBeInGroup = [
        # "Alacritty",
        "polkit-gnome-authentication-agent-1",
        "Toolkit",
        "notification",
        "toolbar",
        "dialog",
        "pavucontrol",
        "blueman-manager",
        "blueman-applet",
        "Blueman-applet",
        "Blueman-manager",
        "nm-applet",
        "Nm-applet",
    ]

    wm_class = client.window.get_wm_class()
    if len(wm_class) >= 1:
        wm_class = wm_class[0]
        if wm_class not in allowToBeInGroup:
            for i in range(len(d)):
                if wm_class in list(d.values())[i]:
                    group = list(d.keys())[i]
                    client.togroup(group)
                    client.group.toscreen(toggle=False)
                    break
                else:
                    client.togroup("9")
                    client.group.toscreen(toggle=False)


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
        Match(wm_class="pavucontrol"),
        Match(wm_class="blueman-manager"),
        Match(wm_class="Blueman-manager"),
        Match(wm_class="nm-applet"),
        Match(wm_class="Nm-applet"),
        Match(wm_class="blueman-applet"),
        Match(wm_class="Blueman-applet"),
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


#
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.call([home])


#
#
wmname = "LG3D"
