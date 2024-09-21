from pydantic import BaseModel
from typing import Optional

class SignUpModel(BaseModel):
    id:Optional[int]
    username: str
    email:str
    password:str
    is_staff:Optional[bool]
    is_active:Optional[bool]

    class Config:
        orm_mode=True
        schema_extra={
            'example':{
                "username":"johndoe",
                "email":"johndeo@gmail.com",
                "password":"password",
                "is_staff":False,
                "is_active":True
            }
        }


class Settings(BaseModel):
    authjwt_secret_key:str='897ed79b601faaacaaa02a01218fedbc902f97e79f22de05600a3a71b851f82b'

class LoginModel(BaseModel):
    username:str
    password:str


class OrderModel(BaseModel):
    id: Optional[int] = None
    quantity: int
    order_status: Optional[str] = "PENDING"
    pizza_size: Optional[str] = "SMALL"
    user_id: Optional[int] = None

    class Config:  # Capitalize 'Config'
        orm_mode = True
        schema_extra = {
            'example': {
                "quantity": 2,
                "pizza_size": "LARGE"
            }
        }