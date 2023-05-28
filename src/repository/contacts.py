from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel, ContactActiveModel


async def get_contacts(db: Session):
    contacts = db.query(Contact).all()
    return contacts


async def get_contacts_birthday(birthday: str, db: Session):
    contacts = db.query(Contact).filter_by(birthday=birthday).all()
    return contacts


async def get_contact_by_id(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def get_contact_by_email(email: str, db: Session):
    contact = db.query(Contact).filter_by(email=email).first()
    return contact


async def get_contacts_by_first_name(first_name: str, db: Session):
    contacts = db.query(Contact).filter_by(first_name=first_name).all()
    return contacts


async def get_contacts_by_last_name(last_name: str, db: Session):
    contacts = db.query(Contact).filter_by(last_name=last_name).all()
    return contacts


async def create(body: ContactModel, db: Session):
    contact = Contact(**body.dict())  # Owner(**body.dict())   Contact(email=body.email)
    db.add(contact)
    db.commit()
    return contact


async def update(contact_id: int, body: ContactModel, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.email = body.email
        db.commit()
    return contact


async def remove(contact_id: int, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def set_is_active_contact(contact_id: int, body: ContactActiveModel, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.is_active_contact = body.is_active_contact
        db.commit()
    return contact
