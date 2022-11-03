from datetime import date , timedelta 
import aiohttp
import asyncio
import json

class NbaDetail():
    players = {}

    async def get_data(self,session: aiohttp.ClientSession , url , index):

        data = await (await session.get(url=url)).json() 

        for player in data : 

            values_from_site = [player['PTS'] , player['REB'] , player['AST'] , player['STL'] , player['BLK'] , player['BLK'] , player['THREEPM'] , player['TO']]
            values_from_site = [round(float(value),1) for value in values_from_site]       
            values_from_img = [1,1.2,1.5,3,2,1,-2]

            values_multiply = [values_from_site[i] * values_from_img[i] for i in range(7)]
            daily_sum = round(sum(values_multiply),1)


            if self.players.get(player["player"]) : 

                self.players[player["player"]]['sum'][index] = daily_sum

            else : 

                self.players[player["player"]] = {
                    'name' : player["player"] ,
                    'position' : player["pos"] , 
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

                    d = date.today() + timedelta(days=index)
                    dates.append(str(d))
                    url = f'https://www.rotowire.com/basketball/tables/projections.php?type=daily&pos=ALL&date={d}'
                    
                    tasks.append(self.get_data(session , url , index))  

            await asyncio.gather(*tasks)

    async def getInfo(self) : 

        await self.get_pages()
        return self.players


async def main():
    nbaData = NbaDetail()
    data = await nbaData.getInfo()

    with open('2.json' , 'w') as file : 
        json.dump(data , file , indent=4 , ensure_ascii=False)

# asyncio.get_event_loop().run_until_complete(main())
