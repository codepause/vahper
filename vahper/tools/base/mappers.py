from dataclasses import dataclass, field

from epta.tools.base import PositionMapper


@dataclass
class ScreenCenterMapper(PositionMapper):
    config: field(init=True)
    _key_mappings: tuple = tuple()
    name: str = 'screen_center'

    relative_x: callable = lambda config: config.game_config.settings.screen_w / 2
    relative_y: callable = lambda config: config.game_config.settings.screen_h / 2

@dataclass
class ImageCaptureMapper(ScreenCenterMapper):
    name: str = 'image_capture'

    x: callable = lambda _: None
    y: callable = lambda _: None
    w: callable = lambda _: None
    h: callable = lambda _: None

    def use(self, *args, **kwargs):
        screen_cropper_settings = self.config.screen_capture_config.settings
        self.x = lambda *_: self.relative_x(self.config) + screen_cropper_settings.x
        self.y = lambda *_: self.relative_y(self.config) + screen_cropper_settings.y
        self.w = lambda *_: screen_cropper_settings.w
        self.h = lambda *_: screen_cropper_settings.h


"""
@dataclass
class AdditionalRenderWindowMapper(PositionMapper):
    config: field(init=True)
    _key_mappings: tuple = tuple()
    name: str = 'additional_renderer_window'

    x: callable = lambda _: None
    y: callable = lambda _: None
    w: callable = lambda config: config.render_config.settings.w
    h: callable = lambda config: config.render_config.settings.y
"""