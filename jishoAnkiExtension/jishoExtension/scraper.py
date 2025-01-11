# Saturday May 26, 2024
# Jisho Scraper
# Taha Rashid

# async based on: https://stackoverflow.com/questions/35926917/asyncio-web-scraping-101-fetching-multiple-urls-with-aiohttp

# imports
import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def scrape(headers, search):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url=('https://jisho.org/search/' + search)) as response:
            # grab the webpage
            html = await response.text()

            # parse through the webpage
            soup = BeautifulSoup(html, "html.parser")
            meanings = soup.find_all("div", class_="meaning-tags")

            # printing the answer from our first/top search result
            meaning = meanings[0]
            ans = ""

            # transivity
            if meaning.text.find("Intransitive verb") != -1:
                ans += "Self-Move, "
            if meaning.text.find("Transitive verb") != -1:
                ans += "Other-Move, "

            # return answer
            return ans.rstrip(", ")


async def scrape_all(headers, searches):
    results = await asyncio.gather(
        *[scrape(headers, search) for search in searches],
        return_exceptions=True
    )

    return results


def run(headers, searches):
    # run scraper and get returned results
    saved_searches = list(asyncio.run(scrape_all(headers, searches)))
    return saved_searches


# test run everything
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}
searches = [
    "開く ひらく",
    # add all of your searches
]

scraped = run(headers, searches)
#print(len(scraped))
