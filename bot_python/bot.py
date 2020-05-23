import telebot
import config
from db import SQLighter
import random
from telebot import types

bot = telebot.TeleBot(config.TOKEN)

#welcome message
@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/start.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    
    #keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Add file")
    item2 = types.KeyboardButton("Check history")
    item3 = types.KeyboardButton("Help guide")
    
    markup.add(item1,item2,item3)
    
    bot.send_message(message.chat.id, "Hello, traveller {0.first_name}!\nI am <b>{1.first_name}</b>\nBorn for making student`s life worse!".format(message.from_user, bot.get_me()), parse_mode="html", reply_markup=markup)

#save sent document to local folder documents
@bot.message_handler(content_types=['document'])
def save_document(message):
    try:
        try:
            save_dir = "documents"
        except:
            save_dir = os.getcwd()
            s = "[!] you aren't entered directory, saving to {}".format(save_dir)
            bot.send_message(message.chat.id, str(s))
        file_name = message.document.file_name
        file_id = message.document.file_name
        file_id_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_id_info.file_path)
        src = file_name
        if file_name.endswith("doc") or file_name.endswith("docx"):   
            with open(save_dir + "\\" + src, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.send_message(message.chat.id, "<i>«File uploaded...waiting for the results»</i>".format(message.from_user, bot.get_me()), parse_mode="html")  
            db_worker = SQLighter(config.database_name)
            db_worker.insert_student(file_name)
            db_worker.insert_project(save_dir + "\\" + src)
            tmp = save_dir + "\\" + src
            print(tmp)
            db_worker.insert_result(tmp)
            print("DONE")           
            result = db_worker.select_single(save_dir + "\\" + src)[0]
            db_worker.close()
            print("File loaded!")
            print(result)
            result_str = int(result[0])
            if result_str>60:
                sti = open('static/fail.webp', 'rb')
                bot.send_sticker(message.chat.id, sti)
                bot.send_message(message.chat.id, "<i>«Nice try...»</i>".format(message.from_user, bot.get_me()), parse_mode="html")
            elif result_str<40:
                sti = open('static/success.webp', 'rb')
                bot.send_sticker(message.chat.id, sti)
                bot.send_message(message.chat.id, "<i>«Success! Congratulations!»</i>".format(message.from_user, bot.get_me()), parse_mode="html")           
            else:
                sti = open('static/middle.webp', 'rb')
                bot.send_sticker(message.chat.id, sti)
                bot.send_message(message.chat.id, "<i>«Well, that will do, i guess...»</i>".format(message.from_user, bot.get_me()), parse_mode="html")
            bot.send_message(message.chat.id, "AVG Result: <b>"+str(result_str)+"%</b>".format(message.from_user, bot.get_me()), parse_mode="html")
            bot.send_message(message.chat.id, "<i>P.S. For detailed result view history -> log</i>".format(message.from_user, bot.get_me()), parse_mode="html")
        else:
            bot.send_message(message.chat.id, "File must be *.doc or *.docx")
    except Exception as ex:
        bot.send_message(message.chat.id, "[!] error - {}".format(str(ex)))

#menu replies  
@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.text=="Hi":
        welcome(message)
    elif message.text=="Add file":
        sti = open('static/add.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("Upload", callback_data='upload')
        item2 = types.InlineKeyboardButton("Help", callback_data='help')
        markup.add(item1, item2)
        bot.send_message(message.chat.id, "<i>«File addition mode is on, Sir!»\nP.S. The file name should be like this: <b>Surname_Name_FatherName_acadYear_faculty_group</b>\n<b>Example:Ivanov_Ivan_Ivanovich_3_Phisically_technical_IVT_1</b></i>".format(message.from_user, bot.get_me()), parse_mode="html", reply_markup=markup)    
    elif message.text=="Check history":
        sti = open('static/history.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton("Log", callback_data='log')
        markup.add(item1)
        bot.send_message(message.chat.id, "<i>«Hmmm... Let`s see what we have here.»</i>".format(message.from_user, bot.get_me()), parse_mode="html", reply_markup=markup)   
    elif message.text=="Help guide":
        sti = open('static/help.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
        bot.send_message(message.chat.id, "<i>«Well, i`m not sure that you need any help here, but here we go:»</i>".format(message.from_user, bot.get_me()), parse_mode="html")
        bot.send_message(message.chat.id, " - press «Add file» if you want to add file".format(message.from_user, bot.get_me()), parse_mode="html")
        bot.send_message(message.chat.id, " - press «Check History» if you want to view log".format(message.from_user, bot.get_me()), parse_mode="html")
        bot.send_message(message.chat.id, " - you also can drop file using usual telegram way of file loading".format(message.from_user, bot.get_me()), parse_mode="html")
        bot.send_message(message.chat.id, "<i>«WARNING!» <b>Before uploading make sure that your file doesn`t contain photoes and the front pages before annotation.</b></i>".format(message.from_user, bot.get_me()), parse_mode="html")
        bot.send_message(message.chat.id, "<i>«That`s all folks!»</i>".format(message.from_user, bot.get_me()), parse_mode="html")
    else:
        sti = open('static/sorry.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
        bot.send_message(message.chat.id, "<i>«Sorry, i`m limited with the actions to perform.»</i>".format(message.from_user, bot.get_me()), parse_mode="html")

#inline menu relies
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'upload':
                #bot.send_message(call.message.chat.id, 'File uploaded...waiting for the results')
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,text="Sorry but this way of uploading file is unavailable for now. You may try just add a document using standart telegram features.")
            elif call.data == 'help':
                #bot.send_message(call.message.chat.id, 'You need to upload the file for the uniqueness check!')
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="You need to upload the file for the uniqueness check!")
            elif call.data == 'log':
                db_worker = SQLighter(config.database_name)
                db_log = db_worker.select_all()
                log=""
                for db_log_single in db_log:
                    log += "".join(str(db_log_single)).strip('()') +"%\n\n"
                log = log.replace('documents\\\\','').replace('\'','').replace(',',' - ').replace('_',' ')
                print(log)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=log, reply_markup=None)
                db_worker.close()
    except Exception as e:
        print(repr(e))


#RUN
while True:
    try:
        print("[*] bot starting..")
        #bot.send_message(owner, "[*] bot starting..")
        print("[*] bot started!")
        #bot.send_message(owner, "[*] bot started!")
        bot.polling(none_stop=True, interval=2)
        # Предполагаю, что бот может мирно завершить работу, поэтому
        # даем выйти из цикла
        break

    except Exception as ex:
        print("[*] error - {}".format(str(ex))) # Описание ошибки
        #bot.send_message(owner, "[*] error - {}".format(str(ex)))
        print("[*] rebooting..")
        #bot.send_message(owner, "[*] rebooting..")
        bot.stop_polling()
        # Останавливаем чтобы не получить блокировку
        time.sleep(15)
        print("[*] restarted!")
        #bot.send_message(owner, "[*] restarted!")