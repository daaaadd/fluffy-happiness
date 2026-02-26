import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# ТВОЙ ТОКЕН (я уже вставил)
TOKEN = "8562983961:AAG3BxIR24Ruqx0YsW_j36zlmvo3QFAmmsY"

# КОМАНДА /start
async def start(update: Update, context):
    await update.message.reply_text('Привет! Отправь ссылку на TikTok видео')

# ЭТО ГЛАВНАЯ ФУНКЦИЯ КОТОРАЯ КАЧАЕТ ВИДЕО
async def handle_message(update: Update, context):
    # Получаем ссылку от пользователя
    url = update.message.text
    
    # Проверяем что это TikTok
    if 'tiktok.com' not in url:
        await update.message.reply_text('Это не ссылка на TikTok!')
        return
    
    # Пишем что начали качать
    status_message = await update.message.reply_text('⏳ Скачиваю видео...')
    
    # НАСТРОЙКИ СКАЧИВАНИЯ
    ydl_opts = {
        'format': 'best',           # лучшее качество
        'outtmpl': 'video.%(ext)s', # сохранить как video.mp4
        'quiet': True,               # не показывать лишнего
    }
    
    try:
        # СОЗДАЕМ СКАЧИВАЛЬЩИК
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # СКАЧИВАЕМ ВИДЕО
            ydl.download([url])
        
        # ИЩЕМ СКАЧАННЫЙ ФАЙЛ
        video_file = None
        for file in os.listdir():
            if file.startswith('video.'):
                video_file = file
                break
        
        # ЕСЛИ НАШЛИ ФАЙЛ - ОТПРАВЛЯЕМ
        if video_file:
            with open(video_file, 'rb') as f:
                await update.message.reply_video(f)
            
            # УДАЛЯЕМ ФАЙЛ ЧТОБ НЕ ЗАСОРЯТЬ
            os.remove(video_file)
            await status_message.delete()
        else:
            await status_message.edit_text('Не нашел файл :(')
            
    except Exception as e:
        await status_message.edit_text(f'Ошибка: {str(e)}')

# ЗАПУСК БОТА
def main():
    print("Бот запускается...")
    
    # Создаем бота с твоим токеном
    app = Application.builder().token(TOKEN).build()
    
    # Добавляем команды
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    print("Бот работает! Отправь ему ссылку на TikTok")
    app.run_polling()

if __name__ == '__main__':
    main()
