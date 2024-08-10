from fastapi import FastAPI, Request, File, UploadFile, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from pathlib import Path
from PIL import Image
import numpy as np
import os
import shutil
import torch
import clip
import io

app = FastAPI()

templates = Jinja2Templates(directory="webapp/templates")
app.mount("/static", StaticFiles(directory="webapp/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("page_upload.html", {"request": request})

@app.get("/upload/result", response_class=HTMLResponse)
async def upload_result(request: Request, file_url: str):
    return templates.TemplateResponse("page_result.html", {"request": request, "file_url": file_url})
    
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        upload_dir = Path("webapp/static/upload")
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / file.filename
        
        with file_path.open("wb") as f:
            shutil.copyfileobj(file.file, f)

        file_url = f"/static/upload/{file.filename}"
        return RedirectResponse(url=f"/upload/result?file_url={file_url}", status_code=303)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        model, preprocess = clip.load("ViT-B/32", device='cpu')
        
        image = Image.open(io.BytesIO(await file.read()))
        image = preprocess(image).unsqueeze(0)
        
        text_inputs = torch.cat([clip.tokenize(f"a photo of a {x}") for x in ["cat", "dog"]])
        with torch.no_grad():
            image_features = model.encode_image(image)
            text_features = model.encode_text(text_inputs)
            
            image_features /= image_features.norm(dim=-1, keepdim=True)
            text_features /= text_features.norm(dim=-1, keepdim=True)
            silimarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
            
        result = {
            "similiarity": silimarity.tolist()
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, details=f"Error during prediction: {e}")
        
        