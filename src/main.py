from typing import List

import uvicorn
from fastapi import FastAPI
from fastapi.params import Depends
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from starlette.middleware.cors import CORSMiddleware

from src.config.influxdbConfig import get_influx_client
from src.dto.InfluxDbPoint import InfluxDbPoint
from src.repository.InfluxDbRepository import writePoint
from src.route.influxPointRoute import influxPointRouter
from src.videos.router import router as videosRouter
from src.users.router import router as userRouter
from src.adminuser.router import router as adminUserRouter
from src.users.auth import router as authRouter
app = FastAPI()
app.include_router(influxPointRouter)
app.include_router(videosRouter)
app.include_router(userRouter)
app.include_router(adminUserRouter)
app.include_router(authRouter)
@app.get("/")
async def hello():
    return "hello"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для разработки
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8099)