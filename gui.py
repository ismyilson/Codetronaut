import queue

import PySimpleGUI as sg

from screeninfo import get_monitors
from global_vars import t_event_not_muted, t_event_quit

WINDOW_SIZE = (300, 500)


class GUI:
    _window: sg.Window
    _data_queue: queue.Queue

    def __init__(self, data_queue):
        sg.set_options(element_padding=(0, 0))

        self._data_queue = data_queue

    def start(self):
        self._window = sg.Window('Voice2Code',
                                 layout=self._layout(),
                                 size=WINDOW_SIZE,
                                 location=self._make_window_location(),
                                 keep_on_top=True,
                                 # grab_anywhere=True,
                                 finalize=True)

        self._setup_binds()

        while not t_event_quit.is_set():
            event, values = self._window.read(timeout=100)

            self._update()

            if event == sg.WIN_CLOSED:
                break

            if event == '<SPACEBAR>':
                if t_event_not_muted.is_set():
                    self._window['-MIC-'].update('images/voice_off.png')
                    t_event_not_muted.clear()
                else:
                    self._window['-MIC-'].update('images/voice_on.png')
                    t_event_not_muted.set()

        self._clean_up()

    def _layout(self):
        image_column = [
            [sg.Image('images/voice_on.png', key='-MIC-')]
        ]

        layout = [
            [sg.Column(image_column, justification='center')],
            [sg.Text('', key='-TRANSCRIBEDTEXT1-', expand_x=False)],
            [sg.Text('', key='-TRANSCRIBEDTEXT2-', expand_x=False)],
            [sg.Text('', key='-TRANSCRIBEDTEXT3-', expand_x=False)],
            [sg.Text('', key='-TRANSCRIBEDTEXT4-', expand_x=False)],
            [sg.Text('', key='-TRANSCRIBEDTEXT5-', expand_x=False)],
        ]

        return layout

    def _make_window_location(self):
        monitors = get_monitors()
        primary_monitor = None
        for monitor in monitors:
            if monitor.is_primary:
                primary_monitor = monitor
                break

        if primary_monitor is None:
            return 0 + WINDOW_SIZE[0], 0 + WINDOW_SIZE[1]

        return primary_monitor.width - WINDOW_SIZE[0] - 10, WINDOW_SIZE[1] / 3

    def _setup_binds(self):
        self._window.bind('<space>', '<SPACEBAR>')

    def _update(self):
        while not self._data_queue.empty():
            key, value = self._data_queue.get()
            self._window[key].update(value)

    def _clean_up(self):
        print('Cleaning up GUI')

        t_event_quit.set()  # Let others know we're quitting

        self._window.close()
