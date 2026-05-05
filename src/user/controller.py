from src.user.dtos import UserSchema as User, UserLoginSchema as UserLogin
from sqlalchemy.orm import Session
from src.user.models import UserModel
from fastapi import HTTPException, Request, status
from pwdlib import PasswordHash
from src.utils.settings import settings
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

password_hash = PasswordHash.recommended()

# Utility function to hash the password
def get_password_hash(password):
    return password_hash.hash(password)

# Verify hashed password and plain password
def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

#user registration
def register_user(body: User, db: Session):
    print(body)
    # 1. Username Validation
    # 2. email validation
    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()

    if is_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists..")

    is_email = db.query(UserModel).filter(UserModel.email == body.email).first()

    if is_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists..")

    # 3. Hash the password
    hashed_password = get_password_hash(body.password)
    # 4. mobile number validation
    if not body.mobile_number.isdigit() or len(body.mobile_number) != 10:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid mobile number. It should be a 10-digit number.")

    # 5. create UserModel Instance

    new_user = UserModel(
        name = body.name,
        username = body.username,
        email = body.email,
        hashed_password = hashed_password,
        mobile_number = body.mobile_number
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def login_user(body: UserLogin, db: Session):
    user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    if not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    token = jwt.encode({
        "_id": user.id,
        "username": user.username,
        "exp": (datetime.now(timezone.utc) + timedelta(seconds=settings.EXP_TIME)).timestamp()
    }, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return {
        "token": token
    }

# how to send token in header
def is_authenticated(request: Request, db: Session):
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
