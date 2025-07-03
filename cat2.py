"""
from moviepy.editor import VideoFileClip

print("moviepy is working!")

from fer import FER
import cv2
import matplotlib.pyplot as plt

# Load image
img = cv2.imread("C:\\Aicat2\\generatest2.jpg")

# Create detector
detector = FER(mtcnn=True)

# Detect emotions
results = detector.detect_emotions(img)

# Show emotions
for result in results:
    bounding_box = result["box"]
    emotion = result["emotions"]
    dominant_emotion = max(emotion, key=emotion.get)
    
    x, y, w, h = bounding_box
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(img, dominant_emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

# Show image
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.show()
"""
from fer import FER
import cv2
import os

def predict_emotion(image_path):
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        return "Could not load image"

    # Create FER detector
    detector = FER(mtcnn=True)

    # Detect emotions
    results = detector.detect_emotions(img)

    if not results:
        return "No face detected"

    # Take first face result
    dominant_emotion = max(results[0]["emotions"], key=results[0]["emotions"].get)
    return dominant_emotion
