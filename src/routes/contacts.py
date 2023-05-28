from typing import List
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import Contact, User  # , Role
from src.schemas import ContactResponse, ContactModel
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

# from src.services.roles import RolesAccess

router = APIRouter(prefix="/contacts", tags=["contacts"])


# access_get = RolesAccess([Role.admin, Role.moderator, Role.user])
# access_create = RolesAccess([Role.admin, Role.moderator])
# access_update = RolesAccess([Role.admin, Role.moderator])
# access_delete = RolesAccess([Role.admin])


@router.get("/", response_model=List[ContactResponse])  # , dependencies=[Depends(access_get)])
async def get_contacts(db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                      _: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_id(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return contact


@router.post("/", response_model=ContactResponse,
             status_code=status.HTTP_201_CREATED)  # ,  dependencies=[Depends(access_create)])
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         _: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_email(body.email, db)
    if contact:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is exists!")
    contact = await repository_contacts.create(body, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)  # , dependencies=[Depends(access_update)])
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         _: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)  # , dependencies=[Depends(access_delete)])
async def delete_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         _: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return contact


# ----------begin------------------------------------------------------------------------------------
@router.get("/birthday", response_model=List[ContactResponse])
async def get_contacts_birthday(db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    #  async def get_users_birthday(difference_days: int = 7, db: Session = Depends(get_db)):
    difference_days = 7 + 1
    present_day = datetime.now()

    contacts = []
    all_contacts = await repository_contacts.get_contacts(db)

    for contact in all_contacts:
        if contact.birthday is None:
            continue
        birthday_contact = datetime.strptime(contact.birthday, '%d-%m-%Y')
        birthday_contact_current_year = birthday_contact.replace(year=present_day.year)
        delta_birthday = (birthday_contact_current_year - present_day).days
        if 0 < delta_birthday < difference_days:
            contacts.append(contact)

    if not bool(contacts):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return contacts


@router.get("/first_name/{first_name}", response_model=List[ContactResponse])
async def get_contacts_by_first_name(first_name: str, db: Session = Depends(get_db),
                                     _: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts_by_first_name(first_name, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return contacts


@router.get("/last_name/{last_name}", response_model=List[ContactResponse])
async def get_contacts_by_last_name(last_name: str, db: Session = Depends(get_db),
                                    _: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts_by_last_name(last_name, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return contacts


@router.get("/email/{email}", response_model=ContactResponse)
async def get_contact_by_email(body: ContactModel, db: Session = Depends(get_db),
                               _: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_email(body.email, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return contact


@router.patch("/{contact_id}/is_active_contact", response_model=ContactResponse)
async def set_is_active_contact(body: ContactActiveModel, contact_id: int = Path(ge=1),
                                db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.set_is_active_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return contact
