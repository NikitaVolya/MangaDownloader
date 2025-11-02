
from downloaders.strategies.DownloadStrategy import DownloadStrategy

import os, img2pdf
from PIL import Image


class SavePDFStrategy(DownloadStrategy):


    def Execute(self, path: str):

        name = os.path.basename(path)

        output_path = os.path.join(path, f"{name}.pdf")

        saving_images = []
        tmp_images = []

        print(f"Saving PDF ({name})")

        files = [file for file in os.listdir(path) if file.lower().endswith((".jpg", ".png"))]
        files.sort(
            key=lambda name: int(name.replace(".jpg", "").replace(".png", "")),
        )

        for file in files:
            full_path = os.path.join(path, file)

            with Image.open(full_path) as image:
                if image.mode in ("RGBA", "LA"):
                    background = Image.new("RGB", image.size, (255, 255, 255))
                    background.paste(image, mask=image.getchannel("A"))
                    image = background
                    tmp_path = os.path.splitext(full_path)[0] + "_noalpha.jpg"
                    image.save(tmp_path, "JPEG", dpi=(300, 300))
                    full_path = tmp_path

                    tmp_images.append(tmp_path)

            saving_images.append(full_path)

        with open(output_path, "wb") as f:
            data = img2pdf.convert(saving_images)
            f.write(data)

        for tmp_image in tmp_images:
            os.remove(tmp_image)
