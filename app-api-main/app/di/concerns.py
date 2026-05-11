from typing import Annotated

from fastapi import Depends

from app.concerns.upload import Upload
from app.di.filesystems import get_filesystem
from app.filesystem.filesystem import Filesystem


def get_upload(filesystem: Annotated[Filesystem, Depends(get_filesystem)]) -> Upload:
    return Upload(filesystem)
