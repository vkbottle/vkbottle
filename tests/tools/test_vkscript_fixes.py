from vkbottle import vkscript


@vkscript
def _for_loop(api, items):
    result = []
    for x in items:
        api.users.get(user_id=x)
        result.append(x)
    return result


@vkscript
def _bare_return(api):
    return


@vkscript
def _string_subscript(api, data):
    return data["key"]


def test_vkscript_for_loop_is_forward_and_nondestructive():
    code = _for_loop(items=[1, 2, 3]).code

    # The previous implementation iterated with .pop(), which reverses the order and
    # destroys the source array. A correct loop must not pop.
    assert ".pop()" not in code


def test_vkscript_bare_return():
    # A bare `return` must convert to `return null;`, not raise (emptiness must be
    # checked on the value, not the node).
    assert "return null;" in _bare_return().code


def test_vkscript_string_subscript():
    # A string-key subscript must convert to property access (data.key), not raise
    # AttributeError from a non-existent `.s` on the string.
    assert "data.key" in _string_subscript(data={}).code
