from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
import uuid

from sqlalchemy_mixins import AllFeaturesMixin, TimestampsMixin

from app import db


class BaseModel(db.Model, AllFeaturesMixin, TimestampsMixin):
    __abstract__ = True
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )


BaseModel.set_session(db.session)


def foreign_key(table, field="id", on_delete="CASCADE", **kwargs):
    nullable = kwargs.pop("nullable", False)
    return db.Column(
        UUID(as_uuid=True),
        db.ForeignKey(f"{table}.{field}", ondelete=on_delete),
        nullable=nullable,
        **kwargs,
    )
