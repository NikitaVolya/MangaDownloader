from downloaders.strategies import DownloadStrategy
from PIL import Image
import os


class MergeFramesStrategy(DownloadStrategy):

    def __init__(self, save_original: bool = False, max_size: int = 25000):
        self.__save_original: bool = save_original
        self.__max_height: int = max_size

    @staticmethod
    def MergeFiles(files: Image.Image, path: str):
        global_width = max(files, key=lambda i: i.width).width
        total_height = sum(img.height for img in files)

        result = Image.new("RGBA", (global_width, total_height))
        y_offset = 0
        for img in files:
            current_x_pos = (global_width - img.width) // 2

            result.paste(img, (current_x_pos, y_offset))
            y_offset += img.height
        result.save(path)

    def Execute(self, path: str):

        files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith((".png", ".jpg", ".jpeg"))]
        files.sort(key=lambda f: os.path.getctime(f))

        if not files:
            return

        sort_images = []

        images = [Image.open(f) for f in files]

        rest_height = 0
        for image in images:
            if image.height > rest_height:
                sort_images.append([image])
                rest_height = self.__max_height - image.height
            else:
                rest_height -= image.height
                sort_images[-1].append(image)

        for i, sort_image_list in enumerate(sort_images):
            self.MergeFiles(sort_image_list, os.path.join(path, f"merge_{i}.png"))

        if not self.__save_original:
            for f in files:
                try:
                    os.remove(f)
                except Exception as e:
                    print(f"Не вдалося видалити {f}: {e}")