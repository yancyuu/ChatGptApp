# -*- coding: utf-8 -*-

SUCCESS = (0, 'success')
SERVER_ERROR = (-1, '服务器错误')
PAGE_NOT_FOUND = (404, '页面未找到')
CUSTOM_MESSAGE_ERROR = (9, '{message}')

# 身份验证相关
MISSING_WX_CODE = (10001, '缺少WX_CODE参数')
MISSING_REDIRECT_URL = (10002, '缺少HREF参数')
INCORRECT_SECRET = (10003, '应用密钥错误')

# 顾客登录相关
LOGIN_FAILED = (20001, '请求第三方授权平台失败')
GET_SHARE_INFO_FAILED = (20002, '获取第三方授权平台用户信息失败')
LOGIN_METHOD_ERROR = (20003, '用户登录方式错误')
INVALID_BUFFER = (20004, '非本平台用户信息')
INSUFFICIENT_AUTH_SCOPE = (20005, '授权作用域错误')
INVALID_TOKEN = (20006, 'iam token错误')
TOKEN_EXPIRED = (20007, 'iam token已过期')
INVALID_LOGIN = (20008, '用户无权登录此应用')
API_FAILED = (20009, '请求第三方api失败')