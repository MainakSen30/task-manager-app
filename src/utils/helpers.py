
from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.utils.settings import settings
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from src.user.models import UserModel
from src.utils.db import get_db

def is_authenticated(request: Request, db: Session = Depends(get_db)):
    try:
        token = request.headers.get("authorization")

        # Check if token is present in the header
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

        auth_token = token.split(" ")[-1]
        # Decode the token to get the user information
        data = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        # Extract user information from the token
        user_id = data.get("_id")

        #check if user exists in the database
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        return user

    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
