from typing import Optional

from pydantic import BaseModel, EmailStr, Field

# from src.database.models import Role


class ContactModel(BaseModel):

    first_name: str = Field('Dmytro', min_length=3, max_length=25)
    last_name: str = Field('Oseledko', min_length=3, max_length=25)
    email: EmailStr
    phone_number: str = Field('050-907-97-77')
    birthday: str = Field('10-04-2019')
    nick: str = Field('nick')
    is_active_contact: Optional[bool] = True
    description: str = Field('description')


class ContactActiveModel(BaseModel):
    is_active_contact: bool = True


# class CatModel(BaseModel):
#     nick: str = Field('Barsik', min_length=3, max_length=16)
#     age: int = Field(1, ge=1, le=30)
#     vaccinated: Optional[bool] = False
#     description: str
#     owner_id: int = Field(1, gt=0)  # ge >=  gt >


class ContactResponse(BaseModel):
    id: int = 1
    first_name: str = 'Dmytro'
    last_name: str = 'Oseledko'
    email: EmailStr
    phone_number: str = '050-907-97-77'
    birthday: str = '10-04-2019'

    nick: str
    is_active_contact: bool = True
    description: str

    class Config:
        orm_mode = True


# class CatResponse(BaseModel):
#     id: int = 1
#     nick: str = 'Barsik'
#     age: int = 12
#     vaccinated: bool = False
#     description: str
#     owner: OwnerResponse
#
#     class Config:
#         orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=12)
    email: EmailStr
    password: str = Field(min_length=6, max_length=8)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    avatar: str
    # role: Role  -------------------------------

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
