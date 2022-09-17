import logging
from xlparcer import Day
from xlparcer import Lesson
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


API_TOKEN = '5445757942:AAH9664XnQoatqP30427arxwaLFxb1_aBx8'    # delete this hardcode sometime pls

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    name = State()


def get_info(msg):
    i = 0
    k = 0
    sheet_num = 0
    row = 0
    column = 0
    for c in msg:

        if c.isdigit() and k == 0:
            sheet_num = sheet_num * 10 + int(c)
            continue
        elif c == ' ':
            k = k + 1
            continue

        if c.isdigit() and k == 1:
            row = row * 10 + int(c)
            continue
        elif c == ' ':
            k = k + 1
            continue

        if c.isdigit() and k == 2:
            column = column * 10 + int(c)
            continue

    info = [sheet_num, row, column]
    print(info)
    return info


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("you can get schedule for today by command \"/today\"")


@dp.message_handler(state='*', commands=['cancel'])
async def cancel_handler(message: types.Message, state: FSMContext):

    current_state = await state.get_state()
    if current_state is None:
        # User is not in any state, ignoring
        return

    # Cancel state and inform user about it
    await state.finish()
    await message.reply('Cancelled.')


@dp.message_handler(commands='today')
async def today(message: types.Message):
    await Form.name.set()
    await message.reply("send sheet number, row, column of first period of the day, example for B-M-22: 1 6 3")


@dp.message_handler(state=Form.name)
async def send_today(message: types.Message, state: FSMContext):
    s = message.text
    coords = get_info(s)
    print(coords)
    cur_day = Day(coords[0], coords[1], coords[2])
    strings = cur_day.print_day()      # list of strings containing time and lesson name "8.00 -- 9.35 Иностранный язык"
    answer = ''
    for i in strings:
        answer = answer + i + '\n'
    await state.finish()
    await message.reply(answer)
    print('sent today')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)