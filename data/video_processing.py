import os
import cv2
import numpy as np

def process_video(keyframe_dir, labels_dict=None):
    X_data = []
    y_data = []
    
    for video_folder in os.listdir(keyframe_dir):
        video_path = os.path.join(keyframe_dir, video_folder)
        for frame_file in os.listdir(video_path):
            frame_path = os.path.join(video_path, frame_file)
            image = cv2.imread(frame_path)
            
            image = cv2.resize(image, (224, 224))
            X_data.append(image)
            
            if labels_dict:
                label = labels_dict.get(frame_file, 0)
                y_data.append(label)
            else:
                y_data.append(0)
    
    return np.array(X_data), np.array(y_data)

def process_keyframes(base_dir, labels_dict=None):
    X_data = []
    y_data = []
    
    for i in range(1, 13):
        keyframe_dir = os.path.join(base_dir, f"keyframe_L{i:02d}")
        X, y = process_video(keyframe_dir, labels_dict)
        X_data.append(X)
        y_data.append(y)
    
    X_data = np.concatenate(X_data, axis=0)
    y_data = np.concatenate(y_data, axis=0)
        
    return X_data, y_data