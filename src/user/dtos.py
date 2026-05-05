from pydantic import BaseModel

class UserSchema(BaseModel):
    name: str
    username: str
    email: str
    password: str
    mobile_number: str

class UserResponseSchema(BaseModel):
    id: int
    name: str
    username: str
    email: str
    mobile_number: str

class UserLoginSchema(BaseModel):
    username: str
    password: str
