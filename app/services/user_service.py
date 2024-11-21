from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.exceptions import raise_user_not_found, raise_incorrect_credentials, raise_user_already_exists
from app.core.security import hash_password, verify_password
from .. import models, schemas


def create_user(db: Session, user: schemas.UserCreate) -> dict:
    existing_user_by_email = get_user_by_email(db=db, email=user.email)

    if existing_user_by_email:
        raise_user_already_exists("A user with this email already exists.")

    existing_user_by_phone_number = get_user_by_phone_number(db=db, phone_number=user.phone_number)
    if existing_user_by_phone_number:
        raise_user_already_exists("A user with this phone number already exists.")

    hashed_password = hash_password(user.password)

    db_user = models.User(
        name=user.name,
        surname=user.surname,
        email=user.email,
        phone_number=user.phone_number,
        city=user.city,
        country=user.country,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "user created successfully"}


def get_user(db: Session, user_id: int) -> schemas.UserResponse:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise_user_not_found()
    return schemas.UserResponse.from_orm(db_user)


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_phone_number(db: Session, phone_number: str) -> models.User | None:
    return db.query(models.User).filter(models.User.phone_number == phone_number).first()


def update_user(db: Session, user_id: int, user: schemas.UserUpdate, password: str) -> schemas.UserResponse:
    db_user = get_user(db, user_id)

    if db_user is None:
        raise_user_not_found()

    if not verify_password(password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    if user.name:
        db_user.name = user.name
    if user.surname:
        db_user.surname = user.surname
    if user.email:
        db_user.email = user.email
    if user.phone_number:
        db_user.phone_number = user.phone_number
    if user.city:
        db_user.city = user.city
    if user.country:
        db_user.country = user.country

    if user.password:
        db_user.password = hash_password(user.password)

    db.commit()
    db.refresh(db_user)

    return schemas.UserResponse.from_orm(db_user)


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return {"detail": f"User {user_id} deleted successfully."}
    else:
        raise_user_not_found()


def authenticate_user(db: Session, email: str = None, phone_number: str = None, password: str = None):
    user = None
    if not email and not phone_number:
        raise_incorrect_credentials()

    if email:
        user = get_user_by_email(db, email)
    elif phone_number:
        user = get_user_by_phone_number(db, phone_number)

    if not verify_password(password, user.password):
        raise_incorrect_credentials()

    return user
