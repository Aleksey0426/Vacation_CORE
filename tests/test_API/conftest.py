import os
from datetime import datetime, date

import pytest
import requests

from config import AUTH_URL


@pytest.fixture(scope='session')
def get_new_token_collaborator():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {
        'grant_type': 'password',
        'username': 'aleksey.chugunov@irlix.ru',
        'password': 'irlix2023',
        'client_id': 'core',
        'client_secret': 'd11e83a3-95cc-460c-9289-511d36d3e3fb'
    }
    r = requests.post(f'{AUTH_URL}/auth/realms/freeipa-realm/protocol/openid-connect/token', headers=headers,
                      data=payload)
    response = requests.Response.json(r)

    token_collaborators = response['access_token']

    return r


def write_log_request(r=None, path=None, payload=None, headers=None):
    now_time = datetime.timestamp(datetime.now())
    date_1 = date.today()
    file_path = f'./logs/api/{path}_{r.request.method}_{date_1}'
    file = open(file_path, 'a')
    file.write('Request start\n')
    file.write('%s\n' % r.request)
    file.write('%s\n' % r.url)
    file.write('%s\n' % r.headers)
    file.write('%s\n' % headers)
    file.write('%s\n' % payload)
    file.write('Response \n')
    file.write('%s\n' % r.status_code)
    file.write('%s\n' % r.json())
    file.write('%s\n')
    file.write('Request end\n')
    file.write('\n')

@pytest.fixture(scope='session')
def set_log():
    return write_log_request


# def check_date():
#     reg_ex = "((\d\d)\.(\d\d)\.(\d{4})){1}"
#     if re.match(reg_ex, v) and len(v) == 10:
#         return v
#     else:
#         raise ValueError("Неверный тип даты")
