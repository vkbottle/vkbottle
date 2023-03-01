import pickle

from vkbottle.exception_factory import CodeException, VKAPIError


class CodeError(CodeException):
    pass


class CodeError1(CodeError, code=1):
    pass


def test_code_exception_getitem_given_single_code_returns_subclass_with_specified_code():
    assert issubclass(CodeError[6], CodeError)
    assert CodeError[9].code == 9


def test_code_exception_getitem_given_multiple_codes_returns_multiple_subclasses_with_specified_codes():
    error_1, error_2 = CodeError[6, 9]
    assert issubclass(error_1, CodeError)
    assert issubclass(error_2, CodeError)
    assert error_1.code == 6
    assert error_2.code == 9


def test_specific_code_exception_contains_its_code():
    assert CodeError1.code == 1


def test_code_exception_is_saved_in_module():
    assert CodeError[2] is CodeError[2]
    assert CodeError[1] is CodeError1


def test_specific_code_exception_overrides_general_code_exception():
    _ = CodeError[42]

    class CodeError42(CodeError, code=42):
        pass

    assert CodeError[42] is CodeError42


def test_code_exception_can_be_pickled():
    error = VKAPIError[13](error_msg="test")
    assert pickle.loads(pickle.dumps(error)).error_msg == "test"
