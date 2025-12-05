from  datetime import datetime

from pydantic import BaseModel
class InfluxDbPoint(BaseModel):
    value:float
    timeVideo:datetime
    time:datetime
    video_url:str