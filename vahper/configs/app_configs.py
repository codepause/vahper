from epta.core import *
from .app_settings import *

class GameConfig(Config):
    def __init__(self):
        super(GameConfig, self).__init__(GameSettings())


class ScreenCaptureConfig(Config):
    def __init__(self, **kwargs):
        super(ScreenCaptureConfig, self).__init__(ScreenCaptureSettings(), **kwargs)


class ImageRecognitionConfig(Config):
    def __init__(self, **kwargs):
        super(ImageRecognitionConfig, self).__init__(ImageRecognitionSettings(), **kwargs)


class BBoxRendererConfig(Config):
    def __init__(self, **kwargs):
        super(BBoxRendererConfig, self).__init__(BBoxRenderSettings(), **kwargs)


class MouseControllerConfig(Config):
    def __init__(self, **kwargs):
        super(MouseControllerConfig, self).__init__(MouseControllerSettings(), **kwargs)


class KeyboardControllerConfig(Config):
    def __init__(self, **kwargs):
        super(KeyboardControllerConfig, self).__init__(KeyboardControllerSettings(), **kwargs)


class AppConfig(Config):
    def __init__(self, **kwargs):
        super(AppConfig, self).__init__(AppSettings(), **kwargs)

        self.game_config = GameConfig()
        self.screen_capture_config = ScreenCaptureConfig()
        self.image_recognition_config = ImageRecognitionConfig()
        self.bbox_renderer_config = BBoxRendererConfig()
        self.mouse_controller_config = MouseControllerConfig()
        self.keyboard_controller_config = KeyboardControllerConfig()
