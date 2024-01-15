import uuid
from pathlib import Path

from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles

ROOT_DIR = Path(__file__).parent
UPLOADED_FILES_DIR = ROOT_DIR / "uploaded-files"
UPLOADED_FILES_DIR.mkdir(parents=False, exist_ok=True)

app = FastAPI()


@app.post("/upload/")
async def upload_geo_file(mdfile: UploadFile):
    print(f"Uploaded file: {mdfile}")

    subdir = str(uuid.uuid4())
    (UPLOADED_FILES_DIR / subdir).mkdir(parents=False, exist_ok=False)
    out_file_path = UPLOADED_FILES_DIR / subdir / mdfile.filename
    # To write files async: https://stackoverflow.com/a/63581187/1969672.
    with open(out_file_path, "wb") as out_file:
        while content := await mdfile.read(1024):
            out_file.write(content)


# This mount should come after all other routes defined here.
app.mount("/", StaticFiles(directory="static", html=True), name="static")
