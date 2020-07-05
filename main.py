import telegram, logging, time, schedule, datetime, os
from telegram.ext import Updater, MessageHandler, ConversationHandler, CallbackQueryHandler, CommandHandler, Filters
from telegram.forcereply import ForceReply
from dateutil.relativedelta import relativedelta

url = ''
waktu = ''  
active = True
PRODUKNYA, PENGINGAT, BATAL = range(3) 

def start(update, context):
  update.message.reply_text('okay');
  update.message.reply_text(reply_markup=ForceReply(selective=True), text='Masukan link produk')  
  return PRODUKNYA
 

def product(update, context):
  global url
  url = update.message.text
  update.message.reply_text('format waktu harus seperti: \n contoh:\n 08:00\n 14:00\n 22:50\n');
  update.message.reply_text(reply_markup=ForceReply(selective=True), text='Masukan waktu flashsale')
  return PENGINGAT

def reminder(update, context):
  global waktu
  try:
    waktu = update.message.text
    # update.message.reply_text('produknya');
    # update.message.reply_text(url);
    # update.message.reply_text('waktu flashsale');
    # update.message.reply_text(waktu);
    mulai = datetime.datetime.now().time().strftime('%H:%M')
    akhir = str(waktu)
    selisih = relativedelta(datetime.datetime.strptime(akhir,'%H:%M'), datetime.datetime.strptime(mulai,'%H:%M'))
    waktunya = ('{h} jam {m} menit lagi'.format(h=selisih.hours, m=selisih.minutes))
    update.message.reply_text('okay, bot akan memberi kamu notifikasi jika waktu flashsale telah dimulai')
    update.message.reply_text('silahkan menunggu terlebih dahulu🤗')
    update.message.reply_text(waktunya)
    while active:
      nows = datetime.datetime.now().time().strftime('%H:%M')
      # if update.message.text == 'done':
      #   break
      # else:
      if(nows != waktu):
        print('not yet!');
      else:
        update.message.reply_text('Flashsale dimulai!');
        update.message.reply_text('produknya');
        update.message.reply_text(url);
        break
    return ConversationHandler.END
  except ValueError:
      update.message.reply_text(waktu);
      update.message.reply_text('format waktu salah!');
      update.message.reply_text('silahkan ulangin dari awal');
      return ConversationHandler.END 

def batalkan(update, context):
  update.message.reply_text('hi');
  # global active
  # henti = False
  # update.message.reply_text('dibatalkan');
  # update.message.reply_text('Batalkan pengingat?');
  # update.message.reply_text(reply_markup=ForceReply(selective=True), text='ya/tidak')
  # return ConversationHandler.END 
  # return BATAL


def batal(update, context):
  print("cancel")


def cancel(update, context):
    print("cancel")
    return ConversationHandler.END      

def main():
  updater = Updater (token='1157307067:AAHXt-c6iRrMsO102C-Gs8l54xSta8rRJ7U', use_context=True)
  dispatcher = updater.dispatcher

  logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

  create_conversation_handler = ConversationHandler(
        entry_points = [CommandHandler('start',start)],

        states = {
            PRODUKNYA: [MessageHandler(Filters.text, product)],
            PENGINGAT: [MessageHandler(Filters.text, reminder)],
            BATAL: [MessageHandler(Filters.text, batalkan)],
        },
        fallbacks = [CommandHandler('cancel',cancel)]
    )

  dispatcher.add_handler(create_conversation_handler)
  # dispatcher.add_handler(CommandHandler("cancel", batalkan))



  updater.start_polling()
  updater.idle()

if __name__ == '__main__':
    main()
