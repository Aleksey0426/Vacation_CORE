import datetime

import pytest
import requests
from datetime import date, timedelta

from config import URL_VACATION_SERVICE, PATH_VACATION
from src.schemas.API.create_vacation import validate_response_error


@pytest.mark.parametrize('vacation_type_id', [
    '0',
    'null',
    None,
    '9223372036854775808',
    '-1',
    '-9223372036854775807',
    '-9223372036854775808',
    '-9223372036854775809',
    '++1',
    '1,1',
    '1.1',
    'Ааа',
    '"Ааа"',
    'true',
    '@#$%^&*()',
    '"@#$%^&*()"',
    '0.001E03',
    '2а'
])
def test_vacation_type_error_validation(get_new_token_collaborator, set_log, vacation_type_id):
    request = get_new_token_collaborator
    response_token = request.json()

    headers = {'Authorization': 'Bearer ' + response_token['access_token']}
    payload = {
        'dateFrom': '02.08.2023',
        'dateTo': '15.08.2023',
        'vacationTypeId': vacation_type_id
    }
    r = requests.post(f'{URL_VACATION_SERVICE}{PATH_VACATION}', headers=headers,
                      json=payload)
    # write log in file
    # write_log = set_log(r, PATH_VACATION, payload)

    parse = validate_response_error(r.json())

    if r.status_code != 400:
        # write log in file
        write_log = set_log(r, PATH_VACATION, payload, headers)

    assert r.status_code == 400
    assert parse is None


@pytest.mark.parametrize('vacation_type_id', [
    '9223372036854775806',
    '9223372036854775807'
])
def test_vacation_type_error_lack_of_recording(get_new_token_collaborator, set_log, vacation_type_id):
    request = get_new_token_collaborator
    response_token = request.json()

    headers = {'Authorization': 'Bearer ' + response_token['access_token']}
    payload = {
        'dateFrom': '02.08.2023',
        'dateTo': '15.08.2023',
        'vacationTypeId': vacation_type_id
    }
    r = requests.post(f'{URL_VACATION_SERVICE}{PATH_VACATION}', headers=headers,
                      json=payload)

    parse = validate_response_error(r.json())

    if r.status_code != 404:
        # write log in file
        write_log = set_log(r, PATH_VACATION, payload, headers)

    assert r.status_code == 404
    assert parse is None
