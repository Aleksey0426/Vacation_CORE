import datetime

import pytest
import requests
from datetime import date, timedelta

from pydantic import json

from src.schemas.API.create_vacation import ResponseSuccessfully, ResponseErrorValidate, validate_response_error

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

    if r.status_code != 201:
        # write log in file
        write_log = set_log(r, PATH_VACATION, payload, headers)

    schema = ResponseSuccessfully.parse_obj(r.json())

    assert r.status_code == 201
    assert schema is not ValueError


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

    if r.status_code != 400:
        # write log in file
        write_log = set_log(r, PATH_VACATION, payload, headers)

    parse = validate_response_error(r.json())

    # if parse is not None:
    #     write_log = set_log(r, PATH_VACATION, payload, headers)

    assert r.status_code == 400
    assert parse is None
