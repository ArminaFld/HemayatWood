from fastapi import FastAPI, File, UploadFile, HTTPException
import shutil
import os

app = FastAPI()

UPLOAD_FOLDER = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_size = len(await file.read())
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds the allowed limit of 10 MB")

    file_location = f"{UPLOAD_FOLDER}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "location": file_location}

@app.get("/files/{filename}")
async def get_file(filename: str):
    file_location = f"{UPLOAD_FOLDER}/{filename}"
    if os.path.exists(file_location):
        return {"file_location": file_location}
    else:
        raise HTTPException(status_code=404, detail="File not found")

@app.delete("/files/{filename}")
async def delete_file(filename: str):
    file_location = f"{UPLOAD_FOLDER}/{filename}"
    if os.path.exists(file_location):
        os.remove(file_location)
        return {"message": f"File {filename} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="File not found")
