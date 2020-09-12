from vkbottle import vkscript

VKSCRIPT = "var a=%A%;var some_list=[];while(a<100){API.users.get({user_id:a});a = a + 1;};return some_list;"


@vkscript
def my_execute_code(api, a: int = 10):
    some_list = []
    while a < 100:
        api.users.get(user_id=a)
        a += 1
    return some_list


def test_vkscript():
    assert my_execute_code(a=10) == VKSCRIPT.replace("%A%", "10")
    assert my_execute_code(a=94) == VKSCRIPT.replace("%A%", "94")
