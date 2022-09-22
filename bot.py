# -*- coding: utf-8 -*-
import os
from aiogram import Bot, Dispatcher, executor, types
import logging
import config
from pytube import YouTube
from db import Database

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.token)
dp = Dispatcher(bot)
db = Database('botdata.db')


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    if not db.user_exist(message.from_user.id):
        db.add_user(message.from_user.id)
    await bot.send_message(message.from_user.id,
                           f"Welcome, {message.from_user.first_name}! \n\nSend me a youtube link and I'll download it for you",
                           parse_mode="Markdown")


@dp.message_handler(commands=['broken'])
async def send_welcome(message: types.Message):
    if message.from_user.id == 555066955:
        rassilka = message.text[8:]
        users = db.get_users()
        for row in users:
            try:
                await bot.send_message(row[0], rassilka)
                if int(row[1]) != 1:
                    db.active(row[0], 1)
            except:
                db.active(row[0], 0)
        await bot.send_message(message.from_user.id, 'Рассылка успешна')


@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    if message.text.startswith('https://www.youtube.com'):
        link = f"{message.text}"
        yt = YouTube(link)
        ys = yt.streams.filter(res="720p").first()
        ys.download(filename=f'{message.from_user.id}.mp4')
        videos = open(f'{message.from_user.id}.mp4', 'rb')
        await bot.send_video(message.chat.id, video=videos, width=1920, height=1080)
        os.remove(f"{message.from_user.id}.mp4")
    else:
        await bot.send_message(message.from_user.id, 'I don’t understand you! Send me a link to YouTube video!!!')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
