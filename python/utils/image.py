from PIL import Image
import io

def imgToByteImg(img):
    im = Image.fromarray(img[..., ::-1])
    img_byte_arr = io.BytesIO()
    im.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()