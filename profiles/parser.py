import time
import asyncio
import aiohttp

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/126.0.0.0 Safari/537.36'
}
def total_async_timer(func):
    async def wrapper(*args):
        start_time = time.time()
        await func(*args)
        print(f'time: {time.time() - start_time}')

    return wrapper


async def async_get_json_data(session, url, result_list):
    async with session.get(url=url, headers=headers) as resp:
        resp_url = await resp.json()
        result_list.append(resp_url['url'])



async def get_tasks(base_url, count):
    async with aiohttp.ClientSession() as session:
        tasks = []
        result_list = []
        for i in range(count):
            task = asyncio.create_task(
                async_get_json_data(session, f'{base_url}{i}', result_list))
            tasks.append(task)
        await asyncio.gather(*tasks)
        return result_list
