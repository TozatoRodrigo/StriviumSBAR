import io
from uuid import uuid4

from fastapi import UploadFile
from PIL import Image, ImageOps

from app.filesystem.filesystem import Filesystem
from app.utils.string import slugify


class Upload:
    def __init__(self, filesystem: Filesystem) -> None:
        self.filesystem = filesystem

    def upload(self, folder: str, file: UploadFile) -> str:
        file.file.seek(0)
        if self.__is_image(file):
            file = self.__compress_image(file)

        file_name_slug = slugify(self.__get_file_name(file))
        file_extension = self.__get_file_extension(file)
        filename = f"{uuid4()}-{file_name_slug}.{file_extension}"

        path = f"{folder}/{filename}"
        self.filesystem.put(path, file.file.read())

        return path

    @staticmethod
    def __get_file_extension(file: UploadFile) -> str:
        return file.filename.split(".")[-1]

    @staticmethod
    def __get_file_name(file: UploadFile) -> str:
        return file.filename.split(".")[0]

    @staticmethod
    def __is_image(file: UploadFile) -> bool:
        return file.filename.endswith((".png", ".jpg", ".jpeg"))

    @staticmethod
    def __compress_image(file: UploadFile) -> UploadFile:
        try:
            image = Image.open(file.file)
            image = ImageOps.exif_transpose(image)
            if image.mode in {"RGBA", "P"}:
                image = image.convert("RGB")

            output = io.BytesIO()
            image.save(output, format="WEBP", quality=85, optimize=True)
            output.seek(0)
            original_name = Upload.__get_file_name(file)
            file_name = f"{original_name}.webp"

            return UploadFile(filename=file_name, file=output)
        except Exception:
            file.file.seek(0)
            return file
