import aiohttp
from bs4 import BeautifulSoup

auth = {'username': 'Keysik', 'password': 'Fantasymlb'}


async def get_schedule():
    url = 'https://www.rotowire.com/baseball/projected-starters.php'
    res = []

    async with aiohttp.ClientSession() as session:

        async def auth_(session: aiohttp.ClientSession, auth):
            async with session.post('https://www.rotowire.com/users/login.php', data=auth) as r:
                await r.text()

        async def getData(session: aiohttp.ClientSession, url):
            async with session.get(url=url) as response:
                soup = BeautifulSoup(await response.text(), 'lxml')
                schedule = soup.find('div', class_=['starters-matrix', 'mb-10'])
                table_lines = schedule.findAll('div', class_=['flex-row', 'myleagues__proteam'])
                for line in table_lines:
                    team_logo = line.findNext(name='img')
                    logo = team_logo.get('src').strip()
                    team = team_logo.get('alt').strip()
                    team_columns = line.findAll(class_='starters-matrix__item')
                    columns = []
                    for column in team_columns:
                        content = column.findAll(name='div')
                        if len(content) == 3:
                            columns.append({
                                'name': content[0].text.strip(),
                                'stats': content[1].text.strip(),
                                'time': content[2].text.replace('@', 'vs').strip()
                            })
                        else:
                            columns.append('-')
                    res.append({
                        'team': team,
                        'logo': logo,
                        'columns': columns
                    })

                return res

        await auth_(session, auth)
        await getData(session, url)

        return res[1:]


async def get_injury_news(date, sport: str):
    """ принимаю дату в формате 2022-10-18"""

    if sport.lower() == 'mba':
        url = f"https://www.rotowire.com/baseball/ajax/get-more-updates.php?type=custom&itemID=custom&lastUpdateTime={date}%2008%3A39%3A56.117&numUpdates=25&view=all"
    elif sport.lower() == 'nba':
        url = f"https://www.rotowire.com/basketball/ajax/get-more-updates.php?type=custom&itemID=custom&lastUpdateTime={date}%2008%3A39%3A56.117&numUpdates=25&view=all"

    async with aiohttp.ClientSession() as session:

        async with session.post('https://www.rotowire.com/users/login.php', data=auth) as r:
            await r.text()

        async with session.post(url=url) as response:
            res = []
            data = await response.json()
            soup = BeautifulSoup(data['updatesHTML'], 'lxml')
            injures = soup.find_all(class_='news-update')
            for injure in injures:
                logo = injure.find(class_='news-update__logo')
                img = logo.get('src')
                team_name = logo.get('alt')
                name = injure.find(
                    class_='news-update__player-link').text.strip()
                short_news = injure.find(
                    class_='news-update__headline').text.strip()
                date = injure.find(
                    class_='news-update__timestamp').text.strip()
                news = injure.find(class_='news-update__news').text.strip()
                analyst = injure.find(
                    class_='news-update__analysis').text.strip()
                analyst = analyst.replace('ANALYSIS', '').strip()
                res.append({
                    "id": f'{name}_{short_news}_{date}',
                    "logo": img,
                    "team": team_name,
                    "playerName": name,
                    "shortNews": short_news,
                    "date": date,
                    "text": news,
                    "analysisText": analyst,
                })
            return res
