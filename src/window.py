import sys
from collections import defaultdict

from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Text, Layout, ListBox, Widget, Button, Label, TextBox
from asciimatics.exceptions import ResizeScreenError, StopApplication


class Window:
    def __init__(self, picture=None, additional_scenes=None):
        self._additional_scenes = additional_scenes
        self._picture = picture

    def start(self):
        while True:
            try:
                Screen.wrapper(self.play_scenes, catch_interrupt=True)
                sys.exit(0)
            except ResizeScreenError as e:
                pass

    def play_scenes(self, screen):
        scenes = [
            Scene([GameFrame(screen, self._picture)], -1, name="Main"),
        ]
        if self._additional_scenes: scenes += self._additional_scenes
        
        screen.play(scenes, stop_on_resize=True)



class GameFrame(Frame):
    def __init__(self, screen, picture=''):
        super(GameFrame, self).__init__(screen,
                                        screen.height,
                                        screen.width,
                                        # on_load=self._reload_list,
                                        hover_focus=True,
                                        title="AGIRL")

        self.palette = defaultdict(
            lambda: (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK))
        for key in ["selected_focus_field", "label"]:
            self.palette[key] = (Screen.COLOUR_BLACK, Screen.A_BOLD, Screen.COLOUR_WHITE)
        self.palette["title"] = (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_WHITE)

        layout = Layout([1,1,1,1], fill_frame=True)
        self.add_layout(layout)

        self._answer_options = ListBox(
            Widget.FILL_FRAME,
            [('1. wup', 1), ('2.dup', 2)],
            name="answer_options",
            on_change=self._on_pick)

        self._picture = TextBox(10)
        self._picture.disabled = True
        self._picture.value = picture
        self.reset()

        # import pudb; pudb.set_trace()

        layout.add_widget(self._picture)
        layout.add_widget(self._answer_options)
        layout.add_widget(Button("Quit", self._quit))
        self.fix()
        self._on_pick()

    def _on_pick(self):
        pass

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")


# class Window:
#     """
#     Representation of game screen.
#     Consists of a scene picture frame and dialog
#     """

#     def __init__(self, screen, dialog):
#         self.screen = screen
#         self.dialog = dialog
#         while True:
#             try:
#                 Screen.wrapper(self.scrn, arguments=[None])
#             except ResizeScreenError:
#                 pass

#     def scrn(self, screen, scene):
#         # frame = Frame(screen, screen.height * 2 // 3, screen.width * 2 // 3, has_border=True, title="AGIRL")
#         frame = Frame(screen, 100, 100, has_border=True, title="AGIRL")
#         layout = layout = Layout([100], fill_frame=True)
#         frame.add_layout(layout)
#         layout.add_widget(Text("Name:", "name"))
#         scenes = [
#             Scene([frame], -1, name="Main"),
#             Scene([frame], -1, name="Main")
#         ]

#         screen.play(scenes, stop_on_resize=True, start_scene=scene)
        

#     def update(self, frame=None, dialog=None):
#         if frame: self.frame = frame
#         if dialog: self.dialog = dialog
#         self.render()

#     def render(self):
#         self.render_screen()
#         self.render_dialog()

#     def render_screen(self):
#         self.stdscr.addstr(0, 0, self.screen)
#         self.stdscr.refresh()

#     def render_dialog(self):
#         print(self.dialog)

#     # def teardown(self):
#     #     # reverse everything that you changed about the terminal
#     #     nocbreak()
#     #     self.stdscr.keypad(False)
#     #     echo()
#     #     # restore the terminal to its original state
#     #     endwin()