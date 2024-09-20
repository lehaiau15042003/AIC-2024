from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb+srv://Milkyway2904:dat29042004@aic2024.jy2so.mongodb.net/")
db = client["AIC2024"]

# Truy vấn fs.files để kiểm tra sự tồn tại của file với gridfs_id
def check_file_exists_in_gridfs(gridfs_id):
    file = db.fs.files.find_one({"_id": ObjectId(gridfs_id)})
    if file:
        print(f"File found in GridFS with ID: {gridfs_id}")
        print(file)  # In ra metadata của file
    else:
        print(f"No file found in GridFS with ID: {gridfs_id}")

# Kiểm tra một ObjectId cụ thể
check_file_exists_in_gridfs("66d852bc13e62f18ca61de0e")
