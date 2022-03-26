import numpy as np

from .utils import init_model, image_to_bbox

from epta.tools.recognition import BaseRecogniser
from epta.core import ConfigDependent


class SkeletonRecogniser(BaseRecogniser, ConfigDependent):
    def __init__(self, config: 'Config', name: str = 'skeleton_recogniser', **kwargs):
        super(SkeletonRecogniser, self).__init__(config=config, name=name, **kwargs)
        self.model = init_model(self.config.settings.weights_path, self.config.settings.device)

    def image_to_data(self, image: np.ndarray, **kwargs) -> str:
        result = image_to_bbox(self.model, image)
        return result
