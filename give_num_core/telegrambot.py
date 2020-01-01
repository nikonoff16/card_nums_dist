from bootstrapping_module import *
from commands import *
import telebot
import telegrame
import archived_nums

__version__ = "1.2.0"

last_int_path = Path.combine(archived_nums.script_dir, "last.txt")

encrypted_telegram_token = [-24, -60, 1, -12, -55, -41, -58, 17, -16, -53, 6,
                            -2, -39, -28, -53, 76, 36, -7, 26, 20, -18, 20, -35,
                            37, 12, -7, 2, 1, -23, 7, -21, 71, 7, -24, 34, 11,
                            18, -45, -56, 77, 1, -24, 34, 39, 9, 14]  # production


def reset_password():
    password = Str.input_pass()
    GIV["api_password_vic"] = password
    return password


try:
    password = GIV["api_password_vic"]
    if "reset" in sys.argv:
        password = reset_password()
except (NameError, KeyError):
    password = reset_password()

telegram_token = Str.decrypt(encrypted_telegram_token, password)

telegram_api = telebot.TeleBot(telegram_token, threaded=False)


def start_todoist_bot(none_stop=True):
    telegram_api = telebot.TeleBot(telegram_token, threaded=False)

    @telegram_api.message_handler(commands=["start"])
    def start_message(message):

        markup = telebot.types.ReplyKeyboardMarkup()
        more_button = telebot.types.KeyboardButton("Номер карточки!")

        i2_button = telebot.types.KeyboardButton("2")
        i5_button = telebot.types.KeyboardButton("5")
        i10_button = telebot.types.KeyboardButton("10")

        i100_button = telebot.types.KeyboardButton("100")

        markup.row(more_button)
        markup.row(i2_button, i5_button, i10_button, i100_button)

        telegrame.send_message(telegram_api, message.chat.id,
                               f"Приветствую в боте для выдачи номеров карт! Укажите цифрой нужное вам количество номеров, "
                               f"или воспользуйтесь специальной клавиатурой для этого. Приятного использования!",
                               reply_markup=markup)

    @telegram_api.message_handler(content_types=["text"])
    def message_hanlder(message):
        # init vars
        chat_id = message.chat.id
        message_id = message.message_id
        try:
            print(chat_id, message_id, message.text)
        except:
            print(chat_id, message_id)

        # actual logic

        try:
            count = int(message.text)
        except ValueError:
            count = 1

        integers = []
        for i in range(count):
            integer = int(File.read(last_int_path))

            while not archived_nums.check_archive(integer):
                integer += 1

            File.write(last_int_path, integer, mode="w")
            integers.append(str(integer))

        markup = telebot.types.ReplyKeyboardMarkup()
        more_button = telebot.types.KeyboardButton("Ещё одну")

        i2_button = telebot.types.KeyboardButton("2")
        i5_button = telebot.types.KeyboardButton("5")
        i10_button = telebot.types.KeyboardButton("10")

        i100_button = telebot.types.KeyboardButton("100")

        markup.row(more_button)
        markup.row(i2_button, i5_button, i10_button, i100_button)

        telegrame.send_message(telegram_api, chat_id, f"{newline.join(integers)}", reply_markup=markup)
        # end of logic

    # start bot
    telegram_api.polling(none_stop=none_stop)
    # https://github.com/eternnoir/pyTelegramBotAPI/issues/273


def main():
    print(f"Bot started v{__version__}")
    telegrame.very_safe_start_bot(start_todoist_bot)


if __name__ == '__main__':
    main()
