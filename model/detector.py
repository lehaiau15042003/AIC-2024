import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
from PIL import Image, ImageColor, ImageDraw, ImageFont, ImageOps

def display_image(image):
    fig = plt.figure(figsize=(20, 15))
    plt.axis('off')
    plt.imshow(image)
    
def load_image(path):
    img = tf.io.read_file(path)
    img = tf.image.decode_jpeg(img, channels=3)
    return img    

faster_rcnn_url = "https://www.kaggle.com/models/google/faster-rcnn-inception-resnet-v2/tensorFlow1/faster-rcnn-openimages-v4-inception-resnet-v2/1"
def load_model():
    detector = hub.load(faster_rcnn_url).signatures['default']
    return detector

def draw(image, max_boxes, min_score, boxes, class_names, scores):
    colors = list(ImageColor.colormap.values())
    
    try:
        font = ImageFont.truetype("arial.ttf", 25, encoding="unic")
    except IOError:
        print("Font not found. Using default font.")
        font = ImageFont.load_default()
    
    detected_boxes = boxes.shape[0]
    for i in range(min(max_boxes, detected_boxes)):
        if scores[i] >= min_score:
            ymin, xmin, ymax, xmax = tuple(boxes[i])
            display_str = "{}: {}%".format(class_names[i].decode("ascii"),
                                           int(100 * scores[i]))
            color = colors[hash(class_names[i]) % len(colors)]
            
            image_convert = Image.fromarray(np.uint8(image)).convert("RGB")
            
            save_image_with_boxes(
                image_convert,
                ymin, xmin,
                ymax, xmax,
                color, font,
                display_str_list=[display_str]
            )
            np.copyto(image, np.array(image_convert))
    return image

def save_image_with_boxes(image, boxes, class_names, scores, path):
    draw(image, boxes, class_names, scores)

def run_detector(detector, path, max_boxes, max_score):
    img = load_image(path)
    
    converted_img = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]
    print("Detecting Image ...")
    output = detector(converted_img)
    print("Detection Complete\n")
    
    for key, value in output.items():
        print(f"Key: {key} \nValue:{value}\n\n")
        
    output = {key:value.numpy() for key,value in output.items()}
    print("Found %d objects." % len(output["detection_scores"]))
    
    image_with_boxes = draw(img.numpy(),
                            max_boxes, max_score,
                            output['detection_boxes'],
                            output['detection_class_entities'],
                            output['detection_scores'])
    display_image(image_with_boxes)