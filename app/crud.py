from app.schemas.item import ItemCreate
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
import sqlalchemy as sa
from loguru import logger
from app.utils import get_password_hash, verify_password

from app.database import Base

from app.models import User, Item
from app.schemas import (
    UserCreate,
    UserUpdate,
    ItemCreate,
    ItemUpdate
)


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, after_field=None, after_value=None, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        q = db.query(self.model)
        if after_field:
            q.order_by(getattr(self.model, after_field))
        if after_value and after_field:
            q = q.filter(getattr(self.model, after_field) >= after_value)
        q = q.offset(skip).limit(limit)
        logger.debug(f"multi {self.model} {q}")
        return q.all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
            is_active=obj_in.is_active,
            is_verified=obj_in.is_verified,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        logger.info(f"authenticating email {email} -> {user}")
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            logger.error("password does not match")
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def get_by_code(self, db: Session, *, code: str) -> Optional[Item]:
        return db.query(Item).filter(Item.code == code).first()

    def get_by_name(self, db: Session, *, name: str) -> Optional[Item]:
        return db.query(Item).filter(Item.name == name).first()

    def create(self, db: Session, *, obj_in: ItemCreate) -> Item:
        db_obj = Item(
            name=obj_in.name,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Item, obj_in: Union[ItemUpdate, Dict[str, Any]]
    ) -> Item:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


item = CRUDItem(Item)