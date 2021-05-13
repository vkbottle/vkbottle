from vkbottle.exception_factory import VKAPIError

try:
    raise VKAPIError(2, "Some exception occurred")
except VKAPIError(3) as e:
    print("Oh, third exception.")
except VKAPIError(2) as e:
    print("Oh, second exception.")
except VKAPIError():
    print("Unknown vk error")
