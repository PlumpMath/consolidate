import sys
from collections import defaultdict

from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
from asciimatics.widgets import Frame, Text, Layout, ListBox, Widget, Button, Label, TextBox
from asciimatics.effects import Print
from asciimatics.renderers import StaticRenderer
from asciimatics.exceptions import ResizeScreenError, StopApplication


class Window:
    def __init__(self, model, additional_scenes=None):
        self._additional_scenes = additional_scenes
        self._model = model

    def start(self):
        while True:
            try:
                Screen.wrapper(self.play_scenes, catch_interrupt=True)
                sys.exit(0)
            except ResizeScreenError as e:
                pass

    def play_scenes(self, screen):
        scenes = [
            Scene([GameFrame(screen, self._model)], -1, name="Controls"),
        ]
        if self._additional_scenes: scenes += self._additional_scenes
        
        screen.play(scenes, stop_on_resize=True)



class GameFrame(Frame):
    def __init__(self, screen, model):
        super(GameFrame, self).__init__(screen,
                                        screen.height,
                                        screen.width)

        self._statement = model.get_statement(1)
        self._picture = model.get_scene("start")

        self.palette = defaultdict(
            lambda: (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK))
        for key in ["selected_focus_field", "label"]:
            self.palette[key] = (Screen.COLOUR_BLACK, Screen.A_BOLD, Screen.COLOUR_WHITE)
        self.palette["title"] = (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_WHITE)

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)

        answer_options = []
        for key, answer in enumerate(self._statement["answers"], 1):
            text = "{num}. {label}".format(num=key, label=answer["text"])
            value = key
            answer_options.append((text, value))

        self._answer_options = ListBox(
            Widget.FILL_FRAME,
            answer_options,
            name="answer_options",
            on_change=self._on_pick)

        self._picture_display = TextBox(16, as_string=True)
        self._picture_display.disabled = True

        self._remark = Text()
        self._remark.value = self._statement['remark']
        self._remark.disabled = True

        self._statement_text = Text()
        self._statement_text.value = self._statement['text']
        self._statement_text.disabled = True

        layout.add_widget(self._picture_display)
        layout.add_widget(self._remark)
        layout.add_widget(self._statement_text)
        layout.add_widget(self._answer_options)
        layout.add_widget(
                Label("Press `q` to quit."))
        
        self.fix()
        self._on_pick()

    def _on_pick(self):
        pass

    def _treceback(self):
        import pudb; pudb.set_trace()

    def _update(self, frame_no):
        self._picture_display.value = self._picture
        self._remark.value = self._statement['remark']
        self._statement_text.value = self._statement['text']

        # Now redraw as normal
        super(GameFrame, self)._update(frame_no)

    def process_event(self, event):
        # Do the key handling for this Frame.
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord('q'), ord('Q'), Screen.ctrl("c")]:
                self._quit()

            # Force a refresh for improved responsiveness
            self._last_frame = 0

        # Now pass on to lower levels for normal handling of the event.
        return super(GameFrame, self).process_event(event)


    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")
