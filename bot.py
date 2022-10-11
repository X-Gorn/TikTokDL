"""
TikTok DL Bot
© All rights reserved by X-Gorn
Kangers don't f*ckin kang this !!!
Should have to give credits 😏 else f***off
"""

import json, requests, os, shlex, asyncio, uuid, shutil
from typing import Tuple
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

# Configs
API_HASH = os.environ['API_HASH']
APP_ID = int(os.environ['APP_ID'])
BOT_TOKEN = os.environ['BOT_TOKEN']
downloads = './downloads/{}/'

#Button
START_BUTTONS=[
    [
        InlineKeyboardButton("Source", url="https://github.com/X-Gorn/TikTokDL"),
        InlineKeyboardButton("Project Channel", url="https://t.me/xTeamBots"),
    ],
    [InlineKeyboardButton("Author", url="https://t.me/xgorn")],
]

DL_BUTTONS=[
    [
        InlineKeyboardButton("No Watermark", callback_data="nowm"),
        InlineKeyboardButton("Watermark", callback_data="wm"),
    ],
    [InlineKeyboardButton("Audio", callback_data="audio")],
]


# Running bot
xbot = Client('TikTokDL',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN)

# Helpers
# Thanks to FridayUB
async def run_cmd(cmd: str) -> Tuple[str, str, int, int]:
  args = shlex.split(cmd)
  process = await asyncio.create_subprocess_exec(
      *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
  )
  stdout, stderr = await process.communicate()
  return (
      stdout.decode("utf-8", "replace").strip(),
      stderr.decode("utf-8", "replace").strip(),
      process.returncode,
      process.pid,
  )

# Start
@xbot.on_message(filters.command('start') & filters.private)
async def _start(bot, update):
  await update.reply_text(f"I'm TikTokDL!\nYou can download tiktok url video/audio using this bot", True, reply_markup=InlineKeyboardMarkup(START_BUTTONS))

# Downloader for tiktok
@xbot.on_message(filters.regex(pattern='.*http.*') & filters.private)
async def _tiktok(bot, update):
  url = update.text
  session = requests.Session()
  resp = session.head(url, allow_redirects=True)
  if not 'tiktok.com' in resp.url:
    return
  await update.reply('Select the options below', True, reply_markup=InlineKeyboardMarkup(DL_BUTTONS))

# Callbacks
@xbot.on_callback_query()
async def _callbacks(bot, cb: CallbackQuery):
  if cb.data == 'nowm':
    dirs = downloads.format(uuid.uuid4().hex)
    os.makedirs(dirs)
    cbb = cb
    update = cbb.message.reply_to_message
    await cb.message.delete()
    url = update.text
    session = requests.Session()
    resp = session.head(url, allow_redirects=True)
    if '?' in resp.url:
      tt = resp.url.split('?', 1)[0]
    else:
      tt = resp.url
    ttid = dirs+tt.split('/')[-1]
    r = requests.get('https://api.reiyuura.me/api/dl/tiktok?url='+tt)
    result = r.text
    rs = json.loads(result)
    link = rs['result']['nowm']
    resp = session.head(link, allow_redirects=True)
    r = requests.get(resp.url, allow_redirects=True)
    open(f'{ttid}.mp4', 'wb').write(r.content)
    await bot.send_video(update.chat.id, f'{ttid}.mp4',)
    shutil.rmtree(dirs)
  elif cb.data == 'wm':
    dirs = downloads.format(uuid.uuid4().hex)
    os.makedirs(dirs)
    cbb = cb
    update = cbb.message.reply_to_message
    await cb.message.delete()
    url = update.text
    session = requests.Session()
    resp = session.head(url, allow_redirects=True)
    if '?' in resp.url:
      tt = resp.url.split('?', 1)[0]
    else:
      tt = resp.url
    ttid = dirs+tt.split('/')[-1]
    r = requests.get('https://api.reiyuura.me/api/dl/tiktok?url='+tt)
    result = r.text
    rs = json.loads(result)
    link = rs['result']['wm']
    resp = session.head(link, allow_redirects=True)
    r = requests.get(resp.url, allow_redirects=True)
    open(f'{ttid}.mp4', 'wb').write(r.content)
    await bot.send_video(update.chat.id, f'{ttid}.mp4',)
    shutil.rmtree(dirs)
  elif cb.data == 'audio':
    dirs = downloads.format(uuid.uuid4().hex)
    os.makedirs(dirs)
    cbb = cb
    update = cbb.message.reply_to_message
    await cb.message.delete()
    url = update.text
    session = requests.Session()
    resp = session.head(url, allow_redirects=True)
    if '?' in resp.url:
      tt = resp.url.split('?', 1)[0]
    else:
      tt = resp.url
    ttid = dirs+tt.split('/')[-1]
    r = requests.get('https://api.reiyuura.me/api/dl/tiktok?url='+tt)
    result = r.text
    rs = json.loads(result)
    link = rs['result']['wm']
    resp = session.head(link, allow_redirects=True)
    r = requests.get(resp.url, allow_redirects=True)
    open(f'{ttid}.mp4', 'wb').write(r.content)
    cmd = f'ffmpeg -i "{ttid}.mp4" -vn -ar 44100 -ac 2 -ab 192 -f mp3 "{ttid}.mp3"'
    await run_cmd(cmd)
    await bot.send_audio(update.chat.id, f'{ttid}.mp3',)
    shutil.rmtree(dirs)

xbot.run()
