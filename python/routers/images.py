from fastapi import APIRouter
from fastapi.responses import FileResponse, Response
import io
from fastapi import UploadFile, File
from fastapi.responses import FileResponse, Response
from ultralytics import YOLO
from PIL import Image

model = YOLO('yolo11m.pt')
router = APIRouter(prefix="")


@router.get("/test")
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

@router.post("/echo-image")
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