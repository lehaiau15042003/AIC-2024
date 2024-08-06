from fastapi import FastAPI, Request, File, UploadFile, Header, requests, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from pydantic import BaseModel
from pathlib import Path
from PIL import Image
import base64
from io import BytesIO
import shutil

app = FastAPI()

class FileUpload(BaseModel):
    fileName: str
    fileType: str
    fileContent: str

templates = Jinja2Templates(directory="webapp/templates")
app.mount("/static", StaticFiles(directory="webapp/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("base.html", {"request":request})


@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("page_upload.html", {"request":request})

@app.get("/upload/result", response_class=HTMLResponse)
async def upload_result(request: Request, file_url: str):
    return templates.TemplateResponse("page_result.html", {"request":request, "file_url": file_url})
    
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        upload_dir = Path("./upload")
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / file.filename
        
        with file_path.open("wb") as f:
            shutil.copyfileobj(file.file, f)

        file_url = f"/static/upload/{file.filename}"
        return RedirectResponse(url=f"/upload/result?file_url={file_url}", status_code=303)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")