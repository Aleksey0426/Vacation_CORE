from typing import List

import pytest
import requests

from src.enums.GlobalEnums import GlobalErrorEnum
from src.schemas.API.create_vacation import ResponseSuccessfully, ResponseErrorValidate, validate_response_error, \
    successfully_response
from config import URL_VACATION_SERVICE, PATH_VACATION


@pytest.mark.parametrize('date_from , date_to , vacation_type_id', [
    ['01.08.2023', '14.08.2023', '1'],
    ['01.08.2023', '01.08.2023', '1'],
])
def test_date_period_successfully(get_new_token_collaborator, set_log, date_to, date_from, vacation_type_id):
    request = get_new_token_collaborator
    response_token = request.json()

    headers = {'Authorization': 'Bearer ' + response_token['access_token']}
    payload = {
        'dateFrom': date_from,
        'dateTo': date_to,
        'vacationTypeId': vacation_type_id
    }
    r = requests.post(f'{URL_VACATION_SERVICE}{PATH_VACATION}', headers=headers,
                      json=payload)

    schema = successfully_response(r.json())

    if r.status_code != 201 or schema != "Done":
        # write log in file
        write_log = set_log(r, PATH_VACATION, payload, headers)

    assert r.status_code == 201, f'{GlobalErrorEnum.WRONG_STATUS_ERROR.value}'
    assert schema == "Done", f'{GlobalErrorEnum.WRONG_VALIDATION_ERROR.value} = {schema}'


@pytest.mark.parametrize('date_from , date_to, vacation_type_id', [
    ['14.08.2023', '01.08.2023', '1'],
    ['01.08.2022', '14.08.2022', '1'],
    ['20.08.2023', '01.08.2023', '1'],
    ['15.05.2023', '01.06.2023', '1'],
    ['0108.2023', '15.08.2023', '1'],
    ['02.08.2023', '1408.2023', '1'],
    ['02.08.2023', '1408.2023', '+1']
])
def test_date_period_unsuccessful(get_new_token_collaborator, set_log, date_to, date_from, vacation_type_id):
    request = get_new_token_collaborator
    response_token = request.json()

    headers = {'Authorization': 'Bearer ' + response_token['access_token']}
    payload = {
        'dateFrom': date_from,
        'dateTo': date_to,
        'vacationTypeId': vacation_type_id
    }
    r = requests.post(f'{URL_VACATION_SERVICE}{PATH_VACATION}', headers=headers,
                      json=payload)

    parse = validate_response_error(r.json())

    if r.status_code != 400 or parse != "Done":
        # write log in file
        write_log = set_log(r, PATH_VACATION, payload, headers, parse)

    assert r.status_code == 400, f'{GlobalErrorEnum.WRONG_STATUS_ERROR.value}'
    assert parse == "Done", f'{GlobalErrorEnum.WRONG_VALIDATION_ERROR.value} : {parse}'
