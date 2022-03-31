import tkinter as tk
from multiprocessing import Process, Queue
import pywintypes
import win32api
import win32con
from PIL import Image, ImageTk
import numpy as np

from epta.core import ConfigDependent, Config, PositionDependent
from epta.tools.renderers import BaseRenderer
import epta.core as ec
import epta.tools.base as eb
import epta.core.base_ops as eco

import vahper.tools.base as vb


class ImageRenderer(PositionDependent, ConfigDependent):
    root: tk.Tk
    canvas: tk.Canvas
    image_on_canvas: ImageTk.PhotoImage
    _image: np.array

    # https://stackoverflow.com/questions/21840133/how-to-display-text-on-the-screen-without-a-window-using-python
    def __init__(self, config: type, image_q: 'Queue', commands_q: 'Queue', name: str = 'screen_renderer',
                 key: str = None,
                 **kwargs):
        config = config()
        position_manager = vb.PositionManager(config)

        super(ImageRenderer, self).__init__(config=config, position_manager=position_manager, name=name,
                                            key=key, **kwargs)
        self.position_manager.update()
        self.update()

        self.ignore_color = '#fc0000'
        self._image_q = image_q
        self._commands_q = commands_q

        image_shape = self.get_image_shape()
        self._dummy_image = np.concatenate(
            [
                np.ones((*image_shape[:2], 1), dtype=np.uint8) * 252,
                np.zeros((*image_shape[:2], 1), dtype=np.uint8),
                np.zeros((*image_shape[:2], 1), dtype=np.uint8)
            ],
            axis=-1
        )

        self.stop_render_after_n_seconds = 0.1
        self.timer = 0
        self.render_every_ms = 10
        self._quit = False

        self._init_labels()
        self.start()

    def get_image_shape(self):
        return self.inner_position[3] - self.inner_position[1], self.inner_position[2] - self.inner_position[0]

    def get_root_position(self):
        return self.inner_position[0], self.inner_position[1]

    def _init_labels(self):
        # https://stackoverflow.com/questions/56096839/getting-background-color-as-well-when-i-transparent-the-background-color
        self.root = tk.Tk()
        height, width = self._dummy_image.shape[:2]
        canvas = tk.Canvas(self.root, height=height, width=width)
        self._prepare_image(self._dummy_image)
        self.image_on_canvas = canvas.create_image(0, 0, anchor='nw', image=self._image)
        canvas.config(highlightthickness=0)
        canvas.master.overrideredirect(True)
        x, y = self.get_root_position()
        canvas.master.geometry(f"{width}x{height}+{x}+{y}")
        canvas.master.lift()
        canvas.master.wm_attributes("-topmost", True)
        canvas.master.wm_attributes("-disabled", True)
        canvas.master.wm_attributes("-transparentcolor", '#fc0000')
        hWindow = pywintypes.HANDLE(int(canvas.master.frame(), 16))
        # http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx
        # The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
        exStyle = win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST  # | win32con.WS_EX_COMPOSITED
        win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)
        canvas.grid(row=0, column=0)
        self.canvas = canvas

    def _prepare_image(self, image: np.ndarray):
        self._image = ImageTk.PhotoImage(image=Image.fromarray(image))

    def parse_commands_q(self, *args, **kwargs):
        if not self._commands_q.empty():
            command = self._commands_q.get()
            if command == 'stop':
                self._quit = True
            if command == 'update':
                # TODO: be clever and redo all of this
                pass

    def parse_image_q(self, *args, **kwargs):
        if self._image_q.empty():
            if self.timer > self.stop_render_after_n_seconds:
                self._prepare_image(self._dummy_image)
                self.timer = self.stop_render_after_n_seconds + 1
        else:
            self._prepare_image(self._image_q.get())
            self.timer = 0

    def render_loop(self, **kwargs):
        self.timer += self.render_every_ms / 1000
        self.parse_commands_q()
        self.parse_image_q()
        self.canvas.itemconfig(self.image_on_canvas, image=self._image)
        if not self._quit:
            self.root.after(self.render_every_ms, self.render_loop)
        else:
            self.quit()

    def quit(self):
        self.root.destroy()

    def start(self):
        self.render_loop()
        self.root.mainloop()


class ImageRendererMP(BaseRenderer, eco.Atomic):
    def __init__(self, config: 'Config', name: str = 'screen_renderer_mp', **kwargs):
        super(ImageRendererMP, self).__init__(name=name, **kwargs)
        self.image_q = Queue()
        self.commands_q = Queue()

        self.process = Process(target=ImageRenderer,
                               args=(type(config), self.image_q, self.commands_q),
                               kwargs={'key': self.key})

    def start(self):
        self.process.start()

    def join(self):
        self.commands_q.put('stop')
        self.process.join()

    def render(self, image: np.ndarray, **kwargs):
        if self.image_q.empty():  # "sync" frames
            self.image_q.put(image)
        return image
