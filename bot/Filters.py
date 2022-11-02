import config

bot = config.BOT


async def user_filter(message):
    if message.chat.type != "private":
        return False
    user = await bot.get_chat_member(config.CHOOSEN_CHAT, message.from_user.id)
    if (user["status"] != "left") or (message.from_user.id in config.ADMINS):
        return True
    return False


async def admin_filter(message):
    if message.chat.type != "private":
        return False
    if message.from_user.id in config.ADMINS:
        return True
    return False
