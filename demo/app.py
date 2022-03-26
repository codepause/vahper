import time
import os

import epta.core as ec
import epta.tools.base as eb

import vahper.tools.base as vb
from vahper.configs.app_configs import AppConfig
from vahper.tools.recognition import SkeletonRecogniser
from vahper.tools.hookers import KeyboardAppController, MouseController
from vahper.tools.renderers import SingleRenderer
from vahper.tools.hookers.image_hookers import MssScreenHooker

class App:
    def __init__(self):
        self.app_config = AppConfig()
        self.app_states = dict()

        self.position_manager = ec.ToolDict([
            eb.PositionMapperWrapper(vb.ImageCaptureMapper(self.app_config))
        ])
        self.ih = MssScreenHooker(config=self.app_config, position_manager=self.position_manager,
                                  key='image_capture')
        self.ir = SkeletonRecogniser(self.app_config.image_recognition_config)
        self.mh = MouseController(self.app_config, position_manager=self.position_manager, key='image_capture')

        self.kh = KeyboardAppController(self.app_config.keyboard_controller_config,
                                        self.app_states)
        self.re = SingleRenderer(self.app_config, key='image_capture')

    def update(self):
        self.position_manager.update()
        self.mh.update()
        self.ih.update()

    def recognise(self, image: 'np.ndarray'):
        data = {'image': image, 'bboxes': self.ir.image_to_data(image)}
        return data

    def launch_once(self):
        if self.app_states.get('working_state', 0):
            image = self.ih.hook_image()
            data = self.recognise(image)
            self.re.render(data, state=self.app_states.get('render_state', 0))
            self.mh.launch_once(data, state=self.app_states.get('active_state', 0))
        else:
            time.sleep(0.1)
        return None

    def launch(self):
        self.re.start()
        while not self.app_states.get('exit', 0):
            self.launch_once()
        self.re.join()
        os._exit(0)
