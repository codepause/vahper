import numpy as np

from epta.core import ConfigDependent
from epta.tools.renderers import BaseRenderer

from .bbox_renderer import BBoxRenderer
from .image_renderer import ImageRendererMP


class SingleRenderer(BaseRenderer, ConfigDependent):
    def __init__(self, config: 'Config', name='single_renderer', key: str = None, **kwargs):
        super(SingleRenderer, self).__init__(config=config, name=name, **kwargs)
        self.bbox_renderer = BBoxRenderer(config, **kwargs)
        self.image_renderer = ImageRendererMP(config, key=key, **kwargs)

    @staticmethod
    def prepare_data(data: dict):
        orig_image = data['image']
        image = np.concatenate(
            [
                np.ones((*orig_image.shape[:2], 1), dtype=np.uint8) * 252,
                np.zeros((*orig_image.shape[:2], 1), dtype=np.uint8),
                np.zeros((*orig_image.shape[:2], 1), dtype=np.uint8)
            ],
            axis=-1
        )
        bboxes = data['bboxes']
        return image, bboxes

    def render(self, data: dict, state: int = 0):
        image, bboxes = self.prepare_data(data)
        bboxes_image = self.bbox_renderer.render(image, bboxes, state=state)
        self.image_renderer.render(bboxes_image)

    def set_state(self, state: int):
        self.bbox_renderer.state = state

    def start(self):
        self.image_renderer.start()

    def join(self):
        self.image_renderer.join()
