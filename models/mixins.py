from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
import uuid
from app import db


class BaseMixin(object):
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


def foreign_key(table, field="id", on_delete="CASCADE", **kwargs):
    nullable = kwargs.pop('nullable', False)
    return db.Column(db.Integer, db.ForeignKey(f'{table}.{field}', ondelete=on_delete), nullable=nullable, **kwargs)
