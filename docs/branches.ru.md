# Бранчи
Бранчи — это удобная и быстрая short-term замена FSM, цепи событий, позволяющие делать всё: от тестов, анкет и опросов до чатов, обработчиков и т. п.

## Инструкции по посадке
### Импорты
В VKBottle представлены два вида бранчей: **росток (sprout)** и **ветка (branch)**.
Первый вид  — **росток**  — невероятно минималистичный и простой. Чтобы его использовать, импортируем следующие классы:
```python
from vkbottle.branch import Branch, ExitBranch 
```
Чтобы использовать **ветку**, необходимо импортировать эти объекты:
```python
from vkbottle.branch import ClsBranch, rule_disposal
```

## Работаем с бранчами
### Создание обработчика
Теперь создадим хендлер, в котором пользователь попадёт в нашу цепь:
```python
@bot.on.message(text="хочу в бранч", lower=True)
async def wrapper(ans: Message):
    await ans("Теперь ты в бранче!")
    await bot.branch.add(ans.peer_id, "my_branch")
```

А сейчас приступим к написанию кода для нашего **ростка**:
```python
@bot.branch.simple_branch("my_branch")
async def branch(ans: Message):
    if ans.text.lower() == "выйти":
        await ans("Окей, вывожу!")
        await bot.branch.exit(ans.peer_id)

    await ans("Ты в бранче. Пиши «выйти», чтобы выйти отсюда.")
```
Тоже самое можно провернуть и с **ветками** — более продвинутым инструментом:
```python
@bot.branch.cls_branch("my_branch")
class Branch(ClsBranch):
    @rule_disposal(VBMLRule("выйти", lower=True))
    async def exit_branch(self, ans: Message):
        await ans("Окей, вывожу!")
        await bot.branch.exit(ans.peer_id)
    
    async def branch(self, ans: Message, *args):
        await ans("Ты в бранче. Пиши «выйти», чтобы выйти отсюда.")
```
Теперь, если пользователь напишет **«Хочу в бранч»**, бот ответит ему **«Теперь ты в бранче»**. В дальнейшем на любое сообщение пользователя поступит ответ **«Ты в бранче. Пиши «выйти», чтобы выйти отсюда.»**, но если он напишет **«Выйти»**, то цепочка разорвется.

### Kwargs в бранчах
При инициализации бранча возможно передать все необходимые значения. Они будут переданы в хендлер бранча.
#### На примере ростков
```python
@bot.on.message(text="ставлю боту <mark:int>", lower=True)
async def wrapper(ans: Message, mark):
    await ans("Теперь расскажи, что ты думаешь о нем:")
    await bot.branch.add(ans.peer_id, "my_branch", mark=mark)

@bot.branch.simple_branch("my_branch")
async def branch(ans: Message, mark):
    if ans.text.lower() in ["это все", "да"]:
        await ans(f"Окей, твоя оценка «{mark}» и рассказ о боте заcчитан!")
        await bot.branch.exit(ans.peer_id)

    await ans(f"Ты считаешь, что {ans.text}. Мы тебя поняли. Это все?")
```
#### На примере веток
```python
from vkbottle.branch import ClsBranch, rule_disposal
from vkbottle.rule import VBMLRule

@bot.on.message(text="ставлю боту <mark:int>", lower=True)
async def wrapper(ans: Message, mark):
    await ans("Теперь расскажи, что ты думаешь о нем:")
    await bot.branch.add(ans.peer_id, "my_branch", mark=mark)

@bot.branch.cls_branch("my_branch")
class Branch(ClsBranch):
    @rule_disposal(VBMLRule(["это все", "да"], lower=True))
    async def exit_branch(self, ans: Message):
        await ans(f"Окей, твоя оценка «{self.context['mark']}» и рассказ о боте заcчитан!")
        await bot.branch.exit(ans.peer_id)
    
    async def branch(self, ans: Message, *args):
        await ans(f"Ты считаешь, что {ans.text}. Мы тебя поняли. Это все?")
```
### Альтернативный синтаксис входа и выхода
Существует альтернативный return-синтаксис для входа/выхода из бранчей. 
```python
async def wrapper(ans: Message):
    # Для ввода пользователя в бранч
    return Branch("branch-name")
    
async def branch(ans: Message):
    # Для вывода пользователя из бранча
    return ExitBranch()
```
## Другие способы хранения состояний
Существуют также другие виды хранения бранчей, один из них `vkbottle.framework.framework.branch.database_branch.DatabaseBranch`

Для того чтобы использовать его, требуется заполнить 4 метода абстрактного класса DatabaseBranch с помощью API вашего ORM. Пример вы можете найти [здесь](https://github.com/timoniq/vkbottle/blob/master/examples/database_branch.py)
