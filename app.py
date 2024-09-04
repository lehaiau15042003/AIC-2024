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
# from pydantic import BaseModel
# from pymongo import MongoClient
# from pymongo.collection import Collection


app = FastAPI()

# client = MongoClient("mongodb://localhost:27017/")
# db = client["AIC2024"] 
# videos_collection: Collection = db["Video"]

templates = Jinja2Templates(directory="webapp/templates")
app.mount("/static", StaticFiles(directory="webapp/static"), name="static")
app.mount("/videos", StaticFiles(directory="webapp/static/videos"), name="videos")

# class VideoMetadata(BaseModel):
#     author: str
#     channel_id: str
#     channel_url: str
#     description: str
#     keywords: List[str]
#     length: int
#     publish_date: str
#     thumbnail_url: str
#     title: str
#     watch_url: str

# class VideosResponse(BaseModel):
#     videos: List[VideoMetadata]

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    video_folder = Path("webapp/static/videos")
    if not video_folder.exists():
        raise HTTPException(status_code=404, detail="Video folder not found")
    video_files = [f.name for f in video_folder.glob("*.mp4") if f.is_file()]
    print("Video files:", video_files)  
    return templates.TemplateResponse("page_DWB.html", {"request": request, "videos": video_files})

# @app.get("/videos")
# async def get_videos():
#     try:
#         video_docs = videos_collection.find()
#         videos = []
#         for video in video_docs:
#             video["_id"] = str(video["_id"])
#             videos.append(video)
#         return JSONResponse(content={"videos": videos})
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error retrieving videos: {str(e)}")

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
