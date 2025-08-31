from downloaders.strategies import DownloadStrategy
from PIL import Image
import os


class MergeFramesStrategy(DownloadStrategy):

    def __init__(self, save_original):
        self.__save_original = save_original

    def Execute(self, path: str):

        files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith((".png", ".jpg", ".jpeg"))]
        files.sort(key=lambda f: os.path.getctime(f))

        if not files:
            return

        images = [Image.open(f) for f in files]

        global_width = max(images, key=lambda i: i.width).width
        total_height = sum(img.height for img in images)

        result = Image.new("RGBA", (global_width, total_height))
        y_offset = 0
        for img in images:

            current_x_pos = (global_width - img.width) // 2

            result.paste(img, (current_x_pos, y_offset))
            y_offset += img.height
        result.save(os.path.join(path, "merged.png"))

        if not self.__save_original:
            for f in files:
                try:
                    os.remove(f)
                except Exception as e:
                    print(f"Не вдалося видалити {f}: {e}")