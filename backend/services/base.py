from typing import Type, TypeVar, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

T = TypeVar("T")


class BaseService:
    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db

    def create(self, obj_data: dict) -> T:
        try:
            obj = self.model(**obj_data)
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
            return obj
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Failed to create object due to integrity error")

    def read(self, obj_id: str) -> Optional[T]:
        return self.db.query(self.model).filter(self.model.id == obj_id).first()

    def update(self, obj_id: str, update_data: dict) -> Optional[T]:
        obj = self.read(obj_id)
        if not obj:
            return None
        for key, value in update_data.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj_id: str) -> bool:
        obj = self.read(obj_id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True

    def list(self, filters: Optional[dict] = None) -> List[T]:
        query = self.db.query(self.model)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(self.model, key) == value)
        return query.all()