from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from ..message import (
    ColorImage,
    DepthImage,
)
from ..utils import keys


class ColorImageParser:

    name = keys.color_image
    subscribe = f'raw.{keys.color_image}'
    publish = f'parsed.{keys.color_image}'

    def parse(self, color_image, img_dir: Path):
        color_image = ColorImage.from_json(color_image)
        size = color_image.width, color_image.height
        image = Image.frombytes('RGB', size, color_image.data)
        img_path = img_dir / 'color_image.jpg'
        image.save(img_path)
        ret = color_image.jsonify()
        ret['data'] = str(img_path)
        return ret


class DepthImageParser:

    def parse(self, depth_image, img_dir: Path):
        depth_image = DepthImage.from_json(depth_image)
        size = depth_image.width, depth_image.height
        data = np.array(depth_image.data).reshape(size)
        plt.imshow(data, cmap='hot', interpolation='gaussian')
        img_path = img_dir / 'depth_image.png'
        plt.savefig(img_path)
        ret = depth_image.jsonify()
        ret['data'] = str(img_path)
        return ret


def parse_feelings(feelings):
    return feelings


parse_feelings.name = keys.feelings
parse_feelings.subscribe = f'raw.{keys.feelings}'
parse_feelings.publish = f'parsed.{keys.feelings}'


def parse_pose(pose):
    return pose
