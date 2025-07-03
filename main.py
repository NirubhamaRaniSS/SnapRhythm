from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fer import FER
import cv2
import numpy as np
import requests
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_spotify_token():
    client_id = "b01a4d1080fa46afb3856d6a21f3580a"
    client_secret = "de47ea7ee9a64f10827f42ae6bb0d76a"
    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    return response.json().get("access_token")

@app.post("/detect_emotion/")
async def detect_emotion(file: UploadFile = File(...)):
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    detector = FER(mtcnn=True)
    results = detector.detect_emotions(img)

    if results:
        emotions = results[0]["emotions"]
        dominant_emotion = max(emotions, key=emotions.get)
        return {"emotion": dominant_emotion}
    else:
        return JSONResponse(content={"error": "No face detected"}, status_code=400)

@app.get("/get_songs/")
def get_songs(emotion: str, language: str):
    token = get_spotify_token()
    if not token:
        return JSONResponse(content={"error": "Failed to fetch Spotify token"}, status_code=500)

    search_query = f"{emotion} {language} playlist"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    url = f"https://api.spotify.com/v1/search?q={search_query}&type=playlist&limit=5"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        playlists_data = response.json().get("playlists", {}).get("items", [])
        
     
        playlists = [p for p in playlists_data if p]

        results = []
        for p in playlists:
            try:
                results.append({
                    "name": p["name"],
                    "url": p["external_urls"]["spotify"],
                    "image": p["images"][0]["url"] if p["images"] else ""
                })
            except Exception as e:
                print(f"Skipping a playlist due to error: {e}")

        return {"playlists": results}
    
    else:
        print("Spotify API Error:", response.text)
        return JSONResponse(
            content={"error": "Spotify API failed", "details": response.text},
            status_code=500
        )



"""
# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fer import FER
import cv2
import numpy as np

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace * with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/detect_emotion/")
async def detect_emotion(file: UploadFile = File(...)):
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    detector = FER(mtcnn=True)
    results = detector.detect_emotions(img)

    if results:
        emotions = results[0]["emotions"]
        dominant_emotion = max(emotions, key=emotions.get)
        return {"emotion": dominant_emotion}
    else:
        return JSONResponse(content={"error": "No face detected"}, status_code=400)

"""
