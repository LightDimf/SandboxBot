from aiogram import types
import DB

class States:
    @staticmethod
    async def start(message):
        keyboard = types.inline_keyboard.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Далее", callback_data="FIRSTACCOUNT"))
        await message.answer("Начальное сообщение.", reply_markup=keyboard)

    @staticmethod
    async def first_account(message):
        keyboard = types.inline_keyboard.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Проверил", callback_data="CHECKER"))
        log, pas = await DB.take()
        await message.edit_text(f"Твой первый аккаунт:\nlog: {log}\nПароль: {pas}\n\nПроверь всё ли правильно.", reply_markup=keyboard)
        await DB.bound(log, message.chat.id)

    @staticmethod
    async def checker(message):
        keyboard = types.inline_keyboard.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Нажал?", callback_data="CHECK"))
        await message.edit_text(f"Давай проверим по этой ссылке: НЕ РЕАЛИЗОВАНО", reply_markup=keyboard)

    @staticmethod
    async def first_map(message):
        keyboard = types.inline_keyboard.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Закончил", callback_data="MAP_FINISHED"))
        map = await DB.currentMap(message.chat.id)
        await message.edit_text(f"Первая карта: {map}", reply_markup=keyboard)

    @staticmethod
    async def another_map(message):
        keyboard = types.inline_keyboard.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Закончил", callback_data="MAP_FINISHED"))
        map = await DB.currentMap(message.chat.id)
        await message.edit_text(f"Твоя следующая карта: {map}", reply_markup=keyboard)

    @staticmethod
    async def another_acc(message):
        keyboard = types.inline_keyboard.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Ок", callback_data="CHECKER"))
        log, pas = await DB.take()
        await message.edit_text(f"Ты набрал нужный уровень! Твой следующий аккаунт:\nlog: {log}\nПароль: {pas}", reply_markup=keyboard)
        await DB.bound(log, message.chat.id)