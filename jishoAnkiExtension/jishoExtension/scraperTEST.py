import asyncio
import aiohttp
from bs4 import BeautifulSoup

saved = []

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def scrape(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, ("https://jisho.org/search/" + url))
        soup = BeautifulSoup(html, 'html.parser')
        # Your scraping logic here
        meanings = soup.find_all("div", class_="meaning-tags")

        # printing the answer from our first/top search result
        meaning = meanings[0]
        #print(meaning)
        ans = ""

        # transivity
        if meaning.text.find("Intransitive verb") != -1:
            ans += "Self-Move, "
        if meaning.text.find("Transitive verb") != -1:
            ans += "Other-Move, "

        temp = ans.rstrip(", ")
        #print(temp)
        saved.append(temp)


async def main(urls):
    # List of URLs to scrape
    # urls = [
    #     '開く ひらく',
    #     '盗む ぬすむ'
    #     '気づく きずく'
    #     # Add more URLs as needed
    # ]

    # Gather all tasks concurrently
    tasks = [scrape(url) for url in urls]
    #print(saved)
    await asyncio.gather(*tasks)


# Run the event loop
if __name__ == "__main__":
    asyncio.run(main())
    print(saved)
