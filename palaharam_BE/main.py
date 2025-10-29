from fastapi import FastAPI
from routes.routes import router
from fastapi.middleware.cors import CORSMiddleware


app =FastAPI()

app.include_router(router)

origins = [
    "http://localhost:3000",  # React default
    "http://127.0.0.1:3000",
    "https://myfrontenddomain.com"  # Production frontend
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # or ["*"] to allow all (not recommended in prod)
    allow_credentials=True,
    allow_methods=["*"],         # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],         # Allow all headers
)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
