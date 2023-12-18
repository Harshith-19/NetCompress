from pydantic import BaseModel

class FileRequest(BaseModel):
    filePath: str
    fileType: str