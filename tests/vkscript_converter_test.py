from vkbottle import vkscript

BASIC_CYCLE = "var a=%A%;var some_list=[];while(a<100){API.users.get({user_id:a});a = a + 1;};return some_list;"


@vkscript
def basic_cycle(api, a: int = 10):
    some_list = []
    while a < 100:
        api.users.get(user_id=a)
        a += 1
    return some_list


@vkscript
def types(api):
    a = 5.1
    b = 5 * a
    results = [b, b - 2]
    _ = {"a": 1, "b": 2}
    _ = True
    _ = 3 - 3.3 + 3.0 * 0.3 / 33 % 3
    _ = "string"

    if a < 5:
        pass
    elif b > 25:
        a += 1
        a -= 1
    else:
        while a < b:
            a *= 1.1

    for i in results:
        results.append(i ** 2)
    results.pop()
    return results


def test_vkscript():
    assert basic_cycle(a=10) == BASIC_CYCLE.replace("%A%", "10")
    assert basic_cycle(a=94) == BASIC_CYCLE.replace("%A%", "94")
    assert types()
