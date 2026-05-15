import io
from uuid import uuid4

from fastapi import UploadFile, status
from PIL import Image, ImageOps

from app.core.environment import envs
from app.exceptions.client_aware_error import ClientAwareError
from app.filesystem.filesystem import Filesystem
from app.utils.string import slugify

INVALID_FILENAME_MESSAGE = "Nome de arquivo inválido"
INVALID_EXTENSION_MESSAGE = "Extensão de arquivo não permitida"
INVALID_MIME_TYPE_MESSAGE = "Tipo de arquivo não permitido"
FILE_TOO_LARGE_MESSAGE = "Arquivo excede o limite de tamanho permitido"


class Upload:
    def __init__(self, filesystem: Filesystem) -> None:
        self.filesystem = filesystem
        self.max_file_size_bytes = max(envs.UPLOAD_MAX_FILE_SIZE_MB, 1) * 1024 * 1024
        self.allowed_extensions = {
            extension.strip().lower()
            for extension in envs.UPLOAD_ALLOWED_EXTENSIONS.split(",")
            if extension.strip()
        }
        self.allowed_mime_types = {
            mime_type.strip().lower()
            for mime_type in envs.UPLOAD_ALLOWED_MIME_TYPES.split(",")
            if mime_type.strip()
        }

    def upload(self, folder: str, file: UploadFile) -> str:
        file.file.seek(0)
        self.__validate_file(file)
        if self.__is_image(file):
            file = self.__compress_image(file)

        file_name_slug = slugify(self.__get_file_name(file))
        file_extension = self.__get_file_extension(file).lower()
        filename = f"{uuid4()}-{file_name_slug}.{file_extension}"

        path = f"{folder}/{filename}"
        self.filesystem.put(path, file.file.read())

        return path

    def __validate_file(self, file: UploadFile) -> None:
        if not file.filename or "." not in file.filename:
            message = INVALID_FILENAME_MESSAGE
            raise ClientAwareError(
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        file_extension = self.__get_file_extension(file).lower()
        if file_extension not in self.allowed_extensions:
            message = INVALID_EXTENSION_MESSAGE
            raise ClientAwareError(
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        if (
            not file.content_type
            or file.content_type.lower() not in self.allowed_mime_types
        ):
            message = INVALID_MIME_TYPE_MESSAGE
            raise ClientAwareError(
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        file_size = self.__get_file_size(file)
        if file_size > self.max_file_size_bytes:
            message = FILE_TOO_LARGE_MESSAGE
            raise ClientAwareError(
                message,
                status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            )

    @staticmethod
    def __get_file_size(file: UploadFile) -> int:
        current_position = file.file.tell()
        file.file.seek(0, io.SEEK_END)
        file_size = file.file.tell()
        file.file.seek(current_position)
        return file_size

    @staticmethod
    def __get_file_extension(file: UploadFile) -> str:
        return file.filename.split(".")[-1]

    @staticmethod
    def __get_file_name(file: UploadFile) -> str:
        return file.filename.split(".")[0]

    @staticmethod
    def __is_image(file: UploadFile) -> bool:
        file_extension = file.filename.lower()
        return file_extension.endswith((".png", ".jpg", ".jpeg", ".webp"))

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

            return UploadFile(
                filename=file_name, file=output, content_type="image/webp"
            )
        except Exception:
            file.file.seek(0)
            return file
