from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    msg: str


class UserInDB(UserBase):
    hashed_password: str


class UserUpdateSub(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    # TODO: include password also


def fake_password_hash(raw_password: str):
    return "supersecret_" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hash(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db
