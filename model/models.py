import torch
import clip
from PIL import Image
import cv2
import torchvision.transforms as transforms
from torchvision.models.detection import fasterrcnn_resnet50_fpn

device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model, preprocess = clip.load("ViT-B/32", device=device)

faster_rcnn = fasterrcnn_resnet50_fpn(pretrained=True)
faster_rcnn.eval()

def extract_frames(video_path, interval=30):
    cap = cv2.VideoCapture(video_path)
    frames = []
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % interval == 0:
            frames.append(frame)
        frame_count += 1
    cap.release()
    return frames

def detect_objects(frames):
    detected_objects = []
    for frame in frames:
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        image_tensor = preprocess(image).unsqueeze(0).to(device)
        with torch.no_grad():
            detections = faster_rcnn(image_tensor)
        detected_objects.append(detections)
    return detected_objects

def map_features_to_text(detected_objects, text_queries):
    text = clip.tokenize(text_queries).to(device)
    text_features = clip_model.encode_text(text)
    results = []
    for objects in detected_objects:
        for obj in objects[0]['boxes']:
            x1, y1, x2, y2 = map(int, obj)
            cropped_image = image.crop((x1, y1, x2, y2))
            image_tensor = preprocess(cropped_image).unsqueeze(0).to(device)
            image_features = clip_model.encode_image(image_tensor)
            similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
            results.append(similarity)
    return results

video_path = ""
frames = extract_frames(video_path)
detected_objects = detect_objects(frames)
text_queries = ["a person", "a car", "a bird", "a dog"]
results = map_features_to_text(detected_objects, text_queries)

print(results)
