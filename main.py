from fastapi import FastAPI
from routers.router import router


app = FastAPI(rooth_path="/docs")



app.include_router(router)
