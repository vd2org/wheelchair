# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from typing import ClassVar


class RequestError(Exception):
    _exceptions = {}
    name = None

    def __init__(self, code: int, error: str, reason: str):
        self.__code = code
        self.__error = error
        self.__reason = reason

    @property
    def code(self) -> int:
        return self.__code

    @property
    def error(self) -> str:
        return self.__error

    @property
    def reason(self) -> str:
        return self.__reason

    def __str__(self):
        return f"{self.__code} {self.__error}: {self.__reason}"

    @classmethod
    def register_exception(cls, exception: ClassVar['RequestError']) -> ClassVar['RequestError']:
        assert exception.name is not None
        assert exception.name not in cls._exceptions
        assert issubclass(exception, RequestError)

        cls._exceptions[exception.name] = exception
        return exception

    @classmethod
    def get_exception(cls, code: int, data: dict) -> 'RequestError':
        error, reason = data['error'], data['reason']

        exception = cls._exceptions.get(error, RequestError)

        return exception(code, error, reason)


@RequestError.register_exception
class BadRequestError(RequestError):
    name = 'bad_request'


@RequestError.register_exception
class NotFoundError(RequestError):
    name = 'not_found'


@RequestError.register_exception
class UnauthorizedError(RequestError):
    name = 'unauthorized'


@RequestError.register_exception
class FileExists(RequestError):
    name = 'file_exists'
