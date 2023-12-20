from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import FileRequest
from Compression.audio import main_audio
from Compression.data import main_data
from Compression.image import main_image
from Compression.mixed import main_mixed
from Compression.real import main_real
from Compression.text import main_text
from Compression.video import main_video

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.options("/upload/")
async def options_upload():
    return {"message": "Allowed"}

@app.post("/upload/")
def upload_file(file_request: FileRequest):
    file_path = file_request.filePath
    file_type = file_request.fileType

    if file_type == "Text":
        return main_text(file_path)
    
    elif file_type == "Image":
        return main_image(file_path)
    
    elif file_type == "Audio":
        return main_audio(file_path)
    
    elif file_type == "Video":
        return main_video(file_path)
    
    elif file_type == "Real time text":
        return main_real(file_path)
    
    elif file_type == "Mixed data":
        return main_mixed(file_path)
    
    elif file_type == "Data dump":
        return main_data(file_path)
    
    return {"message" : "Type not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
