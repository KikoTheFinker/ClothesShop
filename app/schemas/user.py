from pydantic import BaseModel, EmailStr, Field, constr


class BaseConfig:
    from_attributes = True


class UserBase(BaseModel):
    name: constr(min_length=2)
    surname: constr(min_length=2)
    email: EmailStr
    phone_number: constr(pattern=r"^\+[1-9]\d{7,14}$",  strip_whitespace=True)
    city: constr(min_length=2) | None = None
    country: constr(min_length=2)

    class Config(BaseConfig):
        pass


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    class Config(BaseConfig):
        pass


class UserUpdate(BaseModel):
    user_id: int = Field(alias="id")
    name: str | None = None
    surname: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    city: str | None = None
    country: str | None = None

    class Config(BaseConfig):
        pass


class UserResponse(UserBase):
    user_id: int = Field(..., alias="id")

    class Config(BaseConfig):
        pass


class UserLogin(BaseModel):
    email: EmailStr | None = None
    phone_number: str | None = None
    password: str

    class Config(BaseConfig):
        pass
