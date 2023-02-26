# -*- coding: utf-8 -*-

import requests

from ..system import sys_env


def get_user_by_token(token):
    service_url = sys_env.get_env("IAM_SERVICE_URL")
    response = requests.post('{}/staff/get'.format(service_url), headers={'token': token}, json={})
    res_json = response.json()
    return res_json['data']


def get_user_id_by_token(token):
    service_url = sys_env.get_env("IAM_SERVICE_URL")
    response = requests.post('{}/staff/get'.format(service_url), headers={'token': token}, json={})
    res_json = response.json()
    return res_json['data']['id']


def get_wecom_by_user_id(user_id, token):
    service_url = sys_env.get_env("IAM_SERVICE_URL")
    response = requests.post('{}/wecom/get_by_staff_id'.format(service_url), 
                headers={'token': token}, json={'staff_id': user_id})
    res_json = response.json()
    return res_json['data']
