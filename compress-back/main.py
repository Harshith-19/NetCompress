from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from Compression.audio import main_audio
from Compression.data import main_data
from Compression.image import main_image
from Compression.mixed import main_mixed
from Compression.real import main_real
from Compression.text import main_text
from Compression.video import main_video
import shutil
import os


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

async def save_upload_file(upload_file: UploadFile) -> str:
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    file_location = os.path.join(upload_dir, upload_file.filename)
    with open(file_location, "wb") as file_object:
        shutil.copyfileobj(upload_file.file, file_object)
    
    return file_location


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), fileType: str = Form(...)):
    file_path = await save_upload_file(file)

    file_path = file_path
    file_type = fileType

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
