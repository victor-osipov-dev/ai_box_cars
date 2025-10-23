from fastapi import APIRouter
from fastapi.responses import FileResponse, Response
import io
from fastapi import UploadFile, File
from fastapi.responses import FileResponse, Response
from ultralytics import YOLO
from PIL import Image
from typing import List
import aiohttp
from requests_toolbelt.multipart.encoder import MultipartEncoder

model = YOLO('best.pt')
router = APIRouter(prefix="")

def imgToByteImg(img):
    im = Image.fromarray(img[..., ::-1])
    img_byte_arr = io.BytesIO()
    im.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()


boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
def create_multidata(field, data, type):

    return f"""{boundary}
Content-Disposition: form-data; name="{field}"; filename="{field}"
Content-Type: {type}

{data}
{boundary}
"""

class FormData:
    def __init__(self):
        self.boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
        self.data = io.BytesIO()

    def append(self, field, file_name, data):
        self.data.write(f'--{boundary}\r\n'.encode())
        self.data.write(f'Content-Disposition: form-data; name="{field}"; filename="{file_name}"\r\n'.encode())
        self.data.write(b'Content-Type: image/jpg\r\n\r\n')
        self.data.write(data)
        self.data.write(b'\r\n')

    def getAll(self):
        self.data.write(f'--{boundary}--\r\n'.encode())
        return self.data.getvalue()
    def getMediaType(self):
        return f"multipart/form-data; boundary={self.boundary}"


@router.post("/echo-image")
async def echo_image(files: List[UploadFile] = File(...)):
    # form_data = aiohttp.FormData()
    form_data = FormData()
    images = []

    for file in files:
        content = await file.read()
        image = Image.open(io.BytesIO(content))
        images.append(image)

    results = model.predict(images, stream=False, classes=[9, 10])

    print(results)

    response_data = []

    for result in results:
        response_data.append(
            imgToByteImg(result.plot())
        )
        form_data.append('image', 'image.jpeg', imgToByteImg(result.plot()))

    # multipart = MultipartEncoder(
    #     fields={
    #         "image": ("image.jpg", response_data[0], "image/jpeg"),
    #         "image2": ("image.jpg", response_data[0], "image/jpeg"),
    #     }
    # )
    

     # Создаем бинарные данные (например, изображение)
    # binary_data = response_data[0]
    
    # output = io.BytesIO()
    
    # # Текстовая часть
    # output.write(f'--{boundary}\r\n'.encode())
    # output.write(b'Content-Disposition: form-data; name="description"\r\n\r\n')
    # output.write(b'This is a JPG image\r\n')
    
    # # Бинарная часть
    # output.write(f'--{boundary}\r\n'.encode())
    # output.write(b'Content-Disposition: form-data; name="image"; filename="image.jpg"\r\n')
    # output.write(b'Content-Type: image/jpg\r\n\r\n')
    # output.write(binary_data)
    # output.write(b'\r\n')

    # # Бинарная часть 2
    # output.write(f'--{boundary}\r\n'.encode())
    # output.write(b'Content-Disposition: form-data; name="image"; filename="image.jpg"\r\n')
    # output.write(b'Content-Type: image/jpg\r\n\r\n')
    # output.write(binary_data)
    # output.write(b'\r\n')
    
    # # Закрытие
    # output.write(f'--{boundary}--\r\n'.encode())
    
    # content_bytes = output.getvalue()
    
    return Response(
        content=form_data.getAll(),
        media_type=form_data.getMediaType(),
        # headers={"Content-Length": str(len(content_bytes))}
    )
    # return Response(
    #     content=create_multidata('image', response_data[0], "image/jpeg"),
    #     media_type=f"multipart/form-data; boundary={boundary}"
    # )
    # return Response(
    #     content=response_data[0],
    #     media_type="image/jpeg"
    # )




@router.get("/test")
def get_images():
    file_path = "images/55.5817833,37.5914424.jpg"

    return FileResponse(
        path=file_path,
        media_type='image/jpg'
    )