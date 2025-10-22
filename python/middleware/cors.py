from fastapi.middleware.cors import CORSMiddleware

def defineCorsMiddleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Разрешает все домены
        allow_credentials=True,
        allow_methods=["*"],  # Разрешает все HTTP методы
        allow_headers=["*"],  # Разрешает все заголовки
    )