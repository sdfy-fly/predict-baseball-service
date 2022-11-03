import aiohttp
from bs4 import BeautifulSoup


async def getSchedule():
    url = 'https://www.rotowire.com/baseball/projected-starters.php'
    auth = {'username': 'Keysik', 'password': 'Fantasymlb'}
    data = {'data': ""}
    async with aiohttp.ClientSession() as session:
        async def auth_(session: aiohttp.ClientSession, auth):
            async with session.post('https://www.rotowire.com/users/login.php', data=auth) as r:
                await r.text()

        async def getData(session: aiohttp.ClientSession, url):
            async with session.get(url=url) as response:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                data["data"] = soup.find(class_='starters-matrix mb-10')
                return data

        await auth_(session, auth)
        await getData(session, url)

        return data


async def getInjuryNews(date):
    """ принимаю дату в формате 2022-10-18"""

    url = f"https://www.rotowire.com/baseball/ajax/get-more-updates.php?type=custom&itemID=custom&lastUpdateTime={date}%2008%3A39%3A56.117&numUpdates=25&injuries=all"

    async with aiohttp.ClientSession() as session:
        async with session.post(url=url) as response:
            res = []
            data = await response.json()
            soup = BeautifulSoup(data['updatesHTML'], 'lxml')
            injures = soup.find_all(class_='news-update')
            for injure in injures:
                logo = injure.find(class_='news-update__logo')
                img = logo.get('src')
                team_name = logo.get('alt')
                name = injure.find(class_='news-update__player-link').text.strip()
                short_news = injure.find(class_='news-update__headline').text.strip()
                date = injure.find(class_='news-update__timestamp').text.strip()
                news = injure.find(class_='news-update__news').text.strip()
                analyst = injure.find(class_='news-update__analysis').text.strip()
                analyst = analyst.replace('ANALYSIS', '').strip()
                res.append({
                    "id": f'{name} {short_news} {date}',
                    "logo": img,
                    "team": team_name,
                    "playerName": name,
                    "shortNews": short_news,
                    "date": date,
                    "text": news,
                    "analysisText": analyst,
                })
            return res
