import aiohttp
from bs4 import BeautifulSoup


async def getSchedule():
    
    url = 'https://www.rotowire.com/baseball/projected-starters.php'
    auth = {'username' : 'Keysik' , 'password' : 'Fantasymlb' }
    async with aiohttp.ClientSession() as session:

        async with session.post('https://www.rotowire.com/users/login.php', data = auth) as r : 
            
            await r.text()

            async with session.get(url=url, data = auth) as response : 

                soup = BeautifulSoup(await response.text() , 'html.parser')
                data = soup.find(class_='starters-matrix mb-10')
                return {'data' : data}
