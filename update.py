from pymongo import MongoClient
from gridfs import GridFS
import os
import numpy as np

client = MongoClient("mongodb+srv://Milkyway2904:dat29042004@aic2024.jy2so.mongodb.net/")
db = client['AIC2024']
grid_fs = GridFS(db)
metadata_collection = db['Video2']

embedding_folder = "E:/data/CLIP features (ViT-B32)/CLIP_2"
documents = metadata_collection.find({})

for doc in documents:
    filename_DB = doc.get('filename')
    for filename in os.listdir(embedding_folder):
        if filename.endswith("L02_V026.npy"): 
            if filename_DB in filename:
                file_path = os.path.join(embedding_folder, filename)
                
                try:
                    data = np.load(file_path)
                    
                    with open(file_path, 'rb') as f:
                        grid_fs_id = grid_fs.put(f, filename=filename, content_type='application/octet-stream')

                    print(f'Uploaded {filename} with GridFS ID: {grid_fs_id}')
                    
                    metadata_collection.update_one({"_id": doc["_id"]}, {"$set": {"gridfs_id": grid_fs_id}})
                    
                    break
                except Exception as e:
                    print(f"Error processing file {filename}: {str(e)}")
