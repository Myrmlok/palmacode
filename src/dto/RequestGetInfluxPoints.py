from pydantic import BaseModel


class InfluxPointsParameters(BaseModel):
    user_id:str
    video_id:int

