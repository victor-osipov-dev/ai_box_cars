import os
import cv2
import io
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from PIL import Image
import numpy as np


model = YOLO('yolo11m.pt')



app = FastAPI()

image_dir = "images"
color_blue = (255, 0, 0)

app.mount("/static", StaticFiles(directory=image_dir), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешает все домены
    allow_credentials=True,
    allow_methods=["*"],  # Разрешает все HTTP методы
    allow_headers=["*"],  # Разрешает все заголовки
)

@app.get("/images")
def get_images():
    file_path = "images/55.5817833,37.5914424.jpg"

    return FileResponse(
        path=file_path,
        media_type='image/jpg'
    )

def imgToByteImg(img):
    im = Image.fromarray(img[..., ::-1])
    img_byte_arr = io.BytesIO()
    im.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()

@app.post("/echo-image")
async def echo_image(file: UploadFile = File(...)):
    contents = await file.read()
    
    image = Image.open(io.BytesIO(contents))
    results = model.predict(image, stream=True)

    for result in results:
        img = result.plot()

    img = imgToByteImg(img)
    
    return Response(
        content=img,
        media_type="image/jpeg"
    )