import re
import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# بيانات الحساب المساعد الخاص بك (الذي يسحب الميديا)
api_id = 36064345
api_hash = 'f120703574d1a114de4d623f99cd6dd2'
session_string = '1BJWap1wBuz4hdcewTcc1QXAyPKE2ylGStgYAr7BicWm87t61j__a9ZtcO3ekgmvNko9pxt7XTf4iMriMHnn-CDh1U2GbwmyAmMKBLt41a033Lgqxit8qZaTAUAMXngLQiIEtZOF2V09QIVJbGUyriV6Fe1MlhuWN6x80Lux_uNoOaQLiIQW4LQZSgN9_5DnxflSYboD36bDQAdHbRjRVRdpVgornsOxE9ACm1QCaU9grdXoyjTZ2XoaYenQkFn6jd8cen31NjVL7rNwAUxyY0Wc1QggNn0Vx6r83KzJ5v8_yUwVCMb5wbueLAeS1yZJIUSgRCa5guf-XbvVnlby-pG9givoL0='

# توكن البوت الخاص بك من BotFather
bot_token = '8683947335:AAGD-BkV4R357aJMdVjiYTNj7V9E8P4lU9k'

print("⏳ جاري تهيئة النظام والربط بالسيرفر السحابي...")
assistant = TelegramClient(StringSession(session_string), api_id, api_hash)
bot = TelegramClient('bot_cloud_session', api_id, api_hash)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("👋 مرحباً بك في بوت سحب الميديا السحابي المستقر!\n🔗 أرسل لي رابط المنشور المقيد الآن وسأقوم بجلبه فوراً.")

@bot.on(events.NewMessage)
async def handle_message(event):
    text = event.text.strip()
    if 't.me/c/' in text:
        status_msg = await event.reply("⏳ جاري سحب وتحميل الميديا سحابياً...")
        try:
            match = re.search(r't\.me/c/(\d+)/(\d+)', text)
            if not match:
                await status_msg.edit("❌ صيغة الرابط غير صحيحة.")
                return
                
            channel_id = int(f"-100{match.group(1)}")
            message_id = int(match.group(2))
            
            message = await assistant.get_messages(channel_id, ids=message_id)
            
            if message and message.media:
                await status_msg.edit("📥 تم السحب بنجاح، جاري الرفع إلى شات البوت...")
                file_path = await assistant.download_media(message)
                
                # إرسال الملف للمستخدم
                await bot.send_file(event.chat_id, file_path, caption=message.text or "")
                
                # تنظيف مساحة السيرفر فوراً للحفاظ على الاستقرار
                if os.path.exists(file_path):
                    os.remove(file_path)
                await status_msg.delete()
            else:
                if message and message.text:
                    await status_msg.edit(f"📝 المنشور يحتوي على نص فقط:\n\n{message.text}")
                else:
                    await status_msg.edit("❌ لم يتم العثور على ميديا في هذا الرابط.")
        except Exception as e:
            await status_msg.edit(f"❌ خطأ أثناء السحب السحابي: {str(e)}")

async def main():
    await assistant.start()
    await bot.start(bot_token=bot_token)
    print("🚀 البوت شغال الآن سحابياً وبأعلى كفاءة!")
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
