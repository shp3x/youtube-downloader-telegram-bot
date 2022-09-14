from aiogram import types

download_kb = types.InlineKeyboardMarkup(row_width=1)
download_audio = types.InlineKeyboardButton('🔉 Download audio', callback_data='download_audio')
download_video = types.InlineKeyboardButton('🎥 Download video', callback_data='download_video')
download_kb.add(download_audio, download_video)
