import os
from typing import Any, AsyncGenerator

from pydantic_settings import BaseSettings, SettingsConfigDict
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
class INFLUXdbSetting(BaseSettings):
    INFLUX_TOKEN:str
    INFLUX_URL:str
    INFLUX_ORG:str
    INFLUX_BUCKET:str
    model_config = SettingsConfigDict(
        env_file=os.path.join("C:/Users/user/PycharmProjects/BrainTubeBack/env/influxdb.env")
    )
influxdb_settings=INFLUXdbSetting()
async def get_influx_client()-> AsyncGenerator[InfluxDBClientAsync, Any]:
    async with InfluxDBClientAsync(url="http://localhost:8086",
                               token=influxdb_settings.INFLUX_TOKEN,
                               org=influxdb_settings.INFLUX_ORG,
                               ) as client:

        yield client
        await client.close()