from vkbottle import CodeException


def test_code_exception():
    class CodeError(CodeException):
        pass

    try:
        raise CodeError[1]
    except CodeError[2] as e:
        raise AssertionError from e
    except CodeError[3, 4] as e:
        raise AssertionError from e
    except CodeError[1, 2, 5] as e:
        assert e.code == 1  # noqa: PT017
