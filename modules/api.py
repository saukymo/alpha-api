# coding: utf-8
import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

BASE_URL = "http://cloud.yjxgh.com/"

request_header = {
    "apikey": "aa0ee7e6ef7149f9b3310b6be2fdc26c",
    "Content-Type": "application/json"
}

file_header = {
    "apikey": "aa0ee7e6ef7149f9b3310b6be2fdc26c"
}


PARTNER_ID = "ict"
APP_ID = "pdcare"
APP_OS = 1
INVITE_CODE = "test1234"


def register_user(user_info):
    end_point = "v1/user/register"
    user_info.update({
        "inviteCode": INVITE_CODE
    })

    request_body = {
        "partnerId": PARTNER_ID,
        "appId": APP_ID,
        "userInfo": user_info,
    }
    print(BASE_URL + end_point)
    print(request_header)
    print(request_body)
    r = requests.post(BASE_URL + end_point, data=json.dumps(request_body), headers=request_header)
    response = r.json()
    print(response)
    return response


def upload_data(data_body):
    end_point = "v1/data/upload"
    request_body = {
        "partnerId": PARTNER_ID,
        "appId": APP_ID,
        "appOS": APP_OS,
        "data": [data_body]
    }
    print(BASE_URL + end_point)
    print(request_header)
    print(request_body)
    # r = requests.post(BASE_URL + end_point, data=request_body, headers=request_header)
    r = requests.post(BASE_URL + end_point, data=json.dumps(request_body), headers=request_header)
    response = r.json()
    print(response)
    return response


def upload_file(request_body, filename):
    end_point = "v1/file/upload"
    request_body.update({
        "partnerId": PARTNER_ID,
        "appId": APP_ID,
        "appOS": "%d" % APP_OS,
        "data": (filename, open("uploads/" + filename, "rb"), 'text/' + request_body.get("fileType"))
    })
    print(BASE_URL + end_point)
    print(request_header)
    print(request_body)
    multipart_data = MultipartEncoder(request_body)
    file_header.update({'Content-Type': multipart_data.content_type})
    r = requests.post(BASE_URL + end_point, data=multipart_data, headers=file_header)
    response = r.json()
    print(response)
    return response
