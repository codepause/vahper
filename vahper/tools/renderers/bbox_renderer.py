import cv2 as cv
import numpy as np

from epta.tools.renderers import BaseRenderer


class BBoxRenderer(BaseRenderer):
    def __init__(self, name='bbox_renderer', **kwargs):
        super(BBoxRenderer, self).__init__(name=name, **kwargs)

    @staticmethod
    def render(image: np.ndarray, bboxes: list, state: int = 0, **kwargs):
        if state:
            if state >= 1:
                for pose in bboxes:
                    if pose.head_center is not None:
                        cv.circle(image, pose.head_center, 3, (0, 0, 255), thickness=2)

            if state >= 2:
                for pose in bboxes:
                    pose.draw(image)

            if state >= 3:
                for pose in bboxes:
                    cv.rectangle(image, (pose.bbox[0], pose.bbox[1]),
                                 (pose.bbox[0] + pose.bbox[2], pose.bbox[1] + pose.bbox[3]), (0, 255, 0))
        return image

    def start(self, *args, **kwargs):
        pass

    def join(self, *args, **kwargs):
        pass
