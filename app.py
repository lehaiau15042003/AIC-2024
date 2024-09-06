from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List
from gridfs import GridFS
import numpy as np
from bson import ObjectId
from transformers import CLIPProcessor, CLIPModel
import torch

# Khởi tạo mô hình CLIP
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Hàm lấy embedding cho văn bản
def get_text_embedding(query: str):
    inputs = processor(text=query, return_tensors="pt", padding=True)
    with torch.no_grad():
        text_features = model.get_text_features(**inputs)
    return text_features.squeeze().cpu().numpy()

app = FastAPI()

# Kết nối MongoDB và GridFS
try:
    client = MongoClient("mongodb+srv://Milkyway2904:dat29042004@aic2024.jy2so.mongodb.net/")
    db = client["AIC2024"]
    fs = GridFS(db)
    print("Connected to MongoDB")
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error connecting to MongoDB: {str(e)}")

# Thiết lập templates và static files
templates = Jinja2Templates(directory="webapp/templates")
app.mount("/static", StaticFiles(directory="webapp/static"), name="static")

# Định nghĩa schema cho video
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

# Hàm tìm kiếm dựa trên embedding
def find_videos_by_embedding(query_embedding, threshold=0.5):
    results = []
    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        videos = list(collection.find({}))
        for video in videos:
            gridfs_id = video.get('gridfs_id')
            if gridfs_id:
                try:
                    file = fs.get(ObjectId(gridfs_id))  # Lấy file từ GridFS
                    video_embedding = np.load(file)  # Tải embedding từ file
                    similarity = np.dot(query_embedding, video_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(video_embedding))
                    if similarity >= threshold:  # So sánh độ tương đồng với ngưỡng
                        video["_id"] = str(video["_id"])
                        results.append(video)
                except Exception as e:
                    print(f"Error loading embedding for video: {video['_id']}, Error: {str(e)}")
    return results

# Trang gốc hiển thị tất cả video
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    try:
        all_videos = []
        for collection_name in db.list_collection_names():
            collection = db[collection_name]
            videos = list(collection.find({}))
            for video in videos:
                video["_id"] = str(video["_id"])
                video['thumbnail_url'] = video.get('thumbnail_url', '')
                video['watch_url'] = video.get('watch_url', '')
                all_videos.append(video)
        return templates.TemplateResponse("page_DWB.html", {"request": request, "videos": all_videos})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving videos: {str(e)}")

# API lấy danh sách video
@app.get("/videos", response_model=VideosResponse)
async def get_videos(skip: int = 0, limit: int = 10):
    try:
        all_videos = []
        for collection_name in db.list_collection_names():
            collection = db[collection_name]
            video_docs = collection.find().skip(skip).limit(limit)
            for video in video_docs:
                video["_id"] = str(video["_id"])
                all_videos.append(video)

        return {"videos": all_videos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving videos: {str(e)}")

# API tìm kiếm video theo tiêu đề
@app.get("/search", response_model=VideosResponse)
async def search_video(query: str):
    try:
        all_videos = []
        for collection_name in db.list_collection_names():
            collection = db[collection_name]
            video_docs = collection.find({"title": {"$regex": query, "$options": "i"}})
            for video in video_docs:
                video["_id"] = str(video["_id"])
                all_videos.append(video)

        return {"videos": all_videos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching videos: {str(e)}")

# API tìm kiếm video theo embedding
@app.post("/search_by_embedding", response_model=VideosResponse)
async def search_by_embedding(query_embedding: List[float], threshold: float = 0.5):
    try:
        query_embedding = np.array(query_embedding)
        results = find_videos_by_embedding(query_embedding, threshold)
        return {"videos": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching videos by embedding: {str(e)}")
