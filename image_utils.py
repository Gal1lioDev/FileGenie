import io

from PIL import Image

from config import JPEG_QUALITY
from config import RESIZE_FACTOR


class ImageProcessor:

    @staticmethod
    def compress(image_path):

        with Image.open(image_path) as img:

            new_size = (
                int(img.width * RESIZE_FACTOR),
                int(img.height * RESIZE_FACTOR)
            )

            img = img.resize(new_size, Image.LANCZOS)

            buffer = io.BytesIO()

            img.save(
                buffer,
                format="JPEG",
                quality=JPEG_QUALITY,
                optimize=True
            )

            return buffer.getvalue()

    @staticmethod
    def read(path):

        with open(path, "rb") as file:
            return file.read()