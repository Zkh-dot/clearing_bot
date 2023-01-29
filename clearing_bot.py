import telebot
from storage_worker import get, save, get_user, save_users

# Define a list to store the remembered users
remembered_users = get_user('users.txt')

password = input('please, ender your password: ')

# Define a dictionary to store the numbers entered by each user
try:
    user_numbers = get('cash_data.txt', password)
except:
    save({}, 'cash_data.txt', password)
    user_numbers = {}
# Create a bot instance using the token
bot = telebot.TeleBot("*****")

# Decorator to handle the /start command
@bot.message_handler(commands=['start'])
def handle_start(message):
    user = message.from_user.username
    if user in remembered_users:
        bot.send_message(chat_id=message.chat.id, text="Вас, увожаемый, уже записали, отвалите")
    else:
        remembered_users.append(user)
        bot.send_message(chat_id=message.chat.id, text="User {} has been added to the remembered users.".format(user))
        save_users(remembered_users, "users.txt")

# Decorator to handle the /stop command
@bot.message_handler(commands=['stop'])
def handle_stop(message):
    user = message.from_user.username
    # remembered_users.remove(user)
    bot.send_message(chat_id=message.chat.id, text="User {} has been removed from the remembered users.".format(user))

@bot.message_handler(commands=['balance'])
def handle_balance(message):
    # print(remembered_users)
    print(remembered_users)
    for user in remembered_users:
        if user == message.from_user.username:
            continue
        # print(user_numbers, user + message.from_user.username)
        # print(user)
        try:
            money = user_numbers[message.from_user.username + user]
            print(money)
            if money > 0: 
                bot.send_message(chat_id=message.chat.id, text="{} own you {}".format(user, money))
            elif money < 0:
                bot.send_message(chat_id=message.chat.id, text="You own {} {}".format(user, money))
        except Exception as e:
            pass        
        try:
            money = user_numbers[user + message.from_user.username]
            print(money)
            if money < 0: 
                bot.send_message(chat_id=message.chat.id, text="{} own you {}".format(user, money))
            elif money > 0:
                bot.send_message(chat_id=message.chat.id, text="You own {} {}".format(user, money))
        except Exception as e:
            pass
        
        
        

# Decorator to handle the /list command
@bot.message_handler(commands=['list'])
def handle_list(message):
    # Create a list of buttons with the names of the remembered users
    buttons = [telebot.types.InlineKeyboardButton(text=user, callback_data=user) for user in remembered_users]
    
    # Create a markup object for the buttons
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(*buttons)
    
    bot.send_message(chat_id=message.chat.id, text="Select a user:", reply_markup=markup)

# Decorator to handle user input of numbers
@bot.callback_query_handler(func=lambda call: call.data in remembered_users)
def handle_number_input(call):
    user = call.data
    bot.answer_callback_query(callback_query_id=call.id, text="Введите, сколько вы должны {}:".format(user))
    bot.register_next_step_handler(call.message, lambda message: process_number_step(message, user))

def process_number_step(message, user):
    try:
        number = int(message.text)
    except:
        bot.send_message(chat_id=message.chat.id, text="Кринж.")
        return
    if number < 0:
        bot.send_message(chat_id=message.chat.id, text="Ахаахаахаахахах пошел нахуй.")
        return
    if user + message.from_user.username in user_numbers:
        user_numbers[user + message.from_user.username] += number
    elif message.from_user.username + user in user_numbers:
        user_numbers[message.from_user.username + user] -= number
    else:
        user_numbers[user + message.from_user.username] = number
    bot.send_message(chat_id=message.chat.id, text="Вы должны {} {}".format(number, user))
    save(user_numbers, 'cash_data.txt', password)



# Start polling for messages
bot.polling()
