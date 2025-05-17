import requests
import asyncio
import aiohttp
import time



f = open("/Users/rdgarg1/Downloads/UrlShortener/resources/longurls.txt", "r")

to_hit = "https://api.my-short-url.com/shorten_url?url="

request_list = []


def make_all_urls():
    for url in f:
        p = url.rstrip()
        print(p)
        x = to_hit + p
        request_list.append(x)
        # response = requests.get(x)
        # print(response.text)




async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def make_requests():
    # make_all_urls()
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in request_list]
        start_time = time.time()
        await asyncio.gather(*tasks)
        end_time = time.time()
        duration = end_time - start_time
        print(f"Time taken for {len(request_list)} requests: {duration:.2f} seconds")
        print(f"Requests per second: {len(request_list) / duration:.2f}")

if __name__ == "__main__":
    make_all_urls()
    url = "your_target_url"  # Replace with the actual URL
    num_requests = 100
    asyncio.run(make_requests())