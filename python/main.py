from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from middleware import cors
from routers import images
from routers import index

app = FastAPI()

cors.defineCorsMiddleware(app)
app.include_router(index.router)
app.include_router(images.router)

app.mount("/static", StaticFiles(directory="images"), name="static")