from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    password: str
    email: str | None
    first_name: str | None
    last_name: str | None
    address1: str | None
    address2: str | None
    zipcode: str | None
    city: str | None
    state: str | None
    country: str | None
    phone: str | None


class User(UserCreate):
    user_id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")


class UserUpdate(UserCreate):
    pass
