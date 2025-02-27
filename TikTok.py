import telebot
import subprocess
import os

# بيانات البوت
TOKEN = "7724529903:AAFetOKziK54iY0U490GrGkYPWDk78lJ-Pk"  # استبدلها بتوكن البوت الخاص بك
bot = telebot.TeleBot(TOKEN)

# تخزين معرفات الرسائل لكل مستخدم لحذفها لاحقًا
user_messages = {}

print("""
-------------------------------------
  🚀 بوت تحميل الوسائط جاهز للعمل!  
  📥 يدعم: الفيديوهات، الصور، والصوتيات  
  🔥 أرسل الرابط وسأقوم بالتحميل  
-------------------------------------
""")

# تحميل الملفات من أي رابط
def download_media(url):
    cmd = f"yt-dlp -f best -o 'downloaded_media.%(ext)s' {url}"
    subprocess.run(cmd, shell=True)
    
    # البحث عن الملف الذي تم تحميله
    for file in os.listdir():
        if file.startswith("downloaded_media"):
            return file
    return None

# رسالة حقوق البوت
def footer_message():
    return """
-------------------------------------
   Ⓒ جميع الحقوق محفوظة لـ @Vaj80BoT
   🚀 بوت لتحميل الفيديوهات والصور والصوتيات.
-------------------------------------
"""

# رسالة الترحيب عند بدء الاستخدام
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_msg = f"""
👋 مرحبًا {message.chat.first_name}!
🎉 هذا البوت يساعدك على تحميل الفيديوهات والصور والصوتيات.

📥 فقط أرسل الرابط الذي تريد تحميله وسأقوم بمعالجته فورًا.
🔔 **للانضمام لقناة البوت**: @popou77

👥 **للاستفسار **: @hsooooo0

⚡ بمجرد الاشتراك، يمكنك تحميل أي وسائط بسرعة!

{footer_message()}
"""
    bot.reply_to(message, welcome_msg)

# استقبال الروابط وتحميل الوسائط
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text

    if any(domain in url for domain in ["tiktok.com", "youtube.com", "youtu.be", "instagram.com", "facebook.com", "twitter.com"]):
        bot.reply_to(message, "📥 جاري التحميل...")

        media_path = download_media(url)

        if media_path:
            with open(media_path, "rb") as media_file:
                if media_path.endswith((".mp4", ".mkv", ".avi")):
                    sent_msg = bot.send_video(message.chat.id, media_file)
                elif media_path.endswith((".jpg", ".jpeg", ".png", ".webp")):
                    sent_msg = bot.send_photo(message.chat.id, media_file)
                elif media_path.endswith((".mp3", ".m4a", ".wav", ".ogg")):
                    sent_msg = bot.send_audio(message.chat.id, media_file)
                else:
                    sent_msg = bot.send_document(message.chat.id, media_file)

            # حفظ معرف الرسالة لحذفها لاحقًا
            user_messages[message.chat.id] = sent_msg.message_id

            # حذف الملف بعد الإرسال
            os.remove(media_path)
        else:
            bot.reply_to(message, "❌ فشل التحميل، تأكد من صحة الرابط.")

    else:
        bot.reply_to(message, "❌ عذرًا، لا أتعرف على هذا الرابط.")

# حذف الرسالة عند الطلب
@bot.message_handler(commands=['delete'])
def delete_message(message):
    chat_id = message.chat.id

    if chat_id in user_messages:
        try:
            bot.delete_message(chat_id, user_messages[chat_id])  # حذف الفيديو
            bot.reply_to(message, "✅ تم حذف الوسائط بنجاح.")
            del user_messages[chat_id]  # إزالة الرسالة من السجل
        except Exception as e:
            bot.reply_to(message, "❌ لم أتمكن من حذف الوسائط.")
    else:
        bot.reply_to(message, "❌ لا يوجد وسائط لحذفها.")

# تشغيل البوت
bot.polling(none_stop=True, interval=0, timeout=60)