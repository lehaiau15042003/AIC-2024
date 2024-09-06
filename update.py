from pymongo import MongoClient
from gridfs import GridFS
import os
import numpy as np

client = MongoClient("mongodb+srv://Milkyway2904:dat29042004@aic2024.jy2so.mongodb.net/")
db = client['AIC2024']
grid_fs = GridFS(db)
metadata_collection = db['Video12']

embedding_folder = "E:/data/CLIP features (ViT-B32)/CLIP_12"
documents = metadata_collection.find({})
for doc in documents:
    filename_DB = doc.get('filename')
    for filename in os.listdir(embedding_folder):
        if filename.endswith(".npy"): 
            if filename_DB in filename:
                file_path = os.path.join(embedding_folder, filename)

                data = np.load(file_path)

                grid_fs_id = grid_fs.put(data.tobytes(), filename=filename, content_type='application/octet-stream')

                print(f'Uploaded {filename} with GridFS ID: {grid_fs_id}')
        
                metadata_collection.update_one({"_id": doc["_id"]}, {"$set": {"gridfs_id": grid_fs_id}})
                break