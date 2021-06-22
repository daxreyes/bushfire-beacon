import uuid
from datetime import datetime
import enum

import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import (
    UUIDType,
    Timestamp,
    ChoiceType,
    PhoneNumberType,
    URLType,
)

from .database import Base


class User(Base, Timestamp):
    __tablename__ = "user"
    id = sa.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    email = sa.Column(sa.String, unique=True, index=True, nullable=False)
    phone_number = sa.Column(PhoneNumberType())
    full_name = sa.Column(sa.String, index=True, nullable=True)
    hashed_password = sa.Column(sa.String, nullable=False)
    is_active = sa.Column(sa.Boolean, default=True, nullable=False)
    is_verified = sa.Column(sa.Boolean, default=False, nullable=False)
    is_superuser = sa.Column(sa.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<User id:{self.id}, email:{self.email} is_active:{self.is_active}>"


class ByAt(Timestamp):
    """Mixin Class to include creators and modifiers"""

    # https://stackoverflow.com/questions/44434410/sqlalchemy-multiple-foreign-key-pointing-to-same-table-same-attribute
    # https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/mixins.html#mixing-in-relationships

    @declared_attr
    def created_by_id(cls):
        return sa.Column("created_by_id", sa.ForeignKey("user.id"))

    @declared_attr
    def modified_by_id(cls):
        return sa.Column("modified_by_id", sa.ForeignKey("user.id"))

    @declared_attr
    def created_by(cls):
        return relationship("User", foreign_keys=[cls.created_by_id])

    @declared_attr
    def modified_by(cls):
        return relationship("User", foreign_keys=[cls.modified_by_id])


class Item(ByAt, Base):
    """
    Item
    """

    __tablename__ = "item"

    id = sa.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    name = sa.Column(sa.Unicode, index=True)
    address = sa.Column(sa.Unicode)
    lat = sa.Column(sa.Float)
    lng = sa.Column(sa.Float)
    map_url = sa.Column(sa.Unicode)
    phone = sa.Column(sa.Unicode)
    website = sa.Column(URLType)

    # functionality to find and group related questions display sequentially
    # with content displayed first
    def __repr__(self):
        return f"<Hospital id:{self.id}, clean name:{self.clean_name}>"

    beds = relationship("Bed", backref="hospital")


class SourceType(str, enum.Enum):
    CROWD = "crowd"
    VOLUNTEER = "volunteer"
    HOSPITAL = "hospital"
    DOH = "doh"


class Bed(ByAt, Base):
    """
    Beds
    """

    __tablename__ = "bed"

    id = sa.Column(sa.Integer, primary_key=True)
    doh_id = sa.Column(sa.Integer, index=True)
    hosp_id = sa.Column(UUIDType(binary=False), sa.ForeignKey("hospital.id"), index=True)
    icu_vacant = sa.Column(sa.Integer)
    icu_occupied = sa.Column(sa.Integer)
    isolbed_vacant = sa.Column(sa.Integer)
    isolbed_occupied = sa.Column(sa.Integer)
    beds_ward_vacant = sa.Column(sa.Integer)
    beds_ward_occupied = sa.Column(sa.Integer)
    reportdate = sa.Column(sa.DateTime)
    updated = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False)
    source = sa.Column(ChoiceType(SourceType))

    __table_args__ = (
        sa.UniqueConstraint("hosp_id", "updated", "reportdate", name="uq_bed_hospid_upd_rep"),
        sa.Index(None, updated.desc(), hosp_id),
    )

    @hybrid_property
    def doh_code(self):
        return self.hospital.doh_code

    def __repr__(self):
        return f"<Bed id:{self.id}, doh_id:{self.doh_id}, hosp_id: {self.hosp_id}, doh_code: {self.doh_code}>"
