from datetime import datetime
from struct import pack

from PIL import Image


timestamp_format = '<Q'
translation_format = '<ddd'
rotation_format = '<dddd'
height_format = '<I'
width_format = '<I'
pixel_format = '<f'
feelings_format = '<ffff'


class Snapshot:
    def __init__(self, timestamp: datetime, translation, rotation, color_image: Image.Image, depth_image: Image.Image, feelings):
        self.timestamp = timestamp
        self.translation = translation
        self.rotation = rotation
        self.color_image = color_image
        self.depth_image = depth_image
        self.feelings = feelings

    def serialize(self):
        return pack(timestamp_format, int(self.timestamp.timestamp() * 1000)) \
            + pack(translation_format, *self.translation) \
            + pack(rotation_format, self.rotation) \
            + self.color_image.tobytes() \
            + self.depth_image.tobytes() \
            + pack(feelings_format, *self.feelings)
