from influxdb_client import Point
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync

from src.dto.InfluxDbPoint import InfluxDbPoint
from src.config.influxdbConfig import influxdb_settings


async def writePoint(point:InfluxDbPoint,user,influx_client:InfluxDBClientAsync):
    res=Point("bigBrain").time(point.time).tag("user_id",user.id).tag("timeVideo",point.timeVideo).field("value",point.value)
    return await  influx_client.write_api().write(influxdb_settings.INFLUX_BUCKET, influx_client.org, res)