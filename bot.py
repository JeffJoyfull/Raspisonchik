from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import datetime
import random

# 🔹 Расписание
schedule = {
    "понедельник": ["8:00 - Математика", "8:55 - Русский язык", "9:50 - Химия", "10:45 - Геометрия", "11:35 - Английский язык"],
    "вторник": ["8:00 - Русский язык", "8:55 - Физика", "9:50 - Литература", "10:45 - Русский язык", "11:35 - Геометрия"],
    "среда": ["8:00 - Биология", "8:55 - Геометрия", "9:50 - Казахский язык", "10:45 - ОБЖ", "11:35 - Казахский язык"],
    "четверг": ["8:00 - Английский язык", "8:55 - Английский язык", "9:50 - Физкультура", "10:45 - Физика", "11:35 - Литература"],
    "пятница": ["8:00 - Физкультура", "8:55 - Бизнес Английский", "9:50 - История", "10:45 - Информатика", "11:35 - Бизнес Английский"],
}

# 🔹 Клавиатура
keyboard = [["Сегодня", "Неделя"]]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# 🔹 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я умею делать много классных вещей. Например могу давать расписание, а ещееее... ну да, я могу только это.",
        reply_markup=reply_markup
    )

# 🔹 Команда "Сегодня"
async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    weekday = datetime.datetime.now().strftime('%A').lower()
    mapping = {
        'monday': 'понедельник',
        'tuesday': 'вторник',
        'wednesday': 'среда',
        'thursday': 'четверг',
        'friday': 'пятница',
        'saturday': 'суббота',
        'sunday': 'воскресенье',
    }
    day = mapping.get(weekday, "понедельник")
    subjects = schedule.get(day, ["Пар нет 😉"])
    await update.message.reply_text(f"📅 Расписание на сегодня ({day}):\n" + "\n".join(subjects))

# 🔹 Команда "Неделя"
async def week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "📚 Расписание на неделю:\n\n"
    for day, subjects in schedule.items():
        message += f"📅 {day.capitalize()}:\n" + "\n".join(subjects) + "\n\n"
    await update.message.reply_text(message)

# 🔹 Ответ на любое другое сообщение
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.datetime.now().hour

    if 6 <= now < 12:
        greetings = [
            "Доброе утро! С раннего утра думаешь о учебе, одобряю! Вот расписание такой сладкой булочке ;)",
            "С добрым утром! Готовимся к учебе? А как ты собрался к ней готовиться если даже расписания не знаешшь?! Вот держи 😉",
            "Утро доброе! Хочешь увидеть расписание? А ты уже успел снять котенка с дерева или спасти людей из горящего дома? Шучу, лови расписание",
            "Салют! Посмотри что у тебя сегодня, иначе не отвертишся от приколов по типу А ТЫ ГОЛОВУ ДОМА НЕ ЗАБЫЛ?"
        ]
    elif 12 <= now < 18:
        greetings = [
            "Днём всё видно лучше! Но я не вижу тебя на учебе! Посмотри что у тебя сегодня",
            "Хэй, кажется тебе следовало бы быть более осмотрительнее и внимательнее! Начнем с расписания 😉",
            "Вот тебе расписание уроков, пирожочек с вареньем и пицца с ананасами. Шучу, у меня только расписание! Все остальное через донат...",
            "ВАС ПРИВЕТСТВУЕТ АВТОМАТИЗИРОВАННАЯ СИСТЕМА ПО ВЫДАЧЕ КАРТОЧЕК РАСПИСАНИЯ UNISX XXL3310. Я МОГУndiucewie9832nd;kwd. АХахахах, как я тебя развел, держи расписание"
        ]
    else:
        greetings = [
            "Приятного вечерочка. А что вдруг мы о учебе задумались? Может быть начнем с расписания?",
            "Слушай, просто иди поспи, серьезно! Но сначала проверь что у тебя на завтра",
            "Тебе только расписание от меня надо! Забирай его и иди к своим чатикам гпт!",
            "Анекдот на ночь. Студент спрашивает у преподователя... Ладно, мой юмор никому не нужен. Держи свое расписание"
        ]

    text = random.choice(greetings)
    await update.message.reply_text(
        text,
        reply_markup=reply_markup
    )

# 🔹 Запуск бота
app = ApplicationBuilder().token("7837539451:AAEf7JBaATBT4SRwfWyHPoKZjh2NrdDuGUA").build()  # ← сюда вставь токен

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Text("Сегодня"), today))
app.add_handler(MessageHandler(filters.Text("Неделя"), week))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))

app.run_polling()
