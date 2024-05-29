from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from aiogram.types.web_app_info import WebAppInfo
from dotenv import load_dotenv
from datetime import datetime
import datetime as DT
import aiohttp
import asyncio
import json
import os
from pathlib import Path
import logging
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from typing import List, Union


load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
STAT_FILE = 'stat.txt'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)



class OrderStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_photo = State()


#Album class and func for send group

class AlbumMiddleware(BaseMiddleware):  
    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.01):
        self.latency = latency
        super().__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        if not message.media_group_id:
            return
        try:
            self.album_data[message.media_group_id].append(message)
            raise CancelHandler()  # Tell aiogram to cancel handler for this group element
        except KeyError:
            self.album_data[message.media_group_id] = [message]
            await asyncio.sleep(self.latency)
            message.conf["is_last"] = True
        data["album"] = self.album_data[message.media_group_id]

    async def on_post_process_message(self, message: types.Message, result: dict, data: dict):
        #Clean up after handling our album
        if message.media_group_id and message.conf.get("is_last"):
            del self.album_data[message.media_group_id] 







@dp.message_handler(state='*', commands=['start'])
async def start_welcome(message:types.Message, state: FSMContext):
    

    info_text = (
      
        "   Здравствуйте! Вас приветствует студия Альпака!🦙 Мы предлагаем услуги по реставрации кожаных изделий.👞\n\n"
        "   Через нашего чат-бота Вы сможете заказать доставку изделия в нашу мастерскую, узнать стоимость услуг и получить контактную информацию.\n\n"
        "   Для заказа доставки:\n"
        "   1. Нажмите на <b>Меню</b> в нижнем левом углу.\n"
        "   2. Выберите раздел <b>Заказать доставку</b>.\n"
        "   3. Укажите свои данные (ФИО, номер телефона).\n"
        "   4. Отправьте фотографии своего изделия с проблемной зоной.\n"
        "   5. После с Вами свяжется наш администратор.\n"
        
    )
  
    photo = 'alp.png'

    with open(photo, 'rb') as photo:
        await bot.send_photo(chat_id=message.chat.id, photo=photo)


    await message.answer(info_text, parse_mode='HTML')



    with open(STAT_FILE, 'r') as file:
        proof = file.readline()

# Checking condition for empty state

        if proof:

            count = int(proof)

        else:

            count = 0
    
    count += 1

    with open(STAT_FILE, 'w') as file:
        file.write(str(count)) 





@dp.message_handler(state='*', commands=['price'])
async def send_price(message: types.Message, state: FSMContext):

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Обувь", callback_data="obuv_definition"))
    keyboard.add(types.InlineKeyboardButton(text="Сумка", callback_data="sumka_definition"))
    keyboard.add(types.InlineKeyboardButton(text="Куртка", callback_data="kurtka_definition"))
    keyboard.add(types.InlineKeyboardButton(text="Услуги сапожника", callback_data="sapog_definition"))
    await state.finish()
    await message.answer(text="Выберите что Вас интересует:", reply_markup=keyboard)



#Button handler

@dp.callback_query_handler(text="obuv_definition", state='*')
async def obuv_definition(call: types.CallbackQuery, state: FSMContext):

    services = [
        " • Кроссовки тканевые (хим.чистка):   \n<b>3900₽</b> \n",
        " • Слипоны\эспадрильи тканевые (хим.чистка):   \n<b>3900₽</b> \n",
        " • Кроссовки (кожа\замш) Полн. покраска:   \n<b>4900₽</b> \n",
        " • Кроссовки (кожа\замш) Локал. покраска:   \n<b>2400₽</b> \n",
        " • Кроссовки БЕЛЫЕ Полн. покраска:   \n<b>6400₽</b> \n",
        " • Мокасины\лоферы (кожа\замш) Полн. покраска:   \n<b>4900₽</b> \n",
        " • Туфли (кожа\замш) Полн. покраска:   \n<b>4900₽</b> \n",
        " • Балетки (кожа\замш) Полн. покраска:   \n<b>4900₽</b> \n",
        " • Босоножки (кожа\замш) Полн. покраска:   \n<b>4900₽</b> \n",
        " • Слипоны (кожа\замш) Полн. покраска:   \n<b>4900₽</b> \n",
        " • Слипоны БЕЛЫЕ (кожа) Полн. покраска:   \n<b>6400₽</b> \n",
        " • Ботинки\ботильоны (кожа\замш) Полн. покраска:   \n<b>6400₽</b> \n",
        " • Сапоги\полусапоги (кожа\замш) Полн. покраска:   \n<b>7300₽</b>",
        "   • Частич. покраска: <b>4900₽</b> \n",
        " • Обувь экзотич.кожа (питон) Полн. покраска:   \n<b>9500₽</b>",
        "   • Локал. покраска: <b>4400₽</b> \n",
        " • Обувь экзотич.кожа (крокодил\рептилия) Полн. покраска:   \n<b>6900₽</b>",
        "   • Локал. покраска: <b>4400₽</b> \n",
        " • Лаковая кожа Полн. покраска\реставрация:   \n<b>6400₽</b>",
        "   • Локал. покраска: <b>2600₽</b> \n",
        " • Полная перекраска в другой цвет:  \n<b>5500₽</b>",
        "   • Локал. покраска: <b>2600₽</b> \n"
    ]
    services_text = "\n".join(services)

# Button back

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="back_to_menu"))
    

    await bot.answer_callback_query(call.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Список услуг реставрации Обувь:\n\n{services_text}", parse_mode=types.ParseMode.HTML, reply_markup=keyboard)


#Button handler

@dp.callback_query_handler(text="back_to_menu", state='*')
async def back_to_menu(call: types.CallbackQuery, state: FSMContext):
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Обувь", callback_data="obuv_definition"))
    keyboard.add(types.InlineKeyboardButton(text="Сумка", callback_data="sumka_definition"))
    keyboard.add(types.InlineKeyboardButton(text="Куртка", callback_data="kurtka_definition"))
    keyboard.add(types.InlineKeyboardButton(text="Услуги сапожника", callback_data="sapog_definition"))

    await bot.answer_callback_query(call.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите что Вас интересует:", reply_markup=keyboard)
     


# Button handler
@dp.callback_query_handler(text="sumka_definition", state='*')
async def sumka_definition(call: types.CallbackQuery, state: FSMContext):

    services = [
        "Большая сумка:\n"
        " • Полн. покраска покраска (гладкая кожа):   \n<b>14500₽</b>",
        "   • Частич. покраска (гладкая кожа):   \n<b>7500₽</b>",
        "   • Проф.уход (гладкая кожа):   <b>8500₽</b> \n",

        " • Полн. покраска покраска (экзотич. кожа):   \n<b>18000₽</b>",
        "   • Частич. покраска (экзотич. кожа):   \n<b>9000₽</b> ",
        "   • Проф.уход (экзотич. кожа):   \n<b>9000₽</b> \n",

        "Маленькая сумка:\n"
        " • Полн. покраска покраска (гладкая кожа):   \n<b>9500₽</b>",
        "   • Частич. покраска (гладкая кожа):   \n<b>4500₽</b>",
        "   • Проф.уход (гладкая кожа):   \n<b>6000₽</b> \n",

        " • Полн. покраска покраска (экзотич. кожа):  \n <b>12500₽</b>",
        "   • Частич. покраска (экзотич. кожа):   \n<b>6000₽</b>",
        "   • Проф.уход (экзотич. кожа):   \n<b>6500₽</b> \n",

        " • Полн. покраска перекраска в другой цвет:  \n <b>+2000₽</b>",
        "   • Локал. покраска (1 зона): <b>2400₽</b> \n",

    ]
    services_text = "\n".join(services)

# Button back

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="back_to_menu"))
    
    await bot.answer_callback_query(call.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Список услуг реставрации Сумка:\n\n{services_text}", parse_mode=types.ParseMode.HTML, reply_markup=keyboard)





@dp.callback_query_handler(text="kurtka_definition", state='*')
async def kurtka_definition(call: types.CallbackQuery, state: FSMContext):

    services = [
        " • Полн. покраска (гладкая кожа):  \n <b>13700₽</b>",
        "   • Частич. покраска (гладкая кожа):  \n <b>6500₽</b>",
        "   • Проф.уход (гладкая кожа):   \n <b>7000₽</b> \n",
        
        " • Полн. покраска (экзотич. кожа):  \n <b>17000₽</b> ",
        "   • Частич. покраска (экзотич. кожа):   \n <b>8500₽</b>",
        "   • Проф.уход (экзотич. кожа):  \n <b>9500₽</b>\n",

        " • Полн. покраска (замша):  \n <b>14600₽</b> ",
        "   • Частич. покраска (замша): \n <b>7500₽</b>",
        "   • Проф.уход (замша):  \n <b>8500₽</b>",
        "   • Локал. покраска (1 зона): \n <b>2400₽</b> \n",

        " • Полн. перекраска в другой цвет (гладкая):  \n <b>15500₽</b> \n",
        " • Полн. перекраска в другой цвет (экзотич): \n <b>19000₽</b> \n",
        " • Полн. перекраска в другой цвет (замша):  \n <b>16000₽</b> \n",

        " • Плащ Полн. покраска (гладкая кожа):    \n <b>15000₽</b> ",
        "   • Плащ Частич. покраска (гладкая кожа):   \n <b>7500₽</b>",
        "   • Проф.уход (гладкая кожа):  \n <b>8500₽</b> \n",
        " • Ремень: <b>3000₽</b> \n",

        " • Дубленка: <b>16400₽</b> ",
        "   • Локал. покраска (1 зона): <b>2400₽</b> \n",

        " • Перчатки: <b>5600₽</b> ",
        "   • Локал. покраска (1 зона): <b>2400₽</b> \n",

        " • Головной убор (кожа\ замша\ текстиль): <b>3900₽</b>",
        "   • Локал. покраска (1 зона): \n <b>2400₽</b> \n\n",

        "  ДОПОЛНИТЕЛЬНЫЕ УСЛУГИ\n",
        " • Тестирование ткани:    \n <b>1000₽</b> \n",
        " • 1 сквозное отверстие:  \n <b>3000₽</b> \n",
        " • 2 сквозных отверстия:  \n <b>2000₽</b> \n",
        " • 3 сквозных отверстия:  \n <b>1000₽</b> \n",
        " • 4 и последующие сквозные отверстия: \n <b>1000₽</b> \n",


    ]
    services_text = "\n".join(services)

# Button back

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="back_to_menu"))
    
    await bot.answer_callback_query(call.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Список услуг реставрации Куртка:\n\n{services_text}", parse_mode=types.ParseMode.HTML, reply_markup=keyboard)





@dp.callback_query_handler(text="sapog_definition", state='*')
async def sapog_definition(call: types.CallbackQuery, state: FSMContext):

    services = [
        " • Профилактика (ЖЕН): <b>1500₽</b>\n",
        " • Профилактика (МУЖ): <b>2000₽</b>\n\n",

        " • Набойки (ЖЕН): <b>900₽</b>\n",
        " • Набойки (МУЖ): <b>1200₽</b>\n\n",

        " • Латка (ЖЕН): <b>800₽</b>\n",
        " • Латка (МУЖ): <b>1000₽</b>\n\n",

        " • Задники: <b>1600₽</b>\n",

        " • Перетяжка каблука: <b>2500₽</b>\n",

        " • Замена каблука: <b>2500₽</b>\n",

        " • Укрепление каблука: <b>1000₽</b>\n",

        " • Перешив элементов: <b>900₽</b>\n",

        " • Растяжка: <b>1000₽</b>\n",

        " • Круговой пошив: <b>2000₽</b>\n",

        " • Круговая подклейка подошвы: <b>1500₽</b>\n",

        " • Наращивание носика: <b>900₽</b>\n",

        " • Наращивание подошвы: <b>1000₽</b>\n",

        " • Замена сетки: <b>2500₽</b>\n",

        " • Замена молнии:\n",
        "   (мал) - <b>900₽</b>\n",
        "   (больш) - <b>1500₽</b>\n\n",

        " • Перешив\замена ручек: <b>500₽</b>\n",

        " • Перешив\замена резинки: <b>500₽</b>\n",

        " • Укоротить ремешок: <b>500₽</b>\n",






    ]
    services_text = "\n".join(services)


# Button back

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="back_to_menu"))
    
    await bot.answer_callback_query(call.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Список услуг реставрации Сапожника:\n\n{services_text}", parse_mode=types.ParseMode.HTML, reply_markup=keyboard)






@dp.message_handler(state='*', commands=['info'])
async def info_send(message: types.Message, state: FSMContext):


    info_text = (

        "Контактная ифнормация:\n\n"
        "🌎 Адрес: г.Владикавказ, ул. Московская 51/1\n\n"
        "🌎 Адрес: г.Владикавказ, ул. Маркова 1А\n\n"
        "⏳ График работы: с 9:00 до 19:00,\n с понедельника по воскресенье, без выходных\n\n"
        "📲 Контактный телефон: +7(918)-822-94-44\n\n"
        "🗺️ Google карты: [Мы здесь!](https://maps.app.goo.gl/N1FAjH3QFxPBaK9P9)\n\n"
        "🗺️ Яндекс карты: [Мы здесь!](https://yandex.ru/maps/-/CDb~z-Yj)\n\n"
        "🌐 WhatsApp: [WhatsApp Alpaca](wa.me/79188229444)\n\n"
        "🌐 Instagram\*: [Instagram Alpaca](https://www.instagram.com/alpaca_masterskaya?igsh=NTc4MTIwNjQ2YQ==)\n"
        "   \*: «деятельность организации запрещена на территории РФ»"
        
        
    )

    await message.answer(info_text, parse_mode='Markdown', disable_web_page_preview=True)
    # await message.answer(text='*: «деятельность организации запрещена на территории РФ»')

    
    
  

@dp.message_handler(state='*', commands=['delivery'])
async def delivery_send(message: types.Message):
    await OrderStates.waiting_for_name.set()
    await message.answer(text="Здравствуйте, введите свои контактные данные, чтобы мы могли связаться с Вами.")
    await message.answer("Введите Ваше ФИО:")
    


@dp.message_handler(state=OrderStates.waiting_for_name)
async def process_service(message: types.Message, state: FSMContext):

    await state.update_data(name=message.text)
    await message.answer("Введите Ваш контактный номер телефона:")
    await OrderStates.next()



@dp.message_handler(state=OrderStates.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):

    await state.update_data(phone=message.text)
    await message.answer("Пришлите фотографии Вашего изделия. Вы можете выбрать одну или несколько фотографий с проблемной зоной:")
    await OrderStates.next()




#Handler - class AlbumMiddleware for input photo group

@dp.message_handler(is_media_group=True, content_types=types.ContentType.ANY, state=OrderStates.waiting_for_photo)
async def handle_albums(message: types.Message, album: List[types.Message], state:FSMContext):

    
    data = await state.get_data()
    name = data.get("name")
    phone = data.get("phone")

    contact_info = f"ФИО клиента: {name}\nКонтактный номер: {phone}"
    await bot.send_message(chat_id=CHANNEL_ID, text=contact_info)


    media_group = types.MediaGroup()
    for obj in album:
        if obj.photo:
            file_id = obj.photo[-1].file_id
        else:
            file_id = obj[obj.content_type].file_id
        try:
            # We can also add a caption to each file by specifying `"caption": "text"`
            media_group.attach({"media": file_id, "type": obj.content_type})
        except ValueError:
            return await message.answer("This type of album is not supported by aiogram.")
    # Send the media group to the specified group
    await bot.send_media_group(chat_id=CHANNEL_ID, media=media_group)
    await message.reply("Спасибо! Ваша информация была передана, скоро с Вами свяжется наш администратор.")
    await state.finish()



#Handler for send single photo (single photo is not album function)
@dp.message_handler(content_types=[types.ContentType.PHOTO], state=OrderStates.waiting_for_photo)
async def handle_single_photo(message: types.Message, state:FSMContext):

    data = await state.get_data()
    name = data.get("name")
    phone = data.get("phone")

    contact_info = f"Имя: {name}\nКонтактный номер: {phone}"
    await bot.send_message(chat_id=CHANNEL_ID, text=contact_info)

    await bot.send_photo(chat_id=CHANNEL_ID, photo=message.photo[-1].file_id)
    await message.reply("Спасибо! Ваша информация была передана, скоро с Вами свяжется наш сотрудник.")
    await state.finish()




#Statistics command, hiden in chat-bot

@dp.message_handler(state='*', commands=['stat'])
async def send_stat(message: types.Message):

    with open(STAT_FILE, 'r') as file:
        count = file.read().strip()

    await message.answer(f"Бот Альпака использовали {count} раз(а).")





if __name__ == '__main__':

    dp.middleware.setup(AlbumMiddleware())
    executor.start_polling(dp, skip_updates=True)