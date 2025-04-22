from typing import Tuple
from pydantic import BaseModel, field_validator, IPvAnyAddress


class Developer(BaseModel):
    full_name: str
    department: str
    geolocation: Tuple[float, float]
    last_known_ip: IPvAnyAddress
    is_available: bool

    @field_validator("geolocation")
    def validate_geolocation(cls, value: Tuple[float, float]) -> Tuple[float, float]:
        lat, lon = value
        if not (-90 <= lat <= 90):
            raise ValueError('Latitude must be between -90 and 90')
        if not (-180 <= lon <= 180):
            raise ValueError('Longitude must be between -180 and 180')
        return value