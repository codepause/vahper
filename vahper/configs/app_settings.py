from dataclasses import dataclass

from epta.core import Settings


@dataclass
class GameSettings(Settings):
    screen_w: int = 1920
    screen_h: int = 1080
    mouse_sensitivity: float = 1.0  # 0.663


@dataclass
class ScreenCaptureSettings(Settings):
    window_name: str = 'Valorant (TM) Client'
    x: int = -1920 / 6  # relative to the center of a screen
    y: int = -1080 / 6
    w: int = 1920 / 3
    h: int = 1020 / 3


@dataclass
class ImageRecognitionSettings(Settings):
    weights_path = '../vahper/tools/recognition/hpep_cut/weights/checkpoint_iter_370000.pth'
    device = 'cuda:0'


@dataclass
class BBoxRenderSettings(Settings):
    pass


@dataclass
class MouseControllerSettings(Settings):
    duration: float = 0.001


@dataclass
class KeyboardControllerSettings(Settings):
    working_state_key: str = 'NUM_1'
    render_state_key: str = 'NUM_2'
    active_state_key: str = 'NUM_3'
    exit_state_key: str = 'NUM_0'


@dataclass
class AppSettings(Settings):
    pass
