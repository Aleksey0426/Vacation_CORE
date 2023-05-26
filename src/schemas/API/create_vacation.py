import re

from datetime import datetime
from typing import List

from pydantic import BaseModel, validator, Field, ValidationError


class VacationType(BaseModel):
    id: int
    value: str
    description: str


class OverlapVacations(BaseModel):
    id: int
    dateFrom: str
    dateTo: str
    vacationStatus: str

    @validator("dateFrom")
    def check_date_from(cls, v):
        reg_ex = '(\d\d)\.(\d\d)\.(\d{4})'
        if re.match(reg_ex, v) and len(v) == 10:
            return v
        else:
            raise ValueError("Неверный тип даты", v)

    @validator("dateTo")
    def check_date_to(cls, v):
        reg_ex = "((\d\d)\.(\d\d)\.(\d{4})){1}"
        if re.match(reg_ex, v) and len(v) == 10:
            return v
        else:
            raise ValueError("Неверный тип даты", v)


class ResponseSuccessfully(BaseModel):
    id: int
    dateFrom: str
    dateTo: str
    vacationType: VacationType
    vacationStatus: str
    overlapVacations: list[OverlapVacations]

    @validator("dateFrom")
    def check_date_from(cls, v):
        reg_ex = "((\d\d)\.(\d\d)\.(\d{4})){1}"
        if re.match(reg_ex, v) and len(v) == 10:
            return v
        else:
            raise ValueError("Неверный тип даты", v)

    @validator("dateTo")
    def check_date_to(cls, v):
        reg_ex = "((\d\d)\.(\d\d)\.(\d{4})){1}"
        if re.match(reg_ex, v) and len(v) == 10:
            return v
        else:
            raise ValueError("Неверный тип даты", v)


def validate_response_error(json):
    try:
        ResponseErrorValidate.parse_obj(json)
    except ValidationError as error:
        print(error)


class ResponseErrorValidate(BaseModel):
    id: str
    description: str
    timestamp: datetime


# a = ResponseSuccessfully.parse_obj({
#     "id": 1466,
#     "dateFrom": "01.08.20231111",
#     "dateTo": "14.08.2023",
#     "vacationType": {
#         "id": 1,
#         "value": "Основной оплачиваемый",
#         "description": "описание для Основной оплачиваемый"
#     },
#     "vacationStatus": "На согласовании",
#     "overlapVacations": [
#         {
#             "id": 15,
#             "dateFrom": "01.08.2023",
#             "dateTo": "14.08.2023",
#             "vacationStatus": "На согласовании"
#         }
#     ]
# })
#

# json = {
#     "id": "a9ed5a3e-9b58-4145-9a09-117495ab06e2",
#     "description": "Expected array or string.\n at [Source: (org.springframework.util.StreamUtils$NonClosingInputStream); line: 3, column: 13] (through reference chain: com.irlix.microservice.vacationservice.controller.dto.vacation.VacationCreateRequest[\"dateTo\"])",
#     "timestamp": "2023-05-19T13:30:54.630628633"
# }
#
# print(validate_response_error(json))
