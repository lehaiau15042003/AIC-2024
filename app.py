from fastapi import FastAPI, Request, File, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
import numpy as np
import os
import shutil
#import clip
import io
from typing import List
#import torch
#import torchvision.transforms as T
#import torchvision.models.detection as detection
#import cv2
#from model.models import *
import json
#from sqlalchemy import create_engine, Column, Integer, String
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker, Session


app = FastAPI()

'''DATABASE_URL = ""
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

device = "cuda" if torch.cuda.is_available() else "cpu"

model, preprocess = clip.load("ViT-B/32", device=device)
faster_rcnn_model = detection.fasterrcnn_resnet50_fpn(pretrained=True)
faster_rcnn_model.to(device).eval()

class Video(Base):
    __tablename__ = "videos",
    id = Column(Integer, primary_key=True, index=True)
    video_path = Column(String, index=True)
    thumbnail_path = Column(String)
    description = Column(String)

Base.metadata.create_all(bind=engine)'''

templates = Jinja2Templates(directory="webapp/templates")
app.mount("/static", StaticFiles(directory="webapp/static"), name="static")

'''def get_db():
    db  = SessionLocal()
    try:
        yield db
    finally:
        db.close()'''

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("page_DWB.html", {"request": request})

'''def resize_frame(frame, scale_percent=50):
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    return resized_frame

def load_video():
    file_path = Path('data/data.json')
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
    
@app.get("/search")
async def search_video(query: str, db: Session = Depends(get_db)):
    videos = db.query(Video).filter(Video.description.ilike(f"%{query}%")).all()
    video_list = [{"video_path": video.video_path, "thumbnail_path": video.thumbnail_path,} for video in videos]
    return JSONResponse(content={"videos":video_list})'''
    