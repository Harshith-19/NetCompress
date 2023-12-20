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

@app.options("/upload/")
async def options_upload():
    return {"message": "Allowed"}

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

def remove_uploaded_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)

@app.post("/upload/")

async def upload_file(file: UploadFile = File(...), fileType: str = Form(...)):
    try:
        file_path = await save_upload_file(file)
        result = []

        if fileType == "Text":
            result = main_text(file_path)
        elif fileType == "Image":
            result = main_image(file_path)
        elif fileType == "Audio":
            result = main_audio(file_path)
        elif fileType == "Video":
            result = main_video(file_path)
        elif fileType == "Real time text":
            result = main_real(file_path)
        elif fileType == "Mixed data":
            result = main_mixed(file_path)
        elif fileType == "Data dump":
            result = main_data(file_path)
        else:
            result = [{"message": "Type not found"}]

        # Extract compression ratio and paths from the result
        compression_ratios = [algo.get("compression_ratio", 0) for algo in result]
        max_compression_ratio = max(compression_ratios, default=0)

        # Remove files with compression ratio less than max
        for algo in result:
            if algo.get("compression_ratio", 0) < max_compression_ratio:
                compressed_path = algo.get("compressed_file_path", "")
                reconstructed_path = algo.get("reconstructed_file_path", "")
                if compressed_path and os.path.exists(compressed_path):
                    os.remove(compressed_path)
                if reconstructed_path and os.path.exists(reconstructed_path):
                    os.remove(reconstructed_path)

        return result

    finally:
        remove_uploaded_file(file_path)


        

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

