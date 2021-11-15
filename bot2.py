import config
import logging

from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter

#Задаём уровень логов
logging.basicConfig(level=logging.INFO)

#Инициальзируем бота
bot = Bot(token=config.TOKEN2)
dp = Dispatcher(bot)

#Инициализируем соединение с БД
db = SQLighter('bot2.db')

#Команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if(not db.subscriber_exists(message.from_user.id)):

        db.add_subscriber(message.from_user.id)
    else:
        db.update_subcsription(message.from_user.id, True)

    await message.answer("Вы успешно подписались на рассылку!\nЖдите скоро выйдут новые и интересные посты.")

#Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if(not db.subscriber_exists(message.from_user.id)):

        db.add_subscriber(message.from_user.id, False)
        await message.answer("Вы и так не подписаны")
    else:
        db.update_subcsription(message.from_user.id, False)
        await message.answer("Вы успешно отписались от рассылки!")

#Запускаем лонг поллинг
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
