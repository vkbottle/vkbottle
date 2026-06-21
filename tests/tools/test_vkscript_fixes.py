from vkbottle import vkscript


@vkscript
def _for_loop(api, items):
    result = []
    for x in items:
        api.users.get(user_id=x)
        result.append(x)
    return result


def test_vkscript_for_loop_is_forward_and_nondestructive():
    code = _for_loop(items=[1, 2, 3]).code

    # The previous implementation iterated with .pop(), which reverses the order and
    # destroys the source array. A correct loop must not pop.
    assert ".pop()" not in code
