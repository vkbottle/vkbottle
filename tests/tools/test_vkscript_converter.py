from vkbottle import vkscript

BASIC_CYCLE = "var a=%A%;var some_list=[];while(a<100){API.users.get({user_id:a});a = a + 1;some_list.push(a);};return some_list;"
API_REQUEST = "var group_id=%A%;return API.groups.getById({group_id:group_id});"


@vkscript
def basic_cycle(api, a: int = 10):
    some_list = []
    while a < 100:
        api.users.get(user_id=a)
        a += 1
        some_list.append(a)
    return some_list


@vkscript
def api_request(api, group_id):
    return api.groups.get_by_id(group_id=group_id)


@vkscript
def types(api):
    a = 5.1
    b = 5 * a
    results = [b, b - 2, "a"]
    _a = {"a": 1, "b": 2}
    _a = True
    _a = 3 - 3.3 + 3.0 * 0.3 / 33 % 3
    _a = "string" + "string"

    if a < 5:
        pass
    elif b > 25:
        a += 1
        a -= 1
    else:
        while a < b:
            a *= 1.1

    results.extend([_a, b])
    results.pop()
    return results


def test_vkscript():
    assert basic_cycle(a=10) == BASIC_CYCLE.replace("%A%", "10")
    assert basic_cycle(a=94) == BASIC_CYCLE.replace("%A%", "94")
    assert api_request(group_id=1) == API_REQUEST.replace("%A%", "1")
    assert types()
