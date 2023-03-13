from __future__ import annotations
from . import get_global_token, CisprSessionExpiredError
import logging
from base64 import b64encode, b64decode
from typing import Literal
import requests
from pydantic import BaseModel, Field
import bs4
import re


class AttendanceLinkParsingError(Exception):
    pass

class AttendanceCodeParsingError(Exception):
    pass

class UnitId:
    APP = 5
    BSAD = 6
    CF = 2
    DAD = 3
    GEN = 95
    IND = 1
    NCS = 7
    PoP = 4


CODE_REGEX = r"^([A-Z,a-z,0-9]{1,5})(_)([LS])(_)(\d{1,2})(_)(\d{8})$"
UNIT_NAME = (
    Literal["APP"] | Literal["BSAD"] | Literal["CF"] | Literal["DAD"] |
    Literal["4GEN"] | Literal["IND"] | Literal["NCS"] | Literal["PoP"]
)


class AttendanceCode(BaseModel):
    progress_code: str = Field(..., regex=CODE_REGEX)
    week: str = Field(..., regex=r"^[0-9]+$")
    academic_year: str = Field(..., regex=r"^[0-9]{2}\/[0-9]{2}$")
    level: str = Field(..., regex=r"^Level [04567]$")
    type: str = Field(..., regex=r"^(L|S)$")
    unit_id: str = Field(..., regex=r"^[0-9]$")


    @property
    def link(self):
        level = self.level[len("Level "):]
        data = "{level}/{unit_id}/{week}/{type}/{code}".format(
            level=level,
            unit_id=self.unit_id,
            week=self.week,
            type=self.type,
            code=self.progress_code,
        )
        encoded_data = b64encode(b64encode(data.encode())).decode()
        return f"https://cispr.bournemouth.ac.uk/deeplink/qr/{encoded_data}"

    @staticmethod
    def from_code(progress_code: str, academic_year: str, level: str) -> AttendanceCode:
        # PoP_L_23_66202646
        try:
            unit, type, week, _ = progress_code.split("_")
        except Exception:
            raise AttendanceCodeParsingError()
        
        UNIT_ID_LOOKUP = {
            "APP":"5",
            "BSAD":"6",
            "CF":"2",
            "DAD":"3",
            "4GEN":"95",
            "IND":"1",
            "NCS":"7",
            "PoP":"4",
        }
        unit_id = UNIT_ID_LOOKUP.get(unit)
        if unit_id == None:
            raise AttendanceCodeParsingError
        
        return AttendanceCode(
            progress_code=progress_code,
            academic_year=academic_year,
            level=level,
            week=week,
            unit_id=unit_id,
            type=type,
        )


    @staticmethod
    def from_link(link: str) -> AttendanceCode:
        LINK_1_REGEX = r"^https:\/\/cispr.bournemouth.ac.uk\/study-progress\/submit\/[0-9a-zA-Z\+\/]*\/[0-9a-zA-Z\+\/]*"
        LINK_2_REGEX = r"^https:\/\/cispr.bournemouth.ac.uk\/deeplink\/qr\/[0-9a-zA-Z\+\/]*"
        is_valid_link = re.fullmatch(LINK_1_REGEX, link) or re.fullmatch(LINK_2_REGEX, link)
        
        if not is_valid_link:
            raise AttendanceLinkParsingError
        
        try:
            b64 = link.split("/")[-1]
            info_string = b64decode(b64decode(b64)).decode()
            level, unit_id, week, type, code = info_string.split("/")
            
            return AttendanceCode(
                progress_code=code,
                unit_id=unit_id,
                academic_year="22/23",
                level="Level " + level,
                type=type,
                week=week,
            )
        except Exception:
            raise AttendanceLinkParsingError

