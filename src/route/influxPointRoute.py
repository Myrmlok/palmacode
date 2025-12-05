import logging

from fastapi import APIRouter
from fastapi.params import Depends
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from starlette.websockets import WebSocket

from src.config.influxdbConfig import get_influx_client
from src.entity.UserApp import UserApp
from src.service.InfluxPointWebsocketManager import InfluxPointWebsocketManager

influxPointRouter=APIRouter(prefix="/inluxdbpoints",tags=["influxPoints"])
@influxPointRouter.websocket("/ws/login")
async def logWebsocket(websocket:WebSocket,user=UserApp(),influxClient:InfluxDBClientAsync=Depends(get_influx_client)):
    await websocket.accept()
    try:
        while(True):
            await InfluxPointWebsocketManager.receiveAndSavePoint(websocket,user,influxClient)
    except Exception as e:
        logging.info(e)
        await websocket.close()
