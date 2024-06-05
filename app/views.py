from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter

from app.dependencies import get_redis
from app.schema import DataSchema, HealthcheckSchema

router = APIRouter()


@router.get("/healthcheck", response_model=HealthcheckSchema)
def home(redis=Depends(get_redis)):
    redis.set("check", "pass")
    response = redis.get("check")
    return HealthcheckSchema(check=response)


@router.get(
    "/check_data",
    response_model=DataSchema,
)
def check_data(phone: str, redis=Depends(get_redis)):
    address = redis.get(phone)
    return DataSchema(phone=phone, address=address)


@router.post(
    "/write_data",
    response_model=DataSchema,
)
def write_data(data: DataSchema, redis=Depends(get_redis)):
    redis.set(data.phone, data.address)
    return DataSchema(data.phone, data.address)


@router.put(
    "/write_data",
    response_model=DataSchema,
)
def write_data(data: DataSchema, redis=Depends(get_redis)):
    address = redis.get(data.phone)
    if address is not None:
        redis.set(data.phone, data.address)
        return DataSchema(data.phone, data.address)
    else:
        raise HTTPException(status_code=404, detail="The number is missing from the database")
