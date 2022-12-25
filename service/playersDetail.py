import asyncio
from datetime import date , timedelta
import aiohttp

class GetPlayersDetail():
    players = {}

    async def get_data(self,session: aiohttp.ClientSession , url , index):

        daily_data = await (await session.get(url=url)).json() 

        for player in daily_data : 

            if player.get('ip') : 

                # случай когда player == picher
                values_from_site = [player.get('ip') , player.get('pk') , player.get('phits') , player.get('er') , player.get('pbb') , player.get('w') , player.get('sv') , player.get('hld') ]
                values_from_site = [round(float(value),1) for value in values_from_site]       
                values_from_img = [3,2,-0.5,-2,-1,5,10,5]

            else : 
                # случай когда player == batler
                values_from_site = [player.get('r') , player.get('rbi') , player.get('singles') , player.get('doubles') , player.get('triples') , player.get('hr') , player.get('bb') , player.get('k'), player.get('sb')]
                values_from_site = [round(float(value),1) for value in values_from_site]       
                values_from_img = [3,3,2,5,8,10,2,-1,5]

            values_multiply = [values_from_site[i] * values_from_img[i] for i in range(len(values_from_img))]
            daily_sum = round(sum(values_multiply),1)


            if self.players.get(player["player"]) : 

                self.players[player["player"]]['sum'][index] = daily_sum
                
            else :

                self.players[player["player"]] = {
                    'name' : player["player"] ,
                    'position' : player["position"] , 
                    'team' : player["team"] , 
                    'sum' : [daily_sum,0,0,0,0,0,0]
                }



    async def get_pages(self) : 
        dates = []

        auth = {
            'username' : 'Keysik' , 
            'password' : 'Fantasymlb' 
        }
        tasks = []
        async with aiohttp.ClientSession() as session:
            async with session.post('https://www.rotowire.com/users/login.php', data = auth) as r : 

                await r.text()

                for index in range(7): 

                    # d = date.today() + timedelta(days=index)
                    d = '2022-07-01'
                    dates.append(str(d))
                    url = f'https://www.rotowire.com/baseball/tables/daily-projections.php?pos=ALL&start={d}'
                    
                    tasks.append(self.get_data(session , url , index))
                    #temp = '-'.join(d.split('-')[:-1]) + '0' + str(int(d.split('-')[-1]) + 1)

            await asyncio.gather(*tasks)

    async def getData(self) : 

        await self.get_pages()
        return self.players
