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
from sklearn.decomposition import PCA

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def get_text_embedding(query: str):
    inputs = processor(text=query, return_tensors="pt", padding=True)
    with torch.no_grad():
        text_features = model.get_text_features(**inputs)
    text_embedding = text_features.squeeze().cpu().numpy()
    print(f"Text embedding for query '{query}': {text_embedding}")
    return text_embedding

def pad_embedding(embedding, target_dim):
    # Nếu kích thước embedding đã bằng target_dim, trả về chính nó
    if embedding.shape[0] == target_dim:
        return embedding
    # Nếu kích thước nhỏ hơn target_dim, thêm các số 0 vào cuối embedding
    elif embedding.shape[0] < target_dim:
        padded_embedding = np.zeros(target_dim)
        padded_embedding[:embedding.shape[0]] = embedding
        return padded_embedding
    else:
        # Nếu embedding lớn hơn target_dim, bạn có thể giảm kích thước hoặc xử lý khác
        raise ValueError(f"Embedding size exceeds target dimension: {embedding.shape[0]} > {target_dim}")

def reduce_embedding(embedding, target_dim=512):
    # Nếu embedding là vector 1D, chuyển đổi thành mảng 2D
    if len(embedding.shape) == 1:
        print(f"Skipping PCA: embedding is 1D with shape {embedding.shape}")
        # Chuyển đổi thành mảng 2D với một hàng
        return embedding.reshape(1, -1)

    n_samples, n_features = embedding.shape
    
    if n_features <= target_dim:
        print(f"No need for PCA: embedding shape {embedding.shape} is already less than or equal to target_dim")
        return embedding
    
    if n_samples < target_dim:
        print(f"Warning: PCA cannot be applied because n_samples={n_samples} is less than target_dim={target_dim}")
        return embedding

    # Áp dụng PCA để giảm chiều
    pca = PCA(n_components=target_dim)
    reduced_embedding = pca.fit_transform(embedding)
    return reduced_embedding


app = FastAPI()

try:
    client = MongoClient("mongodb+srv://Milkyway2904:dat29042004@aic2024.jy2so.mongodb.net/")
    db = client["AIC2024"]
    fs = GridFS(db)
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

def find_videos_by_embedding(query_embedding, threshold=0.3, limit=50):
    results = []
    query_embedding = pad_embedding(query_embedding, target_dim=512)

    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        videos = list(collection.find({}).limit(limit))
        for video in videos:
            gridfs_id = video.get('gridfs_id')
            if gridfs_id:
                try:
                    file = fs.get(ObjectId(gridfs_id))
                    file_data = file.read()
                    video_embedding = np.frombuffer(file_data, dtype=np.float32)
                    video_embedding = reduce_embedding(video_embedding, target_dim=512)
                    if query_embedding.shape != video_embedding.shape:
                        print(f"Size mismatch: query embedding {query_embedding.shape}, video embedding {video_embedding.shape}")
                        continue
                    
                    print(f"Video embedding for {video.get('title', 'Unknown')}: {video_embedding}")
                    similarity = np.dot(query_embedding, video_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(video_embedding))
                    print(f"Similarity: {similarity} for video {video.get('title', 'Unknown')}")
                    
                    if similarity >= threshold:
                        video["_id"] = str(video["_id"])
                        results.append(video)
                except Exception as e:
                    print(f"Error loading embedding for video: {video.get('title', 'Unknown')} (ID: {video['_id']}), Error: {str(e)}")
    
    return results


@app.get("/", response_class=HTMLResponse)
async def root(request: Request, skip: int = 0, limit: int = 10):
    try:
        all_videos = []
        for collection_name in db.list_collection_names():
            collection = db[collection_name]
            videos = list(collection.find({}).skip(skip).limit(limit))
            for video in videos:
                video["_id"] = str(video["_id"])
                video['thumbnail_url'] = video.get('thumbnail_url', '')
                video['watch_url'] = video.get('watch_url', '')
                all_videos.append(video)
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
            for video in video_docs:
                video["_id"] = str(video["_id"])
                all_videos.append(video)

        return {"videos": all_videos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving videos: {str(e)}")

@app.post("/search_by_embedding", response_model=VideosResponse)
async def search_by_embedding(request: Request):
    try:
        request_data = await request.json()
        query_embedding = np.array(request_data.get('query_embedding'))
        threshold = request_data.get('threshold', 0.3)
        limit = request_data.get('limit', 50)
        
        results = find_videos_by_embedding(query_embedding, threshold, limit)
        
        if not results:
            raise HTTPException(status_code=404, detail="No videos found matching the query.")
        
        return {"videos": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching videos by embedding: {str(e)}")

@app.get("/get_embedding")
async def get_embedding(query: str):
    try:
        embedding = get_text_embedding(query)
        return JSONResponse(content=embedding.tolist())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating embedding: {str(e)}")
