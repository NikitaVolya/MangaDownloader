from downloaders.strategies import DownloadStrategy
from PIL import Image
import os


class MergeFramesStrategy(DownloadStrategy):

    def Execute(self, path: str):

        files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith((".png", ".jpg", ".jpeg"))]
        files.sort(key=lambda f: os.path.getctime(f))

        if not files:
            return

        images = [Image.open(f) for f in files]

        width = images[0].width
        total_height = sum(img.height for img in images)

        result = Image.new("RGB", (width, total_height))
        y_offset = 0
        for img in images:
            result.paste(img, (0, y_offset))
            y_offset += img.height
        result.save(os.path.join(path, "merged.jpg"))

        for f in files:
            try:
                os.remove(f)
            except Exception as e:
                print(f"Не вдалося видалити {f}: {e}")