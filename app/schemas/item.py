from typing import Optional, List, TypeVar, Generic
from pydantic.fields import ModelField
from datetime import datetime
from loguru import logger

from phonenumbers import (
    NumberParseException,
    PhoneNumberFormat,
    PhoneNumberType,
    format_number,
    is_valid_number,
    number_type,
    parse as parse_phone_number,
)

from pydantic import BaseModel, Field, root_validator, constr, validator, HttpUrl
from uuid import UUID
from .byat import ByAtBase

MOBILE_NUMBER_TYPES = (
    PhoneNumberType.MOBILE,
    PhoneNumberType.FIXED_LINE_OR_MOBILE,
    PhoneNumberType.FIXED_LINE,
)

# https://github.com/samuelcolvin/pydantic/issues/181#issuecomment-707186930
PydanticField = TypeVar("PydanticField")


class EmptyStrToNone(Generic[PydanticField]):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: PydanticField, field: ModelField) -> Optional[PydanticField]:
        if v == "":
            return None
        return v


class ItemBase(BaseModel):
    name: Optional[str] = Field(..., description="Name of the hospital")
    clean_name: Optional[str]
    address: Optional[str] = None
    region: Optional[str] = None
    municipality: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    map_url: Optional[str] = None
    doh_code: Optional[str] = None
    website: Optional[EmptyStrToNone[HttpUrl]] = None
    phone: Optional[constr(max_length=50, strip_whitespace=True)] = None
    # last_update: datetime

    @root_validator
    def clean_hospital_name(cls, values):
        # logger.debug(f"values {values}")
        values["clean_name"] = (
            values.get("name").strip() if values.get("name") else values.get("name")
        )
        return values

    # https://github.com/samuelcolvin/pydantic/issues/1551#issuecomment-700154597
    @validator("phone")
    def check_phone_number(cls, v):
        logger.debug(f"validating phone: {v}")
        if v is None:
            return v

        try:
            n = parse_phone_number(v, "PH")
        except NumberParseException as e:
            logger.error(f"Phone not valid {v}")
            raise ValueError("Phone parse error, please provide a valid phone number") from e

        if not is_valid_number(n) or number_type(n) not in MOBILE_NUMBER_TYPES:
            logger.debug(f"valid: {is_valid_number(n)}, num type: {number_type(n)}")
            raise ValueError("Please provide a valid phone number")
        p = format_number(
            n,
            PhoneNumberFormat.NATIONAL if n.country_code == 63 else PhoneNumberFormat.INTERNATIONAL,
        )
        logger.debug(f"formated phone {p}")
        return p


class ItemCreate(ItemBase):
    name: str = Field(..., description="Name of the hospital")
    address: str = Field(..., description="Complete Adddress")
    region: str
    municipality: str
    lat: Optional[float] = Field(None, decription="Latitute")
    lng: Optional[float] = Field(None, description="Longitude")


# Properties to receive on hospital update
class ItemUpdate(ItemBase):
    name: Optional[str] = None


class ItemInDBBase(ItemBase, ByAtBase):
    id: Optional[UUID] = None

    class Config:
        orm_mode = True


# Properties to return to client
class Item(ItemInDBBase):
    id: Optional[UUID] = None
    # name = None


class ItemOut(BaseModel):
    doh_code: Optional[str] = None
    clean_name: Optional[str] = Field(..., description="Name of the hospital")
    address: Optional[str] = None
    region: Optional[str] = None
    municipality: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    website: Optional[HttpUrl] = None
    phone: Optional[constr(max_length=50, strip_whitespace=True)] = None

    class Config:
        orm_mode = True


class ItemBed(BaseModel):
    id: Optional[UUID] = None
    doh_code: Optional[str]
    created: datetime
    last_update: datetime
    available: Optional[int]
    icu_vacant: Optional[int]
    isolbed_vacant: Optional[int]
    beds_ward_vacant: Optional[int]


# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    pass
