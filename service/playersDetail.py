import asyncio
from datetime import date , timedelta
import aiohttp

def weekDay(year, month, day):
        offset = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
        week   = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',  'Friday', 'Saturday']
        afterFeb = 1
        if month > 2: 
            afterFeb = 0
        aux = year - 1700 - afterFeb
    
        dayOfWeek  = 5

        dayOfWeek += (aux + afterFeb) * 365                  
            
        dayOfWeek += aux // 4 - aux // 100 + (aux + 100) // 400     
        
        dayOfWeek += offset[month - 1] + (day - 1)               
        dayOfWeek %= 7

        return dayOfWeek, week[dayOfWeek]

AUTH = {'username' : 'Keysik' , 'password' : 'Fantasymlb' }


class MBADetail():

    players = {}

    async def get_data(self,session: aiohttp.ClientSession , url , index,d:str):

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

            currentDate = weekDay(*list(map(int,d.split('-'))))
            daily_object = {"match" : True,'dailySum' : daily_sum , 'numWeek': currentDate[0] , 'week' : currentDate[1], 'date' : d}

            if self.players.get(player["player"]) : 

                self.players[player["player"]]['sum'][index] = daily_object

            else :
                self.players[player["player"]] = {
                    'name' : player["player"] ,
                    'position' : player["position"] , 
                    'team' : player["team"] , 
                    'sum' : [daily_object,{"match" : False},{"match" : False},{"match" : False},{"match" : False},{"match" : False},{"match" : False}]
                }


    async def get_pages(self) : 
        # dates = []

        tasks = []
        async with aiohttp.ClientSession() as session:
            async with session.post('https://www.rotowire.com/users/login.php', data = AUTH) as r : 

                await r.text()
                # dates = ['2022-06-01','2022-06-02','2022-06-03','2022-06-04','2022-06-05','2022-06-06','2022-06-07']
                for index in range(7): 

                    d = str(date.today() + timedelta(days=index))
                    # d = dates[index]
                    # dates.append(d)
                    url = f'https://www.rotowire.com/baseball/tables/daily-projections.php?pos=ALL&start={d}'
                    
                    tasks.append(self.get_data(session , url , index,d))

            await asyncio.gather(*tasks)

    async def getData(self) : 
        await self.get_pages()
        return self.players


class NbaDetail():

    players = {}

    async def get_data(self,session: aiohttp.ClientSession , url , index,d:str):

        data = await (await session.get(url=url)).json() 

        for player in data : 

            values_from_site = [player['PTS'] , player['REB'] , player['AST'] , player['STL'] , player['BLK'] , player['BLK'] , player['THREEPM'] , player['TO']]
            values_from_site = [round(float(value),1) for value in values_from_site]       
            values_from_img = [1,1.2,1.5,3,2,1,-2]

            values_multiply = [values_from_site[i] * values_from_img[i] for i in range(7)]
            daily_sum = round(sum(values_multiply),1)

            currentDate = weekDay(*list(map(int,d.split('-'))))
            daily_object = {"match" : True,'dailySum' : daily_sum , 'numWeek': currentDate[0] , 'week' : currentDate[1], 'date' : d}

            if self.players.get(player["player"]) : 
                
                self.players[player["player"]]['sum'][index] = daily_object

            else :
                self.players[player["player"]] = {
                    'name' : player["player"] ,
                    'position' : player["pos"] , 
                    'team' : player["team"] , 
                    'sum' : [daily_object,{"match" : False},{"match" : False},{"match" : False},{"match" : False},{"match" : False},{"match" : False}]
                }

    async def get_pages(self) : 
        tasks = []
        async with aiohttp.ClientSession() as session:
            async with session.post('https://www.rotowire.com/users/login.php', data = AUTH) as r : 

                await r.text()

                for index in range(7): 

                    d = str(date.today() + timedelta(days=index))
                    url = f'https://www.rotowire.com/basketball/tables/projections.php?type=daily&pos=ALL&date={d}'
                    
                    tasks.append(self.get_data(session , url , index,d))  

            await asyncio.gather(*tasks)

    async def getData(self) : 
        await self.get_pages()
        return self.players