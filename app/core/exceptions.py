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


def raise_user_already_exists(message):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"{message}"
    )


def raise_jwt_invalid_or_expired():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Please log in"
    )
def raise_wardrobe_conflict(message):
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=message
    )

def raise_item_exception(message):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message
    )

def raise_forbidden(message):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=message
    )