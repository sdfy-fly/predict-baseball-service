from rest_framework.views import APIView
from rest_framework.response import Response
from asgiref.sync import async_to_sync

from .players_detail import MbaPlayersDetail, NbaPlayersDetail
from .get_schedule import get_schedule, get_injury_news


class PlayersDetail(APIView):

    def post(self, request):
        sport = request.data['sport']
        data = self.get_players_detail(sport)

        if not data:
            return Response(status=401)
        return Response(data)

    @async_to_sync
    async def get_players_detail(self, sport: str):

        if sport.lower() == 'mba':
            gpd = MbaPlayersDetail()

        elif sport.lower() == 'nba':
            gpd = NbaPlayersDetail()

        try:
            return await gpd.getData()
        except Exception as _ex:
            print(_ex)
            return None


class GetSchedule(APIView):

    def post(self, request):
        data = self.getData()

        if not data:
            return Response(status=401)
        return Response(data)

    @async_to_sync
    async def getData(self):
        return await get_schedule()


class GetInjuryNews(APIView):

    def post(self, request):
        data = self.getData(request.data['date'], request.data['sport'])
        if not data:
            return Response(status=401)
        return Response(data)

    @async_to_sync
    async def getData(self, date, sport):
        return await get_injury_news(date, sport)
