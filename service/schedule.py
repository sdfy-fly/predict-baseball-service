import aiohttp
from bs4 import BeautifulSoup

async def getSchedule():
    
    url = 'https://www.rotowire.com/baseball/projected-starters.php'
    auth = {'username' : 'Keysik' , 'password' : 'Fantasymlb' }
    data = {'data' : ""}
    async with aiohttp.ClientSession() as session:

        async def auth_(session:aiohttp.ClientSession , auth):

            async with session.post('https://www.rotowire.com/users/login.php', data = auth) as r : 
                
                await r.text()

        async def getData(session:aiohttp.ClientSession , url):

            async with session.get(url=url) as response : 

                soup = BeautifulSoup(await response.text() , 'html.parser')
                data["data"] = soup.find(class_='starters-matrix mb-10')
                return data
                
        await auth_(session,auth)
        await getData(session,url) 

        return data


async def getInjuryNews(date):

    """ принимаю дату в формате 2022-10-18"""

    url = f"https://www.rotowire.com/baseball/ajax/get-more-updates.php?type=custom&itemID=custom&lastUpdateTime={date}%2008%3A39%3A56.117&numUpdates=25&injuries=all" 

    async with aiohttp.ClientSession() as session : 
        async with session.post(url=url) as response :  
 
            data = await response.json()  
            return data 
