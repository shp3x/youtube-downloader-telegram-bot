from aiogram import Bot, Dispatcher, executor, types
from keyboards import download_kb
from pytube import YouTube
import sqlite3
import func
import os

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

bot = Bot('')
dp = Dispatcher(bot)

links = ['https://www.youtube.com', 'https://www.youtu.be', 'youtube.com', 'youtu.be']


@dp.message_handler(commands=['start'])
async def start(message):
    user_id = message.from_user.id
    link = ''

    await func.db_table_val(user_id=user_id, link=link)
    await bot.send_message(message.chat.id, '<b>Welcome!</b>\n\n'
                                            'With this bot you can download videos from YouTube - just send me the link!', parse_mode='HTML')


@dp.message_handler(content_types=['text'])
async def main(message):
    for link in links:
        if link in message.text:
            await func.add_link(message)
            await bot.send_message(message.chat.id, '<b>File found successfully</b>', reply_markup=download_kb, parse_mode='HTML', reply_to_message_id=message.message_id)
            break

    else:
        await bot.send_message(message.chat.id, '<b>❌ Invalid link</b>', parse_mode='HTML')


@dp.callback_query_handler()
async def callbacks(call):
    if call.data == 'download_audio':
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.answer_callback_query(call.id, '🕔 File is downloading...', cache_time=3)

        link = cursor.execute(f"SELECT link FROM main WHERE user_id = {call.from_user.id}").fetchone()[0]

        yt = YouTube(link)
        stream = yt.streams.filter(only_audio=True).first()
        size = stream.filesize
        url = stream.url

        if size > 50000000:

            save_kb = types.InlineKeyboardMarkup(row_width=1)
            main_link = types.InlineKeyboardButton('Прямая ссылка', url=url)
            save_kb.add(main_link)

            await bot.send_message(call.message.chat.id, '*⚠️File is too big*\n\n'
                                                         '_To download it - use the menu below ⬇_', reply_markup=save_kb)

        elif size < 50000000:

            file = stream.download()
            await bot.send_audio(call.message.chat.id, audio=open(f'{file}', 'rb'))
            await func.clear_link_field(call)
            os.remove(f'{file}')

    elif call.data == 'download_video':
        await bot.answer_callback_query(call.id, '🕔 File is downloading...')
        await bot.delete_message(call.message.chat.id, call.message.message_id)

        link = cursor.execute(f"SELECT link FROM main WHERE user_id = {call.from_user.id}").fetchone()[0]

        yt = YouTube(link)
        stream = yt.streams.get_highest_resolution()
        size = stream.filesize
        url = stream.url

        if size > 50000000:

            savefrom_link = 'https://ru.savefrom.net/?url=' + link

            save_kb = types.InlineKeyboardMarkup(row_width=1)
            main_link = types.InlineKeyboardButton('Direct link', url=url)
            sf_btn = types.InlineKeyboardButton('Download with Savefrom.net', url=savefrom_link)
            save_kb.add(main_link, sf_btn)

            await bot.send_message(call.message.chat.id, '*⚠️File is too big*\n\n'
                                                         '_To download it - use the menu below ⬇_', reply_markup=save_kb)

        elif size < 50000000:

            file = stream.download()
            await bot.send_document(call.message.chat.id, document=open(f'{file}', 'rb'))
            await func.clear_link_field(call)
            os.remove(f'{file}')


executor.start_polling(dp, skip_updates=True)
