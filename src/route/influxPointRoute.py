import datetime
import logging
from idlelib.window import add_windows_to_menu
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from select import select
from starlette.websockets import WebSocket
from datetime import datetime, timezone

from watchfiles import awatch

from src.adminuser.models import UserToAdmin
from src.config.influxdbConfig import get_influx_client, get_influx_client_sync
from src.database.database import session_maker_async
from src.dto.RequestGetInfluxPoints import InfluxPointsParameters
from src.repository.InfluxDbRepository import getInfluxPoints, getInfluxPointsBetweenTime
from src.services.InfluxPointWebsocketManager import InfluxPointWebsocketManager
from src.services.usersDepends import get_current_user
from src.users.models import User

influxPointRouter=APIRouter(prefix="/influxdbpoints",tags=["influxPoints"])
@influxPointRouter.websocket("/ws/login/{video_id}")
async def logWebsocket(websocket:WebSocket,video_id:int,user:User=Depends(get_current_user),influxClient:InfluxDBClientAsync=Depends(get_influx_client_sync)):
    report=await InfluxPointWebsocketManager.register(websocket,video_id,user)
    await websocket.accept()
    try:
        while(True):
            await InfluxPointWebsocketManager.receiveAndSavePoint(websocket,video_id,user,influxClient)
    except Exception as e:
        await InfluxPointWebsocketManager.disconnect(video_id,report.id,user)
        raise e
    finally:
        await InfluxPointWebsocketManager.disconnect(video_id,report.id,user)
        await websocket.close()
@influxPointRouter.get("/points")
async def getPoints(video_id:int=12345,user_id:str="",
                    auth_user:User=Depends(get_current_user),
                    influxClient:InfluxDBClientAsync=Depends(get_influx_client)):
    async with session_maker_async() as session:
        res=await session.query(UserToAdmin). \
            join(UserToAdmin,int(user_id) == UserToAdmin.user_id). \
            filter(UserToAdmin.admin_id == auth_user.id). \
            all()
        if res is None:
            raise Exception("user not found")
        return await getInfluxPoints(InfluxPointsParameters(video_id=video_id,user_id=str(user_id)),influxClient)
@influxPointRouter.get("/points/between")
async def getPointsBetween(video_id:int=12345,user_id:str="",
                           start:datetime=datetime.now(timezone.utc),
                           end:datetime=datetime.now(timezone.utc),
                           influxClient:InfluxDBClientAsync=Depends(get_influx_client),
                           auth_user:User=Depends(get_current_user)):
    async with session_maker_async() as session:
        res=await session.query(UserToAdmin). \
            join(UserToAdmin, int(user_id) == UserToAdmin.user_id). \
            filter(UserToAdmin.admin_id == auth_user.id). \
            all()
        if res is None:
            raise Exception("user not found")
        param=InfluxPointsParameters(user_id=user_id,video_id= video_id)
        return await getInfluxPointsBetweenTime(param_influx_points=param,start=start,end=end,influx_client=influxClient)