#import requests
#import time


#API_URL = 'https://api.telegram.org/bot'
#BOT_TOKEN = '8156474182:AAHvVyrbULj8MFrwfkq2XP6tgxl9p56IK78'

#offset = -2
#timeout = 30
#updates: dict


#def do_something() -> None:
#    print('Был апдейт')


#while True:
#    start_time = time.time()
#    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}&timeout={timeout}').json()

#    if updates['result']:
#        for result in updates['result']:
#            offset = result['update_id']
#            do_something()

    #time.sleep(3)
#    end_time = time.time()
#    print(f'Время между запросами к Telegram Bot API: {end_time - start_time}')


from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
#from aiogram.types import ContentType


# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
BOT_TOKEN = '8156474182:AAHvVyrbULj8MFrwfkq2XP6tgxl9p56IK78'

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message) -> None:
#    print(message)
    print(message.model_dump_json(indent=4, exclude_none=True))
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь - я тебе отвечу!')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message) -> None:
#    print(message)
    print(message.model_dump_json(indent=4, exclude_none=True))
    await message.answer(f'Можете отправить мне сообщения\nА я отправлю его Вам в ответ!:-)')

# Навешиваем декоратор с указанием в качестве фильтра типа контента
@dp.message(F.document)
async def process_send_animation(message: Message):
    # Выводим апдейт в терминал
    #print(message)
    # Отправляем сообщение в чат, откуда пришла анимация
    print(message.model_dump_json(indent=4, exclude_none=True))
    await message.answer(text='Вы прислали какой-то файл!')

# Этот хэндлер будет срабатывать на отправку боту фото
#async def send_photo_echo(message: Message) -> None:
#    print(message)
#    await message.answer_photo(message.photo[0].file_id)

# Этот хэндлер будет срабатывать на отправку боту видео
#async def send_video_echo(message: Message) -> None:
#    print(message)
#    await message.answer_video(message.video.file_id)

# Этот хэндлер будет срабатывать на отправку боту аннотации к видео
#async def send_video_note_echo(message: Message) -> None:
#    print(message)
#    await message.answer_video_note(message.video_note.file_id)

# Этот хэндлер будет срабатывать на отправку боту стикера
#async def send_sticker_echo(message: Message) -> None:
#    print(message)
#    await message.answer_sticker(message.sticker.file_id)

# Этот хэндлер будет срабатывать на отправку боту аудио
#async def send_audio_echo(message: Message) -> None:
#    print(message)
#    await message.answer_audio(message.audio.file_id)

# Этот хэндлер будет срабатывать на отправку боту звукозаписи
#async def send_voice_echo(message: Message) -> None:
#    print(message)
#    await message.answer_voice(message.voice.file_id)

# Этот хэндлер будет срабатывать на отправку боту анимации
#async def echo_animation_echo(message: Message) -> None:
#    print(message)
#    await message.answer_animation(message.animation.file_id)

# Этот хэндлер будет срабатывать на отправку боту файла
#async def send_file_echo(message: Message) -> None:
#    print(message)
#    await message.answer_document(message.document.file_id)

# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
#@dp.message()
#async def send_echo(message: Message) -> None:
#    print(message)
#    await message.answer(text=message.text)


# Этот хэндлер будет срабатывать на любые ваши сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    try:
        print(message.model_dump_json(indent=4, exclude_none=True))
        await message.send_copy(chat_id=message.chat.id, reply_to_message_id=message.message_id)
    except TypeError:
        await message.reply(
            text='Данный тип апдейтов не поддерживается '
                 'методом send_copy'
        )
        print(message.model_dump_json(indent=4, exclude_none=True))


# Навешиваем декоратор без фильтров, чтобы ловить большинство типов апдейтов
#@dp.message()
#async def process_any_update(message: Message):
    # Выводим апдейт в терминал
#    print(message)
    # Отправляем сообщение в чат, откуда пришел апдейт
#    await message.answer(text='Вы что-то прислали')


# Регистрируем хэндлеры
#dp.message.register(process_start_command, Command(commands='start'))
#dp.message.register(process_help_command, Command(commands='help'))
#dp.message.register(send_photo_echo, F.photo)
#dp.message.register(send_sticker_echo, F.sticker)
#dp.message.register(send_video_echo, F.video)
#dp.message.register(send_video_note_echo, F.video_note)
#dp.message.register(send_audio_echo, F.audio)
#dp.message.register(send_voice_echo, F.voice)
#dp.message.register(echo_animation_echo, F.animation)
#dp.message.register(send_file_echo, F.document)
#dp.message.register(send_echo)

if __name__ == '__main__':
    dp.run_polling(bot)