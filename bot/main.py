import logging
import time
import traceback

from aiogram import Dispatcher, executor, types

import config
from states import States
import Filters
import DB



# Configure logging
logging.basicConfig(level=logging.INFO)

bot = config.BOT
dp = Dispatcher(bot)


@dp.errors_handler()
async def error_handler(update, error):
    with open(errorLog := "Logs/errorLog" + str(time.time()) + ".txt", 'w') as f:
        err=traceback.format_exc()
        f.write("Update: "+str(update))
        f.write("\n\n")
        f.write("Error: "+err)
        logging.warning(err)
        for admin in config.ADMINS:
            await bot.send_message(admin, "ADMIN NOTIFICATION: Some error occured during the work of the bot.\n\n"
                                          "Look "+errorLog)
        return True



@dp.callback_query_handler()
async def callback(call: types.CallbackQuery):
    request=call.data.split()
    match request[0]:
        case "FIRSTACCOUNT":
            await States.first_account(call.message)
        case "CHECKER":
            await States.checker(call.message)
        case "CHECK":
            await States.first_map(call.message)
        case "MAP_FINISHED":
            if(await DB.map_finished(call.message.chat.id)):
                await States.another_map(call.message)
            else:
                await States.another_acc(call.message)



@dp.message_handler(Filters.user_filter, commands=['start'])
async def start(message: types.Message):
    await States.start(message)

@dp.message_handler(Filters.admin_filter, commands=['add'])
async def add(message: types.Message):
    await DB.add(message.text)
    await message.answer("Аккаунт добавлен.")

#@dp.message_handler(Filters.admin_filter, commands=['take'])
#async def take(message: types.Message):
#    print(await DB.take())

@dp.message_handler(Filters.admin_filter, commands=['show'])
async def show(message: types.Message):
    await DB.show()
    await DB.TEST(message.chat.id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=DB.startup)
