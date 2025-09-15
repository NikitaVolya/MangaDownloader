from downloaders.strategies import DownloadStrategy
from PIL import Image
import os


class MergeFramesStrategy(DownloadStrategy):

    def __init__(self, save_original: bool = False, max_size: int = 25000):
        self.__save_original: bool = save_original
        self.__max_height: int = max_size

    @staticmethod
    def MergeFiles(files: list[Image.Image], path: str, max_height: int):
        global_width = max(img.width for img in files)
        total_height = sum(img.height for img in files)

        result_height = min(total_height, max_height)
        result = Image.new("RGBA", (global_width, result_height))

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

        images = [Image.open(f) for f in files]
        current_stack = []
        current_height = 0
        page_index = 0

        for img in images:
            y_offset = 0
            while y_offset < img.height:
                available = self.__max_height - current_height
                remaining = img.height - y_offset

                if remaining <= available:
                    cropped = img.crop((0, y_offset, img.width, y_offset + remaining))
                    current_stack.append(cropped)
                    current_height += remaining
                    y_offset += remaining
                else:
                    cropped = img.crop((0, y_offset, img.width, y_offset + available))
                    current_stack.append(cropped)
                    y_offset += available

                    out_path = os.path.join(path, f"merge_{page_index}.png")
                    self.MergeFiles(current_stack, out_path, self.__max_height)
                    page_index += 1
                    current_stack = []
                    current_height = 0

        if current_stack:
            out_path = os.path.join(path, f"merge_{page_index}.png")
            self.MergeFiles(current_stack, out_path, self.__max_height)

        if not self.__save_original:
            for f in files:
                try:
                    os.remove(f)
                except Exception as e:
                    print(f"Не вдалося видалити {f}: {e}")