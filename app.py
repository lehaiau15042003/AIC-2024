from fastapi import FastAPI, Request, File, UploadFile, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from pathlib import Path
from PIL import Image
import numpy as np
from typing import List
import shutil
import torch
import torchvision.transforms as T
import torchvision.models.detection as detection
import clip
import cv2
from pydantic import BaseModel

app = FastAPI()

device = "cuda" if torch.cuda.is_available() else "cpu"

model, preprocess = clip.load("ViT-B/32", device=device)
faster_rcnn_model = detection.fasterrcnn_resnet50_fpn(pretrained=True)
faster_rcnn_model.to(device).eval()

frames = 30

class Prediction(BaseModel):
    predictions: List[str]

templates = Jinja2Templates(directory="webapp/templates")
app.mount("/static", StaticFiles(directory="webapp/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("page_DWB.html", {"request": request})

@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("page_upload.html", {"request": request})

@app.get("/upload/result", response_class=HTMLResponse)
async def upload_result(request: Request, file_url: str, predictions: str = " "):
    return templates.TemplateResponse("page_result.html", {"request": request, "file_url": file_url, "predictions": predictions})

def resize_frame(frame, scale_percent=50):
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    return resized_frame


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        upload_dir = Path("webapp/static/upload")
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / file.filename
        
        with file_path.open("wb") as f:
            shutil.copyfileobj(file.file, f)

        file_url = f"/static/upload/{file.filename}"
        predict_response = await predict(file_path)
        predictions = predict_response.predictions
        predictions_str = ', '.join(predictions)
        
        return RedirectResponse(url=f"/upload/result?file_url={file_url}&predictions={predictions_str}", status_code=303)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")

@app.post("/predict")
async def predict(file_path: str):
    try:
        cap = cv2.VideoCapture(file_path)
        descriptions = ["cat", "dog", "person", "smartphone", "motorbike", "bird"]
        text_inputs = clip.tokenize(descriptions).to(device)
        
        all_prediction = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            if frame_number % frames != 0:
                continue
            
            frame = resize_frame(frame, scale_percent=50)
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            image_input = preprocess(image).unsqueeze(0).to(device)
            
            with torch.no_grad():
                image_features = model.encode_image(image_input)
                text_features = model.encode_text(text_inputs)
                
                similarity = torch.matmul(image_features, text_features.T)
                probs = similarity.softmax(dim=-1).cpu().numpy()
            
            frame_predictions = [descriptions[i] for i in range(len(descriptions)) if probs[0][i] > 0.5]
            if frame_predictions:
                all_prediction.extend(frame_predictions)
        
        cap.release()
        
        unique_predictions = list(set(all_prediction))              
        return Prediction(predictions=unique_predictions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {e}")