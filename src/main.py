from typing import List

import uvicorn
from fastapi import FastAPI
from fastapi.params import Depends
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync

from src.config.influxdbConfig import get_influx_client
from src.dto.InfluxDbPoint import InfluxDbPoint
from src.entity.UserApp import UserApp
from src.repository.InfluxDbRepository import writePoint
from src.route.influxPointRoute import influxPointRouter

app = FastAPI()
app.include_router(influxPointRouter)
@app.get("/")
async def hello():
    return "hello"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8099)