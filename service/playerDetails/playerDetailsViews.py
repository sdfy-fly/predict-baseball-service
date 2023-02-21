from rest_framework.views import APIView
from rest_framework.response import Response
from asgiref.sync import async_to_sync

from .getPlayersDetail import MBADetail, NbaDetail

class PlayersDetail(APIView):

    def post(self, request):
        
        sport = request.data['sport']

        data = self.getPlayersDetail(sport)

        if data:
            return Response(data)

        return Response(status=500)

    @async_to_sync
    async def getPlayersDetail(self,sport:str):

        if sport.lower() == 'mba' :
            gpd = MBADetail()
 
        elif sport.lower() == 'nba' :
            gpd = NbaDetail()

        try:
            data = await gpd.getData()
            return data
        except:
            return None