import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from typing import Dict, Union

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN = '8156474182:AAHvVyrbULj8MFrwfkq2XP6tgxl9p56IK78'

# Создаем объекты бота и диспетчера
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# Количество попыток, доступных пользователю в игре
ATTEMPTS = 5
users = {}

def get_user(message: Message) -> Dict[str, Union[bool, int]]:
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'in_game': False,
            'secret_number': 0,
            'attempts': 0,
            'total_games': 0,
            'wins': 0
        }
    return users[message.from_user.id]

# Словарь, в котором будут храниться данные пользователя
#user = {'in_game': False,
#        'secret_number': None,
#        'attempts': None,
#        'total_games': 0,
#        'wins': 0}


# Функция возвращающая случайное целое число от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)

# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(CommandStart())
#@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message) -> None:
    get_user(message)
    print(message.model_dump_json(indent=4, exclude_none=True))
    await message.answer(f'Привет!\nДавай сыграем в игру "Угадай число"?\nЧтобы получить правила игры и список доступных команд - отправь команду /help')
    # Если пользователь только запустил бота и его нет в словаре '
    # 'users - добавляем его в словарь
#    if message.from_user.id not in users:
#        users[message.from_user.id] = {
#            'in_game': False,
#            'secret_number': None,
#            'attempts': None,
#            'total_games': 0,
#            'wins': 0
#        }
#    return users[message.from_user.id]

# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands='help'))
async def process_help_command(message: Message) -> None:
    get_user(message)
    print(message.model_dump_json(indent=4, exclude_none=True))
    await message.answer(
        'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
        'попыток\n\nДоступные команды:\n/help - правила '
        'игры и список команд\n/cancel - выйти из игры\n'
        '/stat - посмотреть статистику\n\nДавай сыграем?'
    )

# Этот хэндлер будет срабатывать на команду "/stat"
@dp.message(Command(commands='stat'))
async def process_stat_command(message: Message) -> None:
    get_user(message)
    print(message.model_dump_json(indent=4, exclude_none=True))
    await message.answer(
        f'Всего игр сыграно: {users[message.from_user.id]["total_games"]}\n'
        f'Игр выиграно: {users[message.from_user.id]["wins"]}'
    )

# Этот хэндлер будет срабатывать на команду "/cancel"
@dp.message(Command(commands='cancel'))
async def process_cancel_command(message: Message) -> None:
    get_user(message)
    if users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = False
        print(message.model_dump_json(indent=4, exclude_none=True))
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть '
            'снова - напишите об этом'
        )
    else:
        print(message.model_dump_json(indent=4, exclude_none=True))
        await message.answer(
            'А мы и так с вами не играем. '
            'Может, сыграем разок?'
        )


# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра',
                                'играть', 'хочу играть', 'ага']))
async def process_positive_answer(message: Message) -> None:
    get_user(message)
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        users[message.from_user.id]['attempts'] = ATTEMPTS
        print(message.model_dump_json(indent=4, exclude_none=True))
        await message.answer(
            'Ура!\n\nЯ загадал число от 1 до 100, '
            'попробуй угадать!'
        )
    else:
        print(message.model_dump_json(indent=4, exclude_none=True))
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat'
        )


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message) -> None:
    get_user(message)
    if not users[message.from_user.id]['in_game']:
        print(message.model_dump_json(indent=4, exclude_none=True))
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом'
        )
    else:
        print(message.model_dump_json(indent=4, exclude_none=True))
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, числа от 1 до 100'
        )


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message) -> None:
    get_user(message)
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            print(message.model_dump_json(indent=4, exclude_none=True))
            await message.answer(
                'Ура!!! Вы угадали число!\n\n'
                'Может, сыграем еще?'
            )
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            print(message.model_dump_json(indent=4, exclude_none=True))
            await message.answer('Мое число меньше')
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            print(message.model_dump_json(indent=4, exclude_none=True))
            await message.answer('Мое число больше')

        if users[message.from_user.id]['attempts'] == 0:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            print(message.model_dump_json(indent=4, exclude_none=True))
            await message.answer(
                'К сожалению, у вас больше не осталось '
                'попыток. Вы проиграли :(\n\nМое число '
                f'было {users[message.from_user.id]["secret_number"]}\n\nДавайте '
                'сыграем еще?'
            )
    else:
        print(message.model_dump_json(indent=4, exclude_none=True))
        await message.answer('Мы еще не играем. Хотите сыграть?')


# Этот хэндлер будет срабатывать на остальные любые сообщения
@dp.message()
async def process_other_answers(message: Message) -> None:
    get_user(message)
    if users[message.from_user.id]['in_game']:
        print(message.model_dump_json(indent=4, exclude_none=True))
        await message.answer(
            'Мы же сейчас с вами играем. '
            'Присылайте, пожалуйста, числа от 1 до 100'
        )
    else:
        print(message.model_dump_json(indent=4, exclude_none=True))
        await message.answer(
            'Я довольно ограниченный бот, давайте '
            'просто сыграем в игру?'
        )


if __name__ == '__main__':
    dp.run_polling(bot)