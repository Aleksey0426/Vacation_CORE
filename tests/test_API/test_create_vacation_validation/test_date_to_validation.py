import datetime

import pytest
import requests
from datetime import date, timedelta

from config import URL_VACATION_SERVICE, PATH_VACATION
from src.schemas.API.create_vacation import ResponseSuccessfully, validate_response_error


@pytest.mark.parametrize('date_from , date_to', [
    ['14.08.2023', '30.08.2023'],
    ['14.08.2023', '31.08.2023'],
    ['14.08.2023', '02.09.2023'],
    ['14.08.2023', '01.09.2023'],
    ['01.10.2023', '01.11.2023'],
    ['01.10.2023', '01.12.2023'],
    ['15.12.2023', '01.02.2024'],
    ['15.12.2023', '01.01.2024']

])
def test_date_to_successfully(get_new_token_collaborator, set_log, date_to, date_from):
    request = get_new_token_collaborator
    response_token = request.json()

    headers = {'Authorization': 'Bearer ' + response_token['access_token']}
    payload = {
        'dateFrom': date_from,
        'dateTo': date_to,
        'vacationTypeId': '1'
    }
    r = requests.post(f'{URL_VACATION_SERVICE}{PATH_VACATION}', headers=headers,
                      json=payload)

    if r.status_code != 201:
        # write log in file
        write_log = set_log(r, PATH_VACATION, payload, headers)

    schema = ResponseSuccessfully.parse_obj(r.json())

    assert r.status_code == 201
    assert schema is not ValueError


@pytest.mark.parametrize('date_from , date_to', [
    ['14.08.2023', '32.08.2023'],
    ['14.08.2023', '00.09.2023'],
    ['14.02.2024', '01.13.2024'],
    ['14.02.2024', '01.00.2024'],
    ['14.08.2023', '-1.08.2023'],
    ['14.02.2024', '"String"'],
    ['14.08.2023', 'String'],
    ['14.12.1969', 1],
    ['14.12.1969', -1],
    ['14.12.1969', 0],
    ['14.08.2023', '30-08-2023'],
    ['14.08.2023', '30/08/2023'],
    ['14.08.2023', '30082023'],
    ['14.08.2023', '2023-08-30'],
    ['14.08.2023', 'null'],
    ['14.08.2023', 'true'],
    ['14.08.2023', ''],
    ['14.08.2023', '!@#$%^&']
])
def test_date_to_error_validation(get_new_token_collaborator, set_log, date_to, date_from):
    request = get_new_token_collaborator
    response_token = request.json()

    headers = {'Authorization': 'Bearer ' + response_token['access_token']}
    payload = {
        'dateFrom': date_from,
        'dateTo': date_to,
        'vacationTypeId': '1'
    }
    r = requests.post(f'{URL_VACATION_SERVICE}{PATH_VACATION}', headers=headers,
                      json=payload)

    parse = validate_response_error(r.json())

    if r.status_code != 400:
        # write log in file
        write_log = set_log(r, PATH_VACATION, payload, headers)

    assert r.status_code == 400
    assert parse is None


def test_without_date_to(get_new_token_collaborator, set_log):
    request = get_new_token_collaborator
    response_token = request.json()

    headers = {'Authorization': 'Bearer ' + response_token['access_token']}
    payload = {
        'dateFrom': '01.08.2023',
        'vacationTypeId': '1'
    }
    r = requests.post(f'{URL_VACATION_SERVICE}{PATH_VACATION}', headers=headers,
                      json=payload)

    parse = validate_response_error(r.json())

    if r.status_code != 400:
        # write log in file
        write_log = set_log(r, PATH_VACATION, payload, headers)

    assert r.status_code == 400
    assert parse is None
