from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List

app = FastAPI()

try:
    client = MongoClient("mongodb+srv://Milkyway2904:dat29042004@aic2024.jy2so.mongodb.net/")
    db = client["AIC2024"]
    print("Connected to MongoDB")
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error connecting to MongoDB: {str(e)}")

templates = Jinja2Templates(directory="webapp/templates")
app.mount("/static", StaticFiles(directory="webapp/static"), name="static")

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
        all_videos = []
        for collection_name in db.list_collection_names():
            collection = db[collection_name]
            videos = list(collection.find({}))
            all_videos.extend(videos)
        for video in all_videos:
            video["_id"] = str(video["_id"])
            video['thumbnail_url'] = video.get('thumbnail_url', '')
            video['watch_url'] = video.get('watch_url', '')
        return templates.TemplateResponse("page_DWB.html", {"request": request, "videos": all_videos})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving videos: {str(e)}")

@app.get("/videos", response_model=VideosResponse)
async def get_videos(skip: int = 0, limit: int = 10):
    try:
        all_videos = []
        for collection_name in db.list_collection_names():
            collection = db[collection_name]
            video_docs = collection.find().skip(skip).limit(limit)
            videos = [video for video in video_docs]
            all_videos.extend(videos)
        for video in all_videos:
            video["_id"] = str(video["_id"])

        return {"videos": all_videos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving videos: {str(e)}")

@app.get("/search", response_model=VideosResponse)
async def search_video(query: str):
    try:
        all_videos = []
        for collection_name in db.list_collection_names():
            collection = db[collection_name]
            video_docs = collection.find({"title": {"$regex": query, "$options": "i"}})
            videos = [video for video in video_docs]
            all_videos.extend(videos)

        for video in all_videos:
            video["_id"] = str(video["_id"])

        return {"videos": all_videos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching videos: {str(e)}")
