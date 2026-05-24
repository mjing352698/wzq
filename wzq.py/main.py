from logic import wzq
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model import init_db
app = FastAPI()
app.add_middleware(CORSMiddleware, 
    allow_origins=["*"],
    allow_methods=["*"], 
    allow_headers=["*"],
    allow_credentials=True,
)
app.include_router(wzq)
@app.on_event("startup")
def startup_event():
    init_db()
