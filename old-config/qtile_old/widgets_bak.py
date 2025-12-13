widgets_list = [
               widget.GroupBox(
                 fontsize = 11,
                 margin_y = 5,
                 margin_x = 5,
                 padding_y = 0,
                 padding_x = 1,
                 borderwidth = 3,
                 active = colors[8],
                 inactive = colors[1],
                 rounded = False,
                 highlight_color = colors[2],
                 highlight_method = "line",
                 this_current_screen_border = colors[7],
                 this_screen_border = colors [4],
                 other_current_screen_border = colors[7],
                 other_screen_border = colors[4],
                 ),
        widget.TextBox(
                 text = '|',
                 font = "Ubuntu Mono",
                 foreground = colors[1],
                 padding = 2,
                 fontsize = 14
                 ),
        widget.CurrentLayoutIcon(
                 # custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                 foreground = colors[1],
                 padding = 4,
                 scale = 0.6
                 ),
        widget.CurrentLayout(
                 foreground = colors[1],
                 padding = 5
                 ),
        widget.TextBox(
                 text = '|',
                 font = "Ubuntu Mono",
                 foreground = colors[1],
                 padding = 2,
                 fontsize = 14
                 ),
        
        widget.WindowName(
                 foreground = colors[6],
                 max_chars = 40
                 ),
                     widget.Spacer(length = 8),
        # widget.GenPollText(
        #          update_interval = 300,
        #          func = lambda: subprocess.check_output("printf $(uname -r)", shell=True, text=True),
        #          foreground = colors[3],
        #          fmt = '❤  {}',
        #          decorations=[
        #              BorderDecoration(
        #                  colour = colors[3],
        #                  border_width = [0, 0, 2, 0],
        #              )
        #          ],
        #          ),


       widget.Spacer(length = 8),
                        widget.ThermalSensor(
                         foreground = colors[5],
                         format = ' Thermals: {temp:.1f}{unit}',
                         foreground_alert = colors[6],
                         metric = True,
            #  update_interval: 2,
                         padding = 3,
                         threshold = 80,
                        decorations=[
                     BorderDecoration(
                         colour = colors[5],
                         border_width = [0, 0, 2, 0],
                     )
                 ],

                         ),
        widget.Spacer(length = 8),
        widget.Memory(
                 foreground = colors[8],
                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
                 format = '{MemUsed: .0f}{mm}',
                 fmt = '🖥  Mem: {} used',
                 decorations=[
                     BorderDecoration(
                         colour = colors[8],
                         border_width = [0, 0, 2, 0],
                     )
                 ],
                 ),
        # widget.Spacer(length = 8),
        # widget.DF(
        #          update_interval = 60,
        #          foreground = colors[5],
        #          mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e df')},
        #          partition = '/',
        #          #format = '[{p}] {uf}{m} ({r:.0f}%)',
        #          format = '{uf}{m} free',
        #          fmt = '🖴  Disk: {}',
        #          visible_on_warn = False,
        #          decorations=[
        #              BorderDecoration(
        #                  colour = colors[5],
        #                  border_width = [0, 0, 2, 0],
        #              )
        #          ],
        #          ),
        widget.Spacer(length = 8),
        widget.Volume(
                 foreground = colors[7],
                 fmt = '🕫  Vol: {}',
                 decorations=[
                     BorderDecoration(
                         colour = colors[7],
                         border_width = [0, 0, 2, 0],
                     )
                 ],
                 ),
        # widget.Spacer(length = 8),
        # widget.KeyboardLayout(
        #          foreground = colors[4],
        #          fmt = '⌨  Kbd: {}',
        #          decorations=[
        #              BorderDecoration(
        #                  colour = colors[4],
        #                  border_width = [0, 0, 2, 0],
        #              )
        #          ],
        #          ),
        widget.Spacer(length = 8),
        widget.Clock(
                 foreground = colors[8],
                 format = "⏱  %a, %b %d - %H:%M",
                 decorations=[
                     BorderDecoration(
                         colour = colors[8],
                         border_width = [0, 0, 2, 0],
                     )
                 ],
                 ),
        widget.Spacer(length = 8),
  widget.Battery(
            #   font="Noto Sans",
                         update_interval = 10,
            fontsize = 12,
            format = '🔋 Battery: {char} {percent: 2.0%}',
                         foreground = colors[7],
                         decorations=[
                           BorderDecoration(
                           colour = colors[7],
                           border_width = [0, 0, 2, 0],
                             )
                           ],

	                     ),


        widget.Spacer(length = 8),
         widget.TextBox(
                    text=" ",
                    background=catppuccin["Mantle"],
                    foreground=catppuccin["Red"],
                    fontsize=15,
                    mouse_callbacks={
                        "Button1": lazy.shutdown(),
                    },
                ),
 
        widget.Spacer(length = 8),
        widget.Systray(padding = 3),
        widget.Spacer(length = 8),
 
        ]
 
