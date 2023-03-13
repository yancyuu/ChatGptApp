# -*- coding: utf-8 -*-

""" openai操作相关的函数
"""
import requests

from common_sdk.logging.logger import logger
from common_sdk.system import sys_env
from manager.api.openai.api_result import ApiResult
import openai


class Operate:

    def __init__(self):
        openai.api_key = sys_env.get_env("OPENAI_API_KEY")
        openai.organization = sys_env.get_env("OPENAI_ORGANIZATION")

    def completion(self, prompt, engine="text-davinci-002"):
        completion = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            max_tokens=1024,
            temperature=0,
            stop="\n\n"
        )
        logger.info(f"openai的completion返回信息 {completion}")
        return self.create_api_result(result=completion)

    def chat_completion(self, content, engine="gpt-3.5-turbo"):
        replay = openai.ChatCompletion.create(
            model=engine,
            messages=[{"role": "user", "content": content}],
        )
        logger.info(f"openai的聊天completion返回信息 {replay}")
        return self.create_api_result(result=replay)

    def list_engine(self):
        engines = openai.Engine.list()
        logger.info(f"openai的list_engine返回信息 {engines}")
        return self.create_api_result(engines)

    def list_models(self):
        models = openai.Model.list()
        logger.info(f"openai的list_engine返回信息 {models}")
        return self.create_api_result(models)

    def edit(self, input, instruction, engine):
        edit = openai.Edit.create(
            input=input,
            instruction=instruction,
            engine=engine,
            temperature=0,
        )
        logger.info(f"openai的edit返回信息 {edit}")
        return self.create_api_result(edit)

    @staticmethod
    def create_api_result(result):
        ret = ApiResult(result)
        return ret
