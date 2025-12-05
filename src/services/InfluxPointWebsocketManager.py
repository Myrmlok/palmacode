import json
from typing import Dict, List
from uuid import UUID

from websockets import connect

from src.reports.controller import ReportController
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from starlette.websockets import WebSocket
from watchfiles import awatch

from src.database.database import session_maker_async
from src.dto.InfluxDbPoint import InfluxDbPoint
from src.reports.models import Report
from src.repository.InfluxDbRepository import writePoint
from datetime import datetime, timezone

from src.users.models import User


class InfluxPointWebsocketManager:
    connections:Dict[int,Dict[int,WebSocket]]={}
    @classmethod
    async def register(cls,websocket:WebSocket,video_id:int,user:User)->Report:
        cls.connections[video_id][user.id] = websocket
        return await ReportController.create_report(datetime.now(timezone.utc),video_id,user_id=user.id)

    @classmethod
    async def receiveAndSavePoint(cls, websocket:WebSocket,video_id:int,user,influx_db_client):
        data = await websocket.receive_json()
        points:List[InfluxDbPoint] = [InfluxDbPoint.model_validate(el) for el in data]
        for el in points:
             writePoint(video_id,el, user, influx_db_client)
    @classmethod
    async def disconnect(cls,video_id:int,report_id:int,user:User):
        await ReportController.update_report(report_id,datetime.now(timezone.utc))
        await cls.connections[video_id].pop(user.id).close()


