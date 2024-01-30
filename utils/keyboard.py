from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

locations_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
locations_keyboard.add(KeyboardButton("Локація 1"))
locations_keyboard.add(KeyboardButton("Локація 2"))
locations_keyboard.add(KeyboardButton("Локація 3"))
locations_keyboard.add(KeyboardButton("Локація 4"))
locations_keyboard.add(KeyboardButton("Локація 5"))

checklist_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
checklist_keyboard.add(KeyboardButton("Все чисто"))
checklist_keyboard.add(KeyboardButton("Залишити коментар"))

report_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
report_keyboard.add(KeyboardButton("/send_report"))

photo_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
photo_keyboard.add(KeyboardButton("Додати фото"))
photo_keyboard.add(KeyboardButton("Пропустити"))
