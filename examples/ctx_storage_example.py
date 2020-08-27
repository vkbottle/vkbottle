from vkbottle import CtxStorage

ctx_storage = CtxStorage()
ctx_storage.set("a", 100)

# In any part of code in runtime

print(CtxStorage().get("a"))  # 100
