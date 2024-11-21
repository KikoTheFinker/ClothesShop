from pydantic import BaseModel, EmailStr, constr, Field


class UserBase(BaseModel):
    name: str
    surname: str
    email: EmailStr
    phone_number: constr(pattern=r"^\+389\d{8}$")
    city: str | None = None
    country: str

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str

    class Config:
        from_attributes = True


class UserUpdate(UserBase):
    user_id: int = Field(alias="id")
    name: str | None = None
    surname: str | None = None
    email: EmailStr | None = None
    phone_number: constr(pattern=r"^\+389\d{8}$") | None = None
    city: str | None = None
    country: str | None = None

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    user_id: int = Field(..., alias='id')

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr | None = None
    phone_number: constr(pattern=r"^\+389\d{8}$") | None = None
    password: str

    class Config:
        from_attributes = True
