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
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.collection import Collection


app = FastAPI()
try:
    client = MongoClient("mongodb+srv://Milkyway2904:dat29042004@aic2024.jy2so.mongodb.net/")
    db = client["AIC2024"] 
    videos_collection: Collection = db["Video1"]
    print("Connected to MongoDB")
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error connecting to MongoDB: {str(e)}")


templates = Jinja2Templates(directory="webapp/templates")
app.mount("/static", StaticFiles(directory="webapp/static"), name="static")
app.mount("/videos", StaticFiles(directory="webapp/static/videos"), name="videos")

class VideoMetadata(BaseModel):
    author: str
    channel_id: str
    channel_url: str
    description: str
    keywords: List[str]
    length: int
    publish_date: str
    thumbnail_url: str
    title: str
    watch_url: str

class VideosResponse(BaseModel):
    videos: List[VideoMetadata]

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    try:
        video_docs = videos_collection.find()
        videos = [video for video in video_docs]
        for video in videos:
            video["_id"] = str(video["_id"])
        print(videos)
        return templates.TemplateResponse("page_DWB.html", {"request": request, "videos": videos})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving videos: {str(e)}")

@app.get("/videos")
async def get_videos(skip: int = 0, limit: int = 10):
    try:
        video_docs = videos_collection.find().skip(skip).limit(limit)
        videos = [video for video in video_docs]
        for video in videos:
            video["_id"] = str(video["_id"])
        return JSONResponse(content={"videos": videos})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving videos: {str(e)}")

@app.get("/search", response_model=VideosResponse)
async def search_video(query: str):
    try:
        video_docs = videos_collection.find({"title": {"$regex": query, "$options": "i"}})
        videos = []
        for video in video_docs:
            video["_id"] = str(video["_id"])
            videos.append(video)
        return JSONResponse(content={"videos": videos})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching videos: {str(e)}")
