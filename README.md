# Ласкаво просимо до проєкту "AI CheckBot" 🤖📋

## Огляд

"AI CheckBot" - це Telegram-бот, спрямований на ефективну перевірку та аналіз локацій користувачів. Бот надає можливість користувачам заповнити чек-лист, обираючи статус для кожного пункту, додавати коментарі та навіть прикріплювати фотографії. Завершивши чек-лист, користувач отримує звіт, який автоматично відправляється на аналіз штучному інтелекту OpenAI.

## Як почати

### Встановлення через Git:

1. Клонуйте репозиторій:

```bash
git clone https://github.com/kostomeister/py-telegram-bot.git
cd py-telegram-bot
```

2. Встановіть необхідні залежності:

```bash
pip install -r requirements.txt
```
3. Зараньте міграції
```
alembic upgrade head
```

4. Створіть файл `.env` та заповніть його своїм токеном Telegram та OpenAI:

```python
# .env
OPENAI_API_KEY=OPENAI_API_KEY
BOT_TOKEN=BOT_TOKEN
```

5. Запустіть бота:

```bash
python bot.py
```
### Встановлення через Docker з гітхабу:

1. Клонуйте репозиторій:

```bash
git clone https://github.com/kostomeister/py-telegram-bot.git
cd py-telegram-bot
```

2. Створіть файл `.env` та заповніть його своїм токеном Telegram та OpenAI:

```python
# .env
OPENAI_API_KEY=OPENAI_API_KEY
BOT_TOKEN=BOT_TOKEN
```

3. Запустіть бота через Docker:

```bash
docker build -t telegram .
docker run telegram
```

Пам'ятайте, що `.env` файл повинен бути створений та заповнений перед запуском контейнера.

## Використання

1. Почніть розмову з ботом.
2. Вам буде відправлене вітальне повідомлення.
3. Виберіть локацію та заповніть чек-лист.
4. Додайте коментар та прикріпіть фотографію.
5. Завершіть чек-лист та отримайте звіт від штучного інтелекту OpenAI.

## Особливості

- 📊 **База даних**: Зручне збереження та управління даними за допомогою вбудованої бази даних.
- 📸 **Надсилання фотографій**: Можливість прикріплення фотографій до коментарів та збереження посилань на них.
- 🤖 **Вбудований AI**: Автоматична аналітика звітів штучним інтелектом для отримання докладних результатів.
- 🐳 **Docker**: Швидке та легке розгортання бота та бази даних за допомогою Docker, який ізолює програми в контейнерах та гарантує їхню сумісність та безпеку.
- 🚀 **Повна асинхронність**: Проєкт побудований на основі асинхронного підходу, використовуючи асинхронні функції, декоратори та бібліотеки для оптимізації роботи з базою даних, вводом/виводом та взаємодією з зовнішніми сервісами, забезпечуючи високу продуктивність та ефективність обробки подій в багатозадачному середовищі.
## Приклади коду

### Додавання нового функціоналу

```python
# Додавання нового функціоналу до обробника чек-листа

@dp.message_handler(state=BotState.NewFeature)
async def handle_new_feature(message: types.Message):
    # Ваш код для обробки нового функціоналу
    await message.answer("Новий функціонал додано!")
```

## Автори

- [kostomeister](https://github.com/kostomeister) - Developer

## Подяка

Дякуємо вам за використання "AI CheckBot"! Якщо у вас є питання або пропозиції, будь ласка, звертайтеся до нас. 🚀
