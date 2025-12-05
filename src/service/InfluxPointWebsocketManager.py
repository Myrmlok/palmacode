from typing import Dict

from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from starlette.websockets import WebSocket

from src.dto.InfluxDbPoint import InfluxDbPoint
from src.entity.UserApp import UserApp
from src.repository.InfluxDbRepository import writePoint


class InfluxPointWebsocketManager:
    @classmethod
    async def receiveAndSavePoint(cls, websocket:WebSocket,user,influx_db_client:InfluxDBClientAsync):
        points= InfluxDbPoint.model_validate_json( await websocket.receive_json())
        await writePoint(points,user,influx_db_client)