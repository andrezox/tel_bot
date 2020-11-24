import logging
import re
from random import randint
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import settings
import texts
from requests import get
import json
from sqliter import SQLighter
import datetime
import asyncio
# Инициал. бота
bot = Bot(token=settings.token)

now_time_first = datetime.datetime.now().day

dp = Dispatcher(bot,storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

# Инициал. бд
db = SQLighter('db.db')


# Логирование, нужное только во время отладки.
#logging.basicConfig(level=logging.INFO)


class Pr_set:
    text = "Текст не установлен!"
    photo = False
    faq_text = "Текст не установлен!"

""" STATES """
class btc_pay_balance(StatesGroup):


    money = State()
    check = State()

class crystal_pay(StatesGroup):


    money = State()

class pr_make(StatesGroup):


    get_text = State()

class ref_proc(StatesGroup):



    get = State()
class make_faq_text(StatesGroup):


    text = State()

class add_piar_1(StatesGroup):

    name = State()
    text = State()
class add_piar_2(StatesGroup):

    name = State()
    text = State()


class add_categ(StatesGroup):
    name = State()
class del_categ(StatesGroup):
    name = State()



class add_podcateg(StatesGroup):
    categ = State()
    name = State()
class del_podcateg(StatesGroup):
    categ = State()
    name = State()

class add_tovar(StatesGroup):
    categ = State()
    podcateg = State()
    name = State()
    price = State()
    desc = State()
    
class del_tovar(StatesGroup):
    categ = State()
    podcateg = State()
    name = State()

class plus_tovar(StatesGroup):
    categ = State()
    podcateg = State()
    tt = State()
    name = State()



@dp.message_handler(commands="start")
async def advert_1(message: types.Message):
    if int(message.chat.id) >= 0:
        ref_id = message.text[7:].replace(" ","")
        if ref_id == "":
            ref_id = "0"
        db.reg_user(message.from_user.id,ref_id)
        state = dp.current_state(chat = message.chat.id, user = message.from_user.id)
        await state.finish()
        buttons = ReplyKeyboardMarkup(resize_keyboard=True)
        buy_menu = (texts.buy_button)
        pay_bal = (texts.balance_pay_button)
        buttons.add(buy_menu,pay_bal)
        balance = db.get_ebal(message.chat.id)
        reply = texts.menu_text
            
        b1 = db.get_buttons("1")
        b2 = db.get_buttons("2")

        if b1 != "0":
            buttons.add(b1)
        if b2 != "0":
            buttons.add(b2)
        await message.answer(reply.format(balance[0]), reply_markup = buttons)

@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    if str(message.from_user.id) == settings.admin or message.from_user.id in settings.head_admin:
        await message.photo[-1].download('pr.jpg')
        await message.answer("Фотография для рассылки загружена!")

@dp.message_handler(state="*")
async def echo_message(message: types.Message):
    date = db.get_bot()
    text = message.text
    podcateg_active = False
    tovar_active = False
    tovar_chosen = False
    if db.get_podcat_by_parent(text,False):
        podcateg_active = True
    if db.get_prod_by_parent(text,False):
        tovar_active = True
    if db.get_prod_advanced(text,False):
        tovar_chosen = True
    if int(date[0]) != 0:
        if True:
            #-------------------------------ГЛАВНОЕ_МЕНЮ-----------------------------#
            state = dp.current_state(chat = message.chat.id, user = message.from_user.id)
            aastate = await state.get_state()
            if text == texts.back_button:
                state = dp.current_state(chat = message.chat.id, user = message.from_user.id)
                await state.finish()
                buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                buy_menu = (texts.buy_button)
                pay_bal = (texts.balance_pay_button)
                buttons.add(buy_menu,pay_bal)
                balance = db.get_ebal(message.chat.id)

                reply = texts.menu_text
            
                b1 = db.get_buttons("1")
                b2 = db.get_buttons("2")

                if b1 != "0":
                    buttons.add(b1)
                if b2 != "0":
                    buttons.add(b2)
                if str(message.from_user.id) == settings.admin or message.from_user.id in settings.head_admin:
                    admin_menu = ("🔥 Админка 🔥")
                    buttons.add(admin_menu)
                await message.answer(reply.format(balance[0]), reply_markup = buttons)
            #-------------------------------TOVARS_MENU------------------------------#
            elif text == "💰 Управление продажами 💰":
                state = dp.current_state(chat = message.chat.id, user = message.from_user.id)
                await state.finish()
                if str(message.from_user.id) == settings.admin or message.from_user.id in settings.head_admin:
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    categ_button = ("🎁 Категории 🎁")
                    podcateg_button = ("💣 Подкатегории 💣")
                    sell_button = ("💰 Товары 💰")
                    admin = ("🔥 Админка 🔥")
                    buttons.add(categ_button).add(podcateg_button).add(sell_button).add(admin)
                    await message.answer("Menu", reply_markup = buttons)
            #--------------------------------TVARI------------------------------------# 
            elif text == "💰 Товары 💰":
                state = dp.current_state(chat = message.chat.id, user = message.from_user.id)
                await state.finish()
                if str(message.from_user.id) == settings.admin or message.from_user.id in settings.head_admin:
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    categ_button = ("✅ Добавить товар ✅")
                    podcateg_button = ("❌ Удалить товар ❌")
                    podcateg_button1 = ("💣 Пополнить товар 💣")
                    admin = ("💰 Управление продажами 💰")
                    buttons.add(categ_button).add(podcateg_button).add(podcateg_button1).add(admin)
                    await message.answer("Menu", reply_markup = buttons)
            elif text == "💣 Пополнить товар 💣":
                categs = db.get_cat()
                tovarsss = "💰 Товары 💰"
                buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                await plus_tovar.categ.set()
                buttons.add(tovarsss)
                for cat in categs:
                    buttons.add(cat[0])
                await message.answer("🎁 Категории 🎁", reply_markup = buttons)
            elif text == "✅ Добавить товар ✅":
                categs = db.get_cat()
                tovarsss = "💰 Товары 💰"
                buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                await add_tovar.categ.set()
                buttons.add(tovarsss)
                for cat in categs:
                    buttons.add(cat[0])
                await message.answer("🎁 Категории 🎁", reply_markup = buttons)
            elif text == "❌ Удалить товар ❌":
                categs = db.get_cat()
                tovarsss = "💰 Товары 💰"
                buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                await del_tovar.categ.set()
                buttons.add(tovarsss)
                for cat in categs:
                    buttons.add(cat[0])
                await message.answer("🎁 Категории 🎁", reply_markup = buttons)
            #-------------------------------CATEG_MENU--------------------------------#
            elif text == "🎁 Категории 🎁":
                state = dp.current_state(chat = message.chat.id, user = message.from_user.id)
                await state.finish()
                if str(message.from_user.id) == settings.admin or message.from_user.id in settings.head_admin:
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    categ_button = ("✅ Добавить категорию ✅")
                    podcateg_button = ("❌ Удалить категорию ❌")
                    admin = ("💰 Управление продажами 💰")
                    buttons.add(categ_button).add(podcateg_button).add(admin)
                    await message.answer("Menu", reply_markup = buttons)
            elif text == "✅ Добавить категорию ✅":
                if str(message.from_user.id) == settings.admin or message.from_user.id in settings.head_admin:
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    categ_button = ("🎁 Категории 🎁")
                    buttons.add(categ_button)
                    await add_categ.name.set()
                    await message.answer("Отправьте мне название категории.", reply_markup = buttons)
            elif text == "❌ Удалить категорию ❌":
                if str(message.from_user.id) == settings.admin or message.from_user.id in settings.head_admin:
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    categ_button = ("🎁 Категории 🎁")
                    buttons.add(categ_button)
                    categs = db.get_cat()
                    for cat in categs:
                        buttons.add(cat[0])
                    back_menu = (texts.back_button)
                    await del_categ.name.set()
                    await message.answer("Отправьте мне название категории.", reply_markup = buttons)
            #-------------------------------PODCATEG_MENU----------------------------#
            elif text == "💣 Подкатегории 💣":
                state = dp.current_state(chat = message.chat.id, user = message.from_user.id)
                await state.finish()
                if str(message.from_user.id) == settings.admin or message.from_user.id in settings.head_admin:
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    categ_button = ("✅ Добавить подкатегорию ✅")
                    podcateg_button = ("❌ Удалить подкатегорию ❌")
                    admin = ("💰 Управление продажами 💰")
                    buttons.add(categ_button).add(podcateg_button).add(admin)
                    await message.answer("Menu", reply_markup = buttons)
            elif text == "✅ Добавить подкатегорию ✅":
                if str(message.from_user.id) == settings.admin or message.from_user.id in settings.head_admin:
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    categ_button = ("💣 Подкатегории 💣")
                    buttons.add(categ_button)
                    await add_podcateg.categ.set()
                    categs = db.get_cat()
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    for cat in categs:
                        buttons.add(cat[0])
                    back_menu = (texts.back_button)
                    buttons.add(back_menu)
                    await message.answer("В какую категорию ?", reply_markup = buttons)
            elif text == "❌ Удалить подкатегорию ❌":
                if str(message.from_user.id) == settings.admin or message.from_user.id in settings.head_admin:
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    categ_button = ("💣 Подкатегории 💣")
                    buttons.add(categ_button)
                    await del_podcateg.categ.set()
                    categs = db.get_cat()
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    for cat in categs:
                        buttons.add(cat[0])
                    back_menu = (texts.back_button)
                    buttons.add(back_menu)
                    await message.answer("В какой категории??", reply_markup = buttons)

            #-------------------------------ADMIN_PANEL------------------------------#
            elif text == "🔥 Админка 🔥":
                state = dp.current_state(chat = message.chat.id, user = message.from_user.id)
                await state.finish()
                if str(message.from_user.id) == settings.admin or message.from_user.id in settings.head_admin:
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    #ref_edit = ("💵 Изменить % рефералки 💵")
                    #change_faq = ("ℹ️ Изменить FAQ ℹ️")
                    add_pr = ("📈 Редактирование рекламы 📈")
                    sell_settings = ("💰 Управление продажами 💰")
                    make_pr = ("💈 Сделать рассылку 💈")
                    back_menu = (texts.back_button)
                    buttons.add(add_pr).add(sell_settings).add(make_pr).add(back_menu)
                    info = db.get_bot()
                    
                    await message.answer(texts.admin_panel.format(users_amount = db.get_len_users(), make_money = info[2],day = info[0],live = info[1], sold = info[3], refproc = info[4]), reply_markup = buttons)#{make_money}#{sold}#{refproc}
            
            #-------------------------------Изменение доли рефералки-----------------#
            elif text == "💵 Изменить % рефералки 💵":
                
                if str(message.from_user.id) == settings.admin or message.from_user.id in settings.head_admin:
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    admin = ("🔥 Админка 🔥")
                    buttons.add(admin)
                    await ref_proc.get.set()
                    await message.answer("Отправьте мне долю реферера (целое число от 0 до 100 включительно.)", reply_markup = buttons)
            #-------------------------------Управление кнопками пиара--------------------------#
            elif text == "📈 Редактирование рекламы 📈":
                if str(message.from_user.id) == settings.admin or message.from_user.id in settings.head_admin:
                    b1 = db.get_buttons("1")
                    b2 = db.get_buttons("2")
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)

                    if b1 == "0":
                        buttons.add("🔴 Откл 1 🔴")
                        
                    else:
                        buttons.add("🟢 Вкл 1 🟢")
                    if b2 == "0":
                        buttons.add("🔴 Откл 2 🔴")
                        
                    else:
                        buttons.add("🟢 Вкл 2 🟢")

                    admin = ("🔥 Админка 🔥")
                    buttons.add(admin)
                    await message.answer("Управление кнопками рекламы.", reply_markup = buttons)


            elif text == "🔴 Откл 1 🔴" or text == "🔴 Откл 2 🔴":
                if str(message.from_user.id) == settings.admin or message.from_user.id in settings.head_admin:
                    if text == "🔴 Откл 1 🔴":
                        buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                        await add_piar_1.name.set()
                        admin = ("🔥 Админка 🔥")
                        buttons.add(admin)
                        await message.answer("Введите название кнопки.", reply_markup = buttons)
                    elif text == "🔴 Откл 2 🔴":
                        buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                        await add_piar_2.name.set()
                        admin = ("🔥 Админка 🔥")
                        buttons.add(admin)
                        await message.answer("Введите название кнопки.", reply_markup = buttons)
            elif text == "🟢 Вкл 1 🟢" or text == "🟢 Вкл 2 🟢":
                if str(message.from_user.id) == settings.admin or message.from_user.id in settings.head_admin:
                    if text == "🟢 Вкл 1 🟢":
                        db.change_button("0","0",1)
                        b1 = db.get_buttons("1")
                        b2 = db.get_buttons("2")
                        buttons = ReplyKeyboardMarkup(resize_keyboard=True)

                        if b1 == "0":
                            buttons.add("🔴 Откл 1 🔴")
                        
                        else:
                            buttons.add("🟢 Вкл 1 🟢")
                        if b2 == "0":
                            buttons.add("🔴 Откл 2 🔴")
                        
                        else:
                            buttons.add("🟢 Вкл 2 🟢")

                        admin = ("🔥 Админка 🔥")
                        buttons.add(admin)
                        await message.answer("Кнопка была отключена.", reply_markup = buttons)
                    elif text == "🟢 Вкл 2 🟢":
                        db.change_button("0","0",2)
                        b1 = db.get_buttons("1")
                        b2 = db.get_buttons("2")
                        buttons = ReplyKeyboardMarkup(resize_keyboard=True)

                        if b1 == "0":
                            buttons.add("🔴 Откл 1 🔴")
                        
                        else:
                            buttons.add("🟢 Вкл 1 🟢")
                        if b2 == "0":
                            buttons.add("🔴 Откл 2 🔴")
                        
                        else:
                            buttons.add("🟢 Вкл 2 🟢")

                        admin = ("🔥 Админка 🔥")
                        buttons.add(admin)
                        await message.answer("Кнопка была отключена.", reply_markup = buttons)
            #-------------------------------Работа с товаром--------------------------#        
                    
            #-------------------------------РАССЫЛКА_С_ФОТО--------------------------#
            elif text == "💈 Сделать рассылку 💈":
                if str(message.from_user.id) == settings.admin or message.from_user.id in settings.head_admin:
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    get_pr_text = ("✉️ Тест рассылки ✉️")
                    give_pr_text = ("📱 Изменить текст рассылки 📱")
                    start_pr = ("🚀 Запуск рассылки 🚀")

                    if Pr_set.photo:
                        add_photo = ("🟢 Фото 🟢")
                    else:
                        add_photo = ("🔴 Фото 🔴")
                    start_pr = ("🚀 Запуск рассылки 🚀")
                    admin = ("🔥 Админка 🔥")
                    buttons.add(get_pr_text).add(give_pr_text).add(add_photo).add(start_pr).add(admin)
                    await message.answer("Меню создания рассылки \n Отправьте мне фото, чтобы оно отображалось в рассылке. \n🔴 Фото 🔴 - фото в рассылке отключено .\n🟢 Фото 🟢 - фото в рассылке включено.", reply_markup = buttons)
            elif text == "🔴 Фото 🔴" or text == "🟢 Фото 🟢":
                    if str(message.from_user.id) == settings.admin or message.from_user.id in settings.head_admin:
                        if text == "🔴 Фото 🔴":
                            Pr_set.photo = True
                        else:
                            Pr_set.photo = False
                        buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                        get_pr_text = ("✉️ Тест рассылки ✉️")
                        give_pr_text = ("📱 Изменить текст рассылки 📱")
                        start_pr = ("🚀 Запуск рассылки 🚀")

                        if Pr_set.photo:
                            add_photo = ("🟢 Фото 🟢")
                        else:
                            add_photo = ("🔴 Фото 🔴")
                        start_pr = ("🚀 Запуск рассылки 🚀")
                        admin = ("🔥 Админка 🔥")
                        buttons.add(get_pr_text).add(give_pr_text).add(add_photo).add(start_pr).add(admin)
                        await message.answer("Меню создания рассылки \n Отправьте мне фото, чтобы оно отображалось в рассылке. \n🔴 Фото 🔴 - фото в рассылке отключено .\n🟢 Фото 🟢 - фото в рассылке включено.", reply_markup = buttons)
            elif text == "🚀 Запуск рассылки 🚀":
                if str(message.from_user.id) == settings.admin or message.from_user.id in settings.head_admin:
                    ids = db.get_users_id()
                    
                    for id in ids:
                        if Pr_set.photo:
                            try:
                                with open("pr.jpg","rb") as f:
                                    await bot.send_photo(id[0], f, caption=Pr_set.text)
                            except:
                                pass
                        else:
                            await bot.send_message(id[0],Pr_set.text)
            elif text == "✉️ Тест рассылки ✉️":
                if str(message.from_user.id) == settings.admin or message.from_user.id in settings.head_admin:
                    if Pr_set.photo:
                        with open("pr.jpg","rb") as f:

                            await bot.send_photo(message.from_user.id, f, caption=Pr_set.text)
                    else:
                        await bot.send_message(message.from_user.id,Pr_set.text)
            elif text == "📱 Изменить текст рассылки 📱":
                if str(message.from_user.id) == settings.admin or message.from_user.id in settings.head_admin:
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    admin = ("🔥 Админка 🔥")
                    buttons.add(admin)
                    await pr_make.get_text.set()
                    await message.answer("Отправьте мне текст для рассылки.", reply_markup = buttons)
            #---------------------------ПОПОЛНЕНИЕ_БАЛАНСА---------------------------#
            elif text == texts.balance_pay_button:
                buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                btc_pay = (texts.btc_pay_button)
                ticket_pay = (texts.eticket_pay_button)
                back_menu = (texts.back_button)
                buttons.add(btc_pay,ticket_pay).add(back_menu)

                await message.answer(texts.deposit_menu_text, reply_markup = buttons)
            #---------------------------ГЛАВНЫЕ_КАТЕГОРИИ----------------------------#
            elif aastate != "del_categ:name" and text == texts.buy_button:
                categs = db.get_cat()
                buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                for cat in categs:
                    buttons.add(cat[0])
                back_menu = (texts.back_button)
                buttons.add(back_menu)

                await message.answer("Главные категории", reply_markup = buttons)
            #------------------------------ПОДКАТЕГОРИИ------------------------------#
            elif podcateg_active and aastate != "del_categ:name" and aastate != "add_podcateg:categ" and aastate != "add_podcateg:name" and aastate != "del_podcateg:categ" and aastate != "add_tovar:categ" and aastate != "del_tovar:categ"and aastate != "plus_tovar:categ":
                buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                podcats = db.get_podcat_by_parent(text,True)
                for podcat in podcats:
                    buttons.add(podcat[0])
                back_menu = (texts.back_button)
                buttons.add(back_menu)

                await message.answer("Подкатегории", reply_markup = buttons)
            #--------------------------------ТОВАРЫ----------------------------------#
            elif tovar_active and aastate != "del_podcateg:name" and aastate != "add_tovar:podcateg" and aastate != "del_tovar:podcateg"and aastate != "plus_tovar:tt" and aastate != "plus_tovar:podcateg":
                buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                products = db.get_prod_by_parent(text,True)
                for tov in products:
                    buttons.add(tov[0])
                back_menu = (texts.back_button)
                buttons.add(back_menu)

                await message.answer("Товары", reply_markup = buttons)
            #----------------ТОВАР_ВЫБРАН_ПОКАЗ_ОПИСАНИЯ_И_ПОКУПКА-------------------#
            elif tovar_chosen and aastate != "del_tovar:name" and aastate != "plus_tovar:name" and aastate != "plus_tovar:tt":
                buttons = InlineKeyboardMarkup(resize_keyboard=True)
                product = db.get_prod_advanced(text,True)
                tovar = "buy_"+product[3]
                buy_button = InlineKeyboardButton('Купить!', callback_data=tovar)
                buttons.add(buy_button)
                msg_text = "{}\nОсталось товара: {}\nЦена: {}".format(product[0],product[2],product[1])

                await message.answer(msg_text, reply_markup = buttons)
            #---------------------------БИТКОИН_ПЕРЕВОД------------------------------#
            elif text == texts.btc_pay_button:
                await btc_pay_balance.money.set()
                buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                back_menu = (texts.back_button)
                buttons.add(back_menu)

                await message.answer(texts.deposit_btc_pay,reply_markup = buttons)
            #---------------------------ЭЛЕКТРОННЫЙ_ПЕРЕВОД--------------------------#
            elif text == texts.eticket_pay_button:
                await crystal_pay.money.set()

                buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                back_menu = (texts.back_button)
                buttons.add(back_menu)

                await message.answer(texts.deposit_crystal_pay,reply_markup = buttons)
            #---------------------------STATES---------------------------------------#
            else:
               state = dp.current_state(chat = message.chat.id, user = message.from_user.id)
               astate = await state.get_state()
               if astate == "btc_pay_balance:money":
                   try:
                       if int(message.text) >=1:

                           await state.update_data(money=message.text)
                           await btc_pay_balance.next()
                           await message.answer(texts.deposit_btc_check)
                   except:
                        await message.answer("Сумма указана некорректно!")
               elif astate == "btc_pay_balance:check":
                   user_data = await state.get_data()
                   amount = user_data['money']
                   await state.finish()
                   good = InlineKeyboardButton('Принять',callback_data=f'good_{message.from_user.id}_{amount}')
                   bad = InlineKeyboardButton('Отклонить',callback_data=f'bad_{message.from_user.id}')
                   inlineb = InlineKeyboardMarkup().add(good,bad)
                   await bot.send_message(db.get_log_chat(),texts.deposit_go_to_log_channel.format(username = message.from_user.username,user_id = message.from_user.id,amount = user_data['money'],check = message.text),reply_markup = inlineb)
               elif astate == "crystal_pay:money":
                   row = get(f"https://api.crystalpay.ru/api.php?s={settings.crystal_token}&n={settings.crystal_pay_name}&o=generate&amount={message.text}").text
                   row = json.loads(row)
                   #https://pay.crystalpay.ru/?i=

                   await state.finish()
                   pay = InlineKeyboardButton('Оплатить', url = f"https://pay.crystalpay.ru/?i={row['id']}")
                   check_payment = InlineKeyboardButton('Проверить оплату',callback_data=f"check_{row['id']}")
                   inlineb = InlineKeyboardMarkup().add(pay).add(check_payment)
                   await message.answer(texts.deposit_btc_pay,reply_markup = inlineb)
               elif astate == "pr_make:get_text":
                    await state.finish()
                    Pr_set.text = message.text
                    await message.answer("Текст рассылки был установлен!")
               elif astate == "ref_proc:get":
                    await state.finish()
                    db.change_ref_proc(message.text)
                    await message.answer("Новый процент был установлен.")
               elif astate == "add_piar_1:name":
                    await state.update_data(name=message.text)
                    await add_piar_1.next()
                    await message.answer("Введите текст кнопки.")
               elif astate == "add_piar_1:text":
                    user_data = await state.get_data()
                    db.change_button(user_data['name'],message.text,1)
                    await message.answer("Кнопка включена!")

               elif astate == "add_piar_2:name":
                    await state.update_data(name=message.text)
                    await add_piar_2.next()
                    await message.answer("Введите текст кнопки.")
               elif astate == "add_piar_2:text":
                    user_data = await state.get_data()
                    db.change_button(user_data['name'],message.text,2)
                    await message.answer("Кнопка включена!")
               elif astate == "add_categ:name":
                    db.add_cat(message.text)
                    await state.finish()
                    await message.answer("Категория добавлена!")
               elif astate == "del_categ:name":
                    db.del_cat(message.text)
                    await state.finish()
                    categ_button = ("🎁 Категории 🎁")
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    buttons.add(categ_button)
                    await message.answer("Категория удалена !", reply_markup = buttons)
               elif astate == "add_podcateg:categ":
                    await state.update_data(categ=message.text)
                    categ_button = ("💣 Подкатегории 💣")
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    buttons.add(categ_button)
                    await add_podcateg.next()
                    await message.answer("Отправь название подкатегории.", reply_markup = buttons)
               elif astate == "add_podcateg:name":
                    user_data = await state.get_data()
                    await state.finish()
                    db.add_podcat(user_data['categ'],message.text)
                    await message.answer("Подкатегория была добавлена!")
               elif astate == "del_podcateg:categ":
                    await state.update_data(categ=db.get_podcat_by_parent(message.text,True))
                    categ_button = ("💣 Подкатегории 💣")
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    buttons.add(categ_button)
                    podcats = db.get_podcat_by_parent(text,True)
                    for podcat in podcats:
                        buttons.add(podcat[0])
                    back_menu = (texts.back_button)
                    buttons.add(back_menu)
                    await del_podcateg.next()
                    await message.answer("Отправь название подкатегории.", reply_markup = buttons)
               elif astate == "del_podcateg:name":
                    user_data = await state.get_data()
                    await state.finish()
                    db.del_podcat(message.text)
                    await message.answer("Подкатегория была удалена!")
               elif astate == "add_tovar:categ":
                    await add_tovar.next()
                    categ_button = ("💰 Товары 💰")
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    buttons.add(categ_button)
                    podcats = db.get_podcat_by_parent(text,True)
                    for podcat in podcats:
                        buttons.add(podcat[0])
                    await message.answer("💣 Подкатегории 💣", reply_markup = buttons)
               elif astate == "add_tovar:podcateg":
                    await state.update_data(podcateg=message.text)
                    await add_tovar.next()

                    categ_button = ("💰 Товары 💰")
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    await message.answer("Отправь мне название",  reply_markup = buttons)
               elif astate == "add_tovar:name":
                    await state.update_data(name=message.text)
                    await message.answer("Сколько он будет стоить?")
                    await add_tovar.next()
               elif astate == "add_tovar:price":
                    await state.update_data(price=message.text)
                    await add_tovar.next()
                    await message.answer("Отправь описание товара")
               elif astate == "add_tovar:desc": # del_tovar(tovid) get_prodid_by_name(name)
                    user_data = await state.get_data()
                    await state.finish()
                    db.add_prod(user_data['podcateg'],user_data['name'],user_data['price'],message.text)
                    await message.answer("Товар добавлен.")


               elif astate == "del_tovar:categ":
                    await del_tovar.next()
                    categ_button = ("💰 Товары 💰")
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    buttons.add(categ_button)
                    podcats = db.get_podcat_by_parent(text,True)
                    for podcat in podcats:
                        buttons.add(podcat[0])
                    await message.answer("💣 Подкатегории 💣", reply_markup = buttons)
               elif astate == "del_tovar:podcateg":
                    await del_tovar.next()
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    products = db.get_prod_by_parent(text,True)
                    for tov in products:
                        buttons.add(tov[0])
                    await message.answer("Товары", reply_markup = buttons)
               elif astate == "del_tovar:name":
                    await state.update_data(name=message.text)
                    db.del_tovar(db.get_prodid_by_name(message.text))
                    categ_button = ("💰 Товары 💰")
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    buttons.add(categ_button)
                    await message.answer("Товар удалён", reply_markup = buttons)
                    await state.finish()






               elif astate == "plus_tovar:categ":
                    await plus_tovar.next()
                    categ_button = ("💰 Товары 💰")
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    buttons.add(categ_button)
                    podcats = db.get_podcat_by_parent(text,True)
                    for podcat in podcats:
                        buttons.add(podcat[0])
                    await message.answer("💣 Подкатегории 💣", reply_markup = buttons)
               elif astate == "plus_tovar:podcateg":
                    await plus_tovar.next()
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    
                    products = db.get_prod_by_parent(text,True)
                    for tov in products:
                        buttons.add(tov[0])
                    await message.answer("Товары", reply_markup = buttons)
               elif astate == "plus_tovar:tt":
                    await state.update_data(name=message.text)
                    await plus_tovar.next()
                    categ_button = ("💰 Товары 💰")
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    buttons.add(categ_button)
                    await message.answer("Отправьте мне товар, каждые данные должны начинаться с новой строки", reply_markup = buttons)
               elif astate == "plus_tovar:name":
                    user_data = await state.get_data()
                    tove = text.split("\n")
                    for x in tove:
                        if x.replace(" ",""):
                            db.add_prod_real(db.get_prodid_by_name(user_data['name']),x)
                    categ_button = ("💰 Товары 💰")
                    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                    buttons.add(categ_button)
                    await message.answer("Товар пополнен", reply_markup = buttons)
                    await state.finish()

               
               
               else: # add_prod_real(prodid,datayoba):
                   button_text = db.get_button_name(message.text)
                   if button_text != "0":
                       await message.answer(button_text[0]) 
                    #Head Admin's comm_ass
                   if int(message.from_user.id) in settings.head_admin:
                        if text.startswith("/addday"):
                            day = text.replace("/addday","").replace(" ","")
                            db.plus_day(day)
                            await message.answer(f"Срок был продлён на {day} дней. ")  
                        elif text == "/addlog":
                            db.add_log(message.chat.id)


                        elif text.startswith("/addcat"): # /addcat catname
                            catname = text.replace("/addcat","").replace(" ","")
                            try:
                                db.add_cat(catname)
                            except:
                                pass
                            await message.answer(f"Добавлена новая категория: {catname}")
                        elif text.startswith("/addpodcat"): # /addpodcat catname podcatname
                            podcatname = text.replace("/addpodcat ","")
                            hopeless = podcatname.split()
                            try:
                                db.add_podcat(hopeless[0],hopeless[1])
                            except:
                                pass
                            await message.answer("Добавлена новая подкатегория {} , к категории {}".format(hopeless[1],hopeless[0]))
                        elif text.startswith("/addprod"): # /addprod podcatname tovarname price description
                            podcatname = text.replace("/addprod ","")
                            hope = podcatname.split()
                            desc = hope[4].replace("_"," ")
                            try:
                                sos = db.add_prod(hope[0],hope[1],hope[2],desc)
                            except:
                                sos = "ERROR - TOVAR NOT DOBAVLEN"
                            await message.answer("Добавлен товар {} , к подкатегории {}, ценой {} рублей и идентефикатором {}".format(hope[2],hope[1],hope[3],sos))
                        elif text.startswith("/adddataprod"): # /adddataprod id data
                            product = text.replace("/adddataprod ","")
                            product = product.split()
                            error = False
                            try:
                                db.add_prod_real(product[0],product[1])
                            except:
                                error = True
                            if error:
                                await message.answer("ERROR - Неверно введен id товара.")
                            else:
                                await message.answer(f"Добавлен новый товар к id {product[0]}")




    else:
        await message.answer("Срок аренды бота истёк.")
        if int(message.from_user.id) in settings.head_admin:
            if text.startswith("/addday"):
                day = text.replace("/addday","").replace(" ","")
                db.plus_day(day)
                await message.answer(f"Срок был продлён на {day} дней. ")

async def die(wait_for):
    now_time_first = datetime.datetime.now().day
    
    #datetime.datetime.now().day
    while True:
        await asyncio.sleep(wait_for)
        now_date = datetime.datetime.now().day
        if now_date != now_time_first:
            now_time_first = now_date
            date = db.get_bot()
            if int(date[0]) == 1:
                db.minus_day(1)
                await bot.send_message(settings.admin,"Срок аренды бота был завершён!\nОбратитесь к продавцу, если что-то пошло не так.\nВаши товары будут сохранены на нашем сервере еще около 48 часов.")
            elif int(date[0]) == 2:
                db.minus_day(1)
                await bot.send_message(settings.admin,"Срок аренды бота подходит к концу.\nОстался один день.")
            elif int(date[0]) == 0:
                pass
            else:
                db.minus_day(1)





@dp.callback_query_handler()
async def process_callback_button1(callback_query: types.CallbackQuery):
    if callback_query.data.startswith("buy_"):
        tovid = callback_query.data.replace("buy_","")
        balan = db.get_ebal(callback_query.message.chat.id)
        cost = db.get_price_byid(int(tovid))
        if int(balan[0]) >= int(cost[0]):
            txt = db.get_prod_real_1(tovid)
            if txt == "AMOUNT":
                await callback_query.answer(text="Продукта нет на складе")
            else:
                txt = db.get_prod_real(tovid)
                await bot.send_message(callback_query.message.chat.id,text = txt[0][0])
                db.minus_balance(callback_query.message.chat.id,cost[0])
                product = db.get_prod_advanced_by_id(tovid,True)
                msg_text = "{}\nОсталось товара: {}\nЦена: {}".format(product[0],product[2],product[1])
                buttons = InlineKeyboardMarkup(resize_keyboard=True)
                tovar = "buy_"+product[3]
                buy_button = InlineKeyboardButton('Ещё купить!', callback_data=tovar)
                buttons.add(buy_button)
                await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=msg_text, reply_markup = buttons)	

        else:
            await callback_query.answer(show_alert=True,text="Вы бомжара. Внесите денег.")
    elif callback_query.data.startswith("good_"):
        data = callback_query.data.split("_")
        db.plus_balance(data[1],data[2])
        await bot.send_message(data[1],f"✔ Ваш баланс пополнен на {data[2]}p!✔ ")
        await bot.delete_message(callback_query.message.chat.id,callback_query.message.message_id)
    elif callback_query.data.startswith("bad_"):
        data = callback_query.data.split("_")
        await bot.send_message(data[1],f"❌ Вам было отказано в пополнении чеком BTC! ❌")
    elif callback_query.data.startswith("check_"):
        data = callback_query.data.split("_")
        url = f"https://api.crystalpay.ru/api.php?s={settings.crystal_token}&n={settings.crystal_pay_name}&o=checkpay&i={data[1]}_{data[2]}"
        row = get(url).text
        row = json.loads(row)

        
        if row['state'] == "notpayed":
            await bot.send_message(callback_query.message.chat.id,"❌ Вы не оплатили! ❌")
        elif row['state'] == "payed":
            db.plus_balance(callback_query.message.chat.id,row['amount'])
            await bot.send_message(callback_query.message.chat.id,f"✔ Ваш баланс пополнен на {row['amount']}p!✔ ")
            await bot.delete_message(callback_query.message.chat.id,callback_query.message.message_id)

if __name__ == '__main__':
    dp.loop.create_task(die(10)) 
    executor.start_polling(dp, skip_updates=True)