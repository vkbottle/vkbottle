"""
 MIT License

 Copyright (c) 2019 Arseniy Timonik

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
"""

"""
VK API WRAPPER
"""

from .portable import API_VERSION, API_URL
from .utils import HTTPRequest
from .vk.exceptions import *


class Method(object):
    """
    VK API Method

    Universal for User and Bot API. Make single async requests to VK API Server
    """
    def __init__(self, token: str, request: HTTPRequest = None):
        """
        :param token: VK API Token (universal for User and Bot API)
        :param request: aioHTTP ClientSession for ordered sessions
        """
        self.token = token
        self.request = HTTPRequest() if request is None else request

    async def __call__(self, group, method, data: dict = None):
        """
        VK API Method Wrapper
        :param group: method group
        :param method: method name
        :param data: method options
        :return: VK API Server Response
        """

        data = data or {}

        response = await self.request.post(
            url= API_URL + group + '.' + method + '/?access_token={token}&v={version}'.format(
                token=self.token,
                version=API_VERSION),
            params=data)

        try:
            return response['response']
        except KeyError:
            raise VKError([
                response['error']['error_code'],
                response['error']['error_msg']
            ])


class Api(object):
    """
    Allow to make requests like this:
    bot.api.messages.send(**kwargs)

    Receive only kwargs, no positional arguments. Kwargs can be skipped
    """
    def __init__(self, method_object: Method, group_id: int, method = None):
        """
        :param method_object: object class Method
        :param method: Needed for getattr receiver
        """
        self.method_object = method_object
        self.group_id = group_id
        self._method = method

    def __getattr__(self, method):
        if '_' in method:
            m = method.split('_')
            method = m[0] + ''.join(i.title() for i in m[1:])

        return Api(
            self.method_object,
            self.group_id,
            (self._method + '.' if self._method else '') + method
        )

    async def request(self, group, method, data: dict = None) -> dict:
        data = {k: v for k, v in data.items() if v is not None} if data else {}
        return await self.method_object(group, method, data)

    async def __call__(self, **kwargs) -> dict:
        """
        API Method Maker
        :param kwargs: all data of the request
        :return: VK Server Response
        """

        for k, v in enumerate(kwargs):
            if isinstance(v, (list, tuple)):
                kwargs[k] = ','.join(str(x) for x in v)

        method = self._method.split('.')

        if len(method) == 2:
            group = method[0]
            method = method[1]

            return await self.method_object(group, method, kwargs)
