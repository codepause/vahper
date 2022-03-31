from epta.core import *
from epta.core.base_ops import *
from epta.tools.base import PositionMapperWrapper


class ConfigTool(Variable, ConfigDependent):
    def __init__(self, *args, **kwargs):
        super(ConfigTool, self).__init__(*args, **kwargs)

    def use(self, *args, **kwargs):  # return this value
        return self.tool.use(self.config)


class ScreenCenterMapper(ToolDict):
    def __init__(self, game_config: 'Config', name: str = 'screen_center_mapper', **kwargs):
        super(ScreenCenterMapper, self).__init__(name=name, **kwargs)
        tools = {
            'relative_x': ConfigTool(config=game_config,
                                     tool=Lambda(lambda cfg: cfg.settings.screen_w / 2)),
            'relative_y': ConfigTool(config=game_config,
                                     tool=Lambda(lambda cfg: cfg.settings.screen_h / 2)),
        }
        for key, _tool in tools.items():
            self.add_tool(key, _tool)


class ImageMapper(ToolDict):
    def __init__(self, screen_capture_config: 'Config', name: str = 'image_mapper', **kwargs):
        super(ImageMapper, self).__init__(name=name, **kwargs)
        tools = {
            'x': ConfigTool(config=screen_capture_config,
                            tool=Lambda(lambda cfg: cfg.settings.x)),
            'y': ConfigTool(config=screen_capture_config,
                            tool=Lambda(lambda cfg: cfg.settings.y)),
            'w': ConfigTool(config=screen_capture_config,
                            tool=Lambda(lambda cfg: cfg.settings.w)),
            'h': ConfigTool(config=screen_capture_config,
                            tool=Lambda(lambda cfg: cfg.settings.h))
        }
        for key, _tool in tools.items():
            self.add_tool(key, _tool)


class PositionManager(ToolDict):
    def __init__(self, cfg: 'Config', **kwargs):
        tools = self.prepare_tools(cfg)
        super(PositionManager, self).__init__(tools=tools, **kwargs)

    @staticmethod
    def prepare_tools(cfg: 'Config'):
        base_mapper = ToolDict([PositionMapperWrapper(mapper) for mapper in
                                [ScreenCenterMapper(cfg.game_config), ImageMapper(cfg.screen_capture_config)]],
                               name='base_mapper')

        position_wrapper = PositionMapperWrapper(ToolDict({
            'x': Compose(lambda pm: pm['screen_center_mapper']['relative_x'] + pm['image_mapper']['x'],
                         (Wrapper(base_mapper),)),
            'y': Compose(lambda pm: pm['screen_center_mapper']['relative_y'] + pm['image_mapper']['y'],
                         (Wrapper(base_mapper),)),
            'w': Compose(lambda pm: pm['image_mapper']['w'],
                         (Wrapper(base_mapper),)),
            'h': Compose(lambda pm: pm['image_mapper']['h'],
                         (Wrapper(base_mapper),)),
        }, name='image_capture'))
        return [base_mapper, position_wrapper]
