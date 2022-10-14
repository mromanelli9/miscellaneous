import asyncio
import logging

import aiohttp
from aiolimiter import AsyncLimiter

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def download(url: str, semaphore, limiter, timeout) -> bytes:
    content: bytes = b""

    async with aiohttp.ClientSession() as session:
        await semaphore.acquire()
        async with limiter:
            logger.info(f"Begin downloading {url}")

            try:
                async with session.get(url, timeout=timeout) as resp:
                    content = await resp.read()
                    logger.info(f"Finished downloading {url}")
            except aiohttp.ClientError as err:
                logger.error(err)
            except asyncio.exceptions.TimeoutError:
                logger.warning(f"Hit timeout limit for {url}")
            else:
                if resp.status < 400:
                    logger.info(f"Finished downloading {url}")
                else:
                    logger.warning(f"Server responded with {resp.status} for {url}")
                    content = b""
            finally:
                semaphore.release()

            return content


async def write_to_file(filename: str, content: bytes) -> None:
    with open(filename, "wb") as outfile:
        outfile.write(content)
        logger.info(f"Finished writing {filename}")


async def web_scrape_task(
    output_filename: str, url: str, semaphore, limiter, timeout
) -> None:
    content = await download(url, semaphore, limiter, timeout)
    if content:
        await write_to_file(output_filename, content)


async def downloader(
    urls_filename="urls.txt",
    output_folder="htmls",
    connection_timeout=5,  # seconds
    max_active_requests=10,
    max_req_sec=0.125,  # 8 requests/sec
) -> None:
    # Load urls from file
    with open(urls_filename, "r", encoding="utf-8") as infile:
        urls = infile.readlines()
    logger.info(f"Found {len(urls)} urls")

    limiter = AsyncLimiter(1, max_req_sec)
    semaphore = asyncio.Semaphore(value=max_active_requests)
    timeout = aiohttp.ClientTimeout(total=connection_timeout)
    tasks = []
    for index, url in enumerate(urls):
        output_filename = f"{output_folder}/{index}.txt"
        tasks.append(
            asyncio.create_task(
                web_scrape_task(output_filename, url, semaphore, limiter, timeout)
            )
        )

    await asyncio.wait(tasks)


if __name__ == "__main__":
    asyncio.run(downloader())
