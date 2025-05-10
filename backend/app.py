from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router import router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:80"],  # change to in the future ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)