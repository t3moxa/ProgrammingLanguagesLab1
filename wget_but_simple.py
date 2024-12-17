import aiohttp
import asyncio
import urllib.parse
import os

async def download_file(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                global downloaded_size
                downloaded_size = 0

                global elapsed_time
                elapsed_time = 0

                path = urllib.parse.urlparse(url).path
                filename = os.path.split(path)[1]
                path_and_filename = os.getcwd()+"\\" + filename

                with open(path_and_filename, 'wb') as file:
                    timer_task = asyncio.create_task(display_progress())

                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        file.write(chunk)
                        downloaded_size += len(chunk)

                    timer_task.cancel()

                    try:
                        await timer_task
                    except asyncio.CancelledError:
                        print("Скачивание файла завершено!")
            else:
                print(f"Ошибка при скачивании файла: {response.status} {response.reason}")

async def display_progress():
    while True:
        global elapsed_time
        global downloaded_size
        elapsedTime += 1
        print(f"\rСкачано: {downloaded_size} байт, секунд прошло {elapsed_time}.")
        await asyncio.sleep(1)

async def main():
    url = input("Введите URL файла для скачивания: ")
    await download_file(url)

if __name__ == "__main__":
    asyncio.run(main())
