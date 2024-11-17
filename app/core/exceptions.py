from fastapi import HTTPException, status


def raise_user_not_found():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


def raise_incorrect_credentials():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect credentials"
    )


def raise_not_found(message):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{message}"
    )