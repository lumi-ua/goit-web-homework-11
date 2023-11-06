from typing import List
from datetime import date, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, extract 
from fastapi import HTTPException, status

from src.database.models import Contacts
from src.schemas import ContactModel

async def get_contacts(skip: int, limit: int, db: Session) -> List[Contacts]:
    return db.query(Contacts).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session):
    contact = db.query(Contacts).filter_by(id=contact_id).first()
    return contact


async def create_contact(body: ContactModel, db: Session):
    contact = Contacts(**body.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def create_contact(body: ContactModel, db: Session):
    existing_contact = db.query(Contacts).filter(
        (Contacts.email == body.email) | (Contacts.phone_number == body.phone_number)
    ).first()
    if existing_contact:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Contact is exists!') 

    contact = Contacts(**body.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact



async def update_contact(body: ContactModel, contact_id: int, db: Session):
    contact = db.query(Contacts).filter_by(id=contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        db.commit()
    return contact



async def remove_contact(contact_id: int, db: Session):
    contact = db.query(Contacts).filter_by(id=contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact



async def search_contacts(query: str, db: Session):
    contacts = db.query(Contacts).filter(
        or_(
            Contacts.first_name.ilike(f"%{query}%"),
            Contacts.last_name.ilike(f"%{query}%"),
            Contacts.email.ilike(f"%{query}%"),
        )
    ).all()
    return contacts



async def get_contacts_with_upcoming_birthdays(db: Session):
    today = date.today()
    end_date = today + timedelta(days=7)
    contacts = db.query(Contacts).filter(
        and_(
            extract('month', Contacts.birthday) == today.month,
            extract('day', Contacts.birthday) >= today.day,
            extract('day', Contacts.birthday) <= end_date.day,
        )
    ).all()
    return contacts
