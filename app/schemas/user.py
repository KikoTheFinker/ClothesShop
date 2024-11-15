from pydantic import BaseModel, EmailStr, constr


class UserBase(BaseModel):
    name: str
    surname: str
    email: EmailStr
    phone_number: constr(pattern=r"^\+389\d{7}$")
    city: str | None = None
    country: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    name: str | None = None
    surname: str | None = None
    email: EmailStr | None = None
    phone_number: constr(pattern=r"^\+389\d{7}$") | None = None
    city: str | None = None
    country: str | None = None

    class Config:
        orm_mode = True


class UserResponse(UserBase):
    user_id: int

    class Config:
        orm_mode = True
