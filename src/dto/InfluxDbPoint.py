from  datetime import datetime

from pydantic import BaseModel
class InfluxDbPoint(BaseModel):
    attention: float
    relaxation: float
    video_ms: int
    timestamp: datetime
    alpha: int
    beta: int
    theta: int
    gaze_x: float
    gaze_y: float
    gaze_h: str
    gaze_v: str
    left_eye: bool
    right_eye: bool
    elapsed_sec: float