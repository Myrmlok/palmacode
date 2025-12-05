import datetime
from typing import List

from influxdb_client import Point, InfluxDBClient
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync

from src.dto.InfluxDbPoint import InfluxDbPoint
from src.config.influxdbConfig import influxdb_settings
from src.dto.RequestGetInfluxPoints import InfluxPointsParameters


def writePoint(video_id:int,point:InfluxDbPoint,user,influx_client:InfluxDBClient):

    pointRes=(Point(influxdb_settings.INFLUX_MEASUREMENT)
         .time(datetime.datetime.now(datetime.timezone.utc))
         .tag("user_id",user.id)
         .tag("video_id", video_id)
         .field("attention",point.attention)
         .field("elapsed_sec",point.elapsed_sec)
         .tag("video_ms",point.video_ms)
         .field("relaxation",point.relaxation)
         .field("alpha",point.alpha)
         .field("beta",point.beta)
         .field("theta",point.theta)
         .field("gaze_x",point.gaze_x)
         .field("gaze_y",point.gaze_y)
         .tag("gaze_h",point.gaze_h)
         .tag("gaze_v",point.gaze_v)
         .tag("left_eye",point.left_eye)
         .tag("right_eye",point.right_eye))
    res= influx_client.write_api().write(influxdb_settings.INFLUX_BUCKET, influx_client.org, pointRes)
    return res


async def getInfluxPoints(requestGetInfluxPoints:InfluxPointsParameters,influx_client:InfluxDBClientAsync):
    query = f'''
           from(bucket: "{influxdb_settings.INFLUX_BUCKET}")
             |> range(start: 0)
             |> filter(fn: (r) => r["_measurement"] == "{influxdb_settings.INFLUX_MEASUREMENT}")
             |> filter(fn: (r) => r["video_id"] == "{requestGetInfluxPoints.video_id}")
             |> filter(fn: (r) => r["user_id"] == "{requestGetInfluxPoints.user_id}")
             |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
       '''
    res_table = await influx_client.query_api().query(query=query)
    influx_points: List[InfluxDbPoint] = []

    for table in res_table:
        for record in table.records:

            point = InfluxDbPoint(
                elapsed_sec=record.values.get("elapsed_sec",0),
                relaxation=record.values.get("relaxation"),
                attention=record.values.get("attention"),
                video_ms=record.values.get("video_ms", 0),  # это tag
                timestamp=record.get_time(),
                alpha=record.values.get("alpha", 0),
                beta=record.values.get("beta",0),
                theta=record.values.get("theta", 0),
                gaze_x=record.values.get("gaze_x", 0),
                gaze_y=record.values.get("gaze_y", 0),
                gaze_h=record.values.get("gaze_h", ""),
                gaze_v=record.values.get("gaze_v", ""),
                left_eye=record.values.get("left_eye", False),
                right_eye=record.values.get("right_eye", False))
            influx_points.append(point)


    return influx_points
async def getInfluxPointsBetweenTime(param_influx_points:InfluxPointsParameters,start:datetime,end:datetime,influx_client:InfluxDBClientAsync):
    query=f'''
    from(bucket:"{influxdb_settings.INFLUX_BUCKET}")
    |>range(start:"{start}",end:"{end}")
    |> filter(fn: (r) => r["_measurement"] == "{influxdb_settings.INFLUX_MEASUREMENT}")
    |> filter(fn: (r) => r["video_id"] == "{param_influx_points.video_id}")
    |> filter(fn: (r) => r["user_id"] == "{param_influx_points.user_id}")
    |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
'''
    res_table=await influx_client.query_api().query(query)
    influx_points: List[InfluxDbPoint] = []
    for table in res_table:
        for record in table.records:
            point = InfluxDbPoint(
                elapsed_sec=record.values.get("elapsed_sec", 0),
                relaxation=record.values.get("relaxation"),
                attention=record.values.get("attention"),
                video_ms=record.values.get("video_ms", 0),  # это tag
                timestamp=record.get_time(),
                alpha=record.values.get("alpha", 0),
                beta=record.values.get("beta", 0),
                theta=record.values.get("theta", 0),
                gaze_x=record.values.get("gaze_x", 0),
                gaze_y=record.values.get("gaze_y", 0),
                gaze_h=record.values.get("gaze_h", ""),
                gaze_v=record.values.get("gaze_v", ""),
                left_eye=record.values.get("left_eye", False),
                right_eye=record.values.get("right_eye", False))
            influx_points.append(point)
    return influx_points