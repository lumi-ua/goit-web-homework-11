from datetime import date
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

class ContactModel(BaseModel):
    first_name: str = Field(min_length=2, max_length=20)
    last_name: str = Field(min_length=2, max_length=20)
    email: EmailStr
    phone_number: str = Field(min_length=5, max_length=25)
    birthday: date


class ContactResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date
    
    # class Config:
    #     orm_mode = True


