import telebot, random
import spreadsheet

TOKEN = 'Разместите здесь свой токен'

bot = telebot.TeleBot(TOKEN)

#Списки триггеров и реакций. Хранятся здесь, чтобы сборщик мусора не пожрал после вызова функции
class Logic_holder:

    triggers, reactions = spreadsheet.update_sheet()

    def update():
        Logic_holder.triggers, Logic_holder.reactions = spreadsheet.update_sheet()

    def detector(message):
        for objects in Logic_holder.triggers:
            for subject in objects:
                if subject in str(message.text).lower():
                    return True

    def answer(message):
        index = random.randrange(0, len(Logic_holder.triggers)-1)

        for i in range(len(Logic_holder.triggers)):
            for object in Logic_holder.triggers[i]:
                if object in str(message.text).lower():
                    index = i

        elements_count = len(Logic_holder.triggers[index])
        chosen_element = random.randrange(0, elements_count)
        reaction = Logic_holder.reactions[index][chosen_element]
        return reaction



@bot.message_handler(commands=['start',])
def send_welcome(message):
    bot.reply_to(message, "Всё в порядке, бот работает")

@bot.message_handler(func=Logic_holder.detector)
def say_back(message):
    try:
        chance = random.randrange(1, 9)
        if chance < 4:
            answer = Logic_holder.answer(message)
            bot.reply_to(message, answer)
    except:
        bot.reply_to(message, 'Ошибка в строке для данного триггера')

@bot.message_handler(commands=['update'])
def refresh(message):
    try:
        Logic_holder.update()
    except:
        bot.reply_to(message, 'Ошибка при получении данных таблицы')






bot.polling(none_stop=True)
