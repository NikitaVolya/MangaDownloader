
from downloaders.strategies.DownloadStrategy import DownloadStrategy

import os, img2pdf
from PIL import Image


class SavePDFStrategy(DownloadStrategy):


    def Execute(self, path: str):

        files = os.listdir(path)
        for file in files:
            if file.lower().endswith((".jpg", ".png")):
                full_path = os.path.join(path, file)

                with Image.open(full_path) as image:
                    if image.mode in ("RGBA", "LA"):
                        background = Image.new("RGB", image.size, (255, 255, 255))
                        background.paste(image, mask=image.getchannel("A"))
                        image = background
                        tmp_path = os.path.splitext(full_path)[0] + "_noalpha.jpg"
                        image.save(tmp_path, "JPEG")
                        full_path = tmp_path

                pdf_bytes = img2pdf.convert(full_path)

                file_name = os.path.splitext(file)[0]
                output_path = os.path.join(path, f"{file_name}.pdf")

                with open(output_path, "wb") as f:
                    f.write(pdf_bytes)