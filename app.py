from fastapi import FastAPI, Request, File, UploadFile, Header
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from pathlib import Path

app = FastAPI()

templates = Jinja2Templates(directory="webapp/templates")
app.mount("/static", StaticFiles(directory="webapp/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("base.html", {"request":request})

@app.post("/upload")
async def upload_video(    
    request : Request,
    page_id : str,
    file : UploadFile = File(...),
    access_token : str = Header(...),
    ):
    
    file_location = Path("webapp/static/upload")
    
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    
    return JSONResponse(content={"filename": file.filename, "location": str(file_location)})