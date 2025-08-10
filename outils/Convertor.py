
from PIL import Image as PILImage

import numpy as np

from pytoshop.user.nested_layers import Image as PSDImage, nested_layers_to_psd
from pytoshop.enums import ColorMode, BlendMode


class Convertor:


    @staticmethod
    def SavePageAsPSD(image_path: str, output_path: str):

        img = PILImage.open(image_path).convert('RGBA')
        arr = np.array(img)
        h, w = arr.shape[:2]

        channels = {0: arr[..., 0], 1: arr[..., 1], 2: arr[..., 2], -1: arr[..., 3]}

        origin_layer = PSDImage(
            name='Origin',
            visible=True,
            opacity=255,
            group_id=0,
            blend_mode=BlendMode.normal,
            top=0, left=0,
            bottom=h, right=w,
            channels=channels,
            metadata=None,
            layer_color=0,
            color_mode=ColorMode.rgb
        )

        clean_layer = PSDImage(
            name='To clean',
            visible=True,
            opacity=255,
            group_id=0,
            blend_mode=BlendMode.normal,
            top=0, left=0,
            bottom=h, right=w,
            channels=channels,
            metadata=None,
            layer_color=0,
            color_mode=ColorMode.rgb
        )

        psd = nested_layers_to_psd([clean_layer, origin_layer], color_mode=ColorMode.rgb, size=(w, h), compression=0)

        with open(output_path, 'wb') as f:
            psd.write(f)