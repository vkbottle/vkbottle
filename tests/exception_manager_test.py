from vkbottle import CodeErrorFactory, SingleError

def test_exc_manager_code_error():
    exc_manager = CodeErrorFactory()

    try:
        raise exc_manager(7)
    except exc_manager(6):
        assert False
    except exc_manager(7):
        assert True
    except exc_manager():
        assert False


def test_exc_manager_single_error():
    class SomeError(SingleError):
        pass

    try:
        raise SomeError("Some error occurred")
    except SomeError:
        pass
    except BaseException as e:
        assert False
