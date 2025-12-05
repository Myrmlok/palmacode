import os
from typing import Any, AsyncGenerator, Generator

from influxdb_client import InfluxDBClient
from pydantic_settings import BaseSettings, SettingsConfigDict
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
class INFLUXdbSetting(BaseSettings):
    INFLUX_TOKEN:str
    INFLUX_URL:str
    INFLUX_ORG:str
    INFLUX_BUCKET:str
    INFLUX_MEASUREMENT:str
    model_config = SettingsConfigDict(
        env_file=os.path.join("C:/Users/user/PycharmProjects/BrainTubeBack/env/influxdb.env")
    )
influxdb_settings=INFLUXdbSetting()
def get_influx_client_sync()-> Generator[InfluxDBClient, Any, None]:
    client = InfluxDBClient(url=influxdb_settings.INFLUX_URL, token=influxdb_settings.INFLUX_TOKEN,
                            org=influxdb_settings.INFLUX_ORG)
    try:
        yield client
    except Exception as e:
        raise  e
    finally:
        client.close()
async def get_influx_client()-> AsyncGenerator[InfluxDBClientAsync, Any]:
    async with InfluxDBClientAsync(url=influxdb_settings.INFLUX_URL,
                               token=influxdb_settings.INFLUX_TOKEN,
                               org=influxdb_settings.INFLUX_ORG,
                               ) as client:

        yield client
        await client.close()