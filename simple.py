import asyncio
import aiohttp #pip install aiohttp


TOKEN = 'your TOKEN here'

URL = f'https://api.telegram.org/bot{TOKEN}/'


async def send_message(chat_id, text):
    async with aiohttp.ClientSession() as session:
        params = {'chat_id': chat_id, 'text': text}
        async with session.post(URL + 'sendMessage', data=params) as response:
            await response.json()


async def handle_updates(update):
    message = update.get('message', False)
    if message:
        chat_id = message['chat']['id']
        text = message.get('text', False)
        if text:
            await send_message(chat_id, f'Эхо: {text}')
        else:
            await send_message(chat_id, 'Я работаю только с текстом')


async def get_updates():
    offset = None
    async with aiohttp.ClientSession() as session:
        while True:
            params = {'timeout': 10, 'offset': offset}
            async with session.post(URL + 'getUpdates', data=params) as response:
                updates = await response.json()
                if len(updates['result']) > 0:
                    offset = updates['result'][-1]['update_id'] + 1
                    for update in updates['result']:
                        await handle_updates(update)
                        #посмотреть содержимое обновления
                        print(update)

                        
async def main():
    await get_updates()


asyncio.run(main())
