from pydantic import BaseModel, EmailStr, constr, Field


class BaseConfig:
    from_attributes = True


class UserBase(BaseModel):
    name: str
    surname: str
    email: EmailStr
    phone_number: constr(pattern=r"^\+389\d{8}$")
    city: str | None = None
    country: str

    class Config(BaseConfig):
        pass


class UserCreate(UserBase):
    password: str

    class Config(BaseConfig):
        pass


class UserUpdate(BaseModel):
    user_id: int = Field(alias="id")
    name: str | None = None
    surname: str | None = None
    email: EmailStr | None = None
    phone_number: constr(pattern=r"^\+389\d{8}$") | None = None
    city: str | None = None
    country: str | None = None

    class Config(BaseConfig):
        pass


class UserResponse(UserBase):
    user_id: int = Field(..., alias='id')

    class Config(BaseConfig):
        pass


class UserLogin(BaseModel):
    email: EmailStr | None = None
    phone_number: constr(pattern=r"^\+389\d{8}$") | None = None
    password: str

    class Config(BaseConfig):
        pass
