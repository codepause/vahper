import mouse
import numpy as np

from epta.core import BaseTool, ConfigDependent, PositionDependent


class MouseControllerBase(BaseTool, ConfigDependent):
    def __init__(self, config: 'Config', name: str = 'mouse_controller_base', **kwargs):
        super(MouseControllerBase, self).__init__(config=config, name=name, **kwargs)

    def move_mouse_delta(self, target_position_delta: tuple):
        dx, dy = target_position_delta
        duration = self.config.mouse_controller_config.settings.get('duration', 0.01)
        mouse.move(dx, dy, duration=duration, absolute=False)

    def get_modified_delta(self, target_position_delta: tuple):
        dx, dy = target_position_delta

        dx *= 1 / self.config.game_config.settings.get('mouse_sensitivity', 1)
        dy *= 1 / self.config.game_config.settings.get('mouse_sensitivity', 1)

        return dx, dy

    def move_mouse_delta_modified(self, target_position_delta: tuple):
        self.move_mouse_delta(self.get_modified_delta(target_position_delta))


class MouseController(PositionDependent, ConfigDependent):
    def __init__(self, config: 'Config', **kwargs):
        super(MouseController, self).__init__(config=config, name='mouse_controller', **kwargs)
        self.controller = MouseControllerBase(self.config)

        self.offset = None

    def update(self, *args, **kwargs):
        self.inner_position = self.make_inner_position(*args, **kwargs)
        self.offset = np.array(self.inner_position[:2]).astype(np.int32)

    def prepare_data(self, data: dict):
        bboxes = data['bboxes']
        head_positions = list()
        for pose in bboxes:
            if pose.head_center is not None:
                head_positions.append(pose.head_center[None])
        if head_positions:
            head_positions = np.concatenate(head_positions, axis=0)
            head_positions += self.offset
            return head_positions
        else:
            return None

    def launch_once(self, data, state: int = 0):
        if state:
            bboxes = self.prepare_data(data)
            if bboxes is not None:
                deltas = bboxes - np.array(mouse.get_position())
                absolute_deltas = np.linalg.norm(deltas, axis=1)
                min_idx = np.argmin(absolute_deltas)
                closest_delta = deltas[min_idx]
                self.controller.move_mouse_delta_modified(closest_delta)
