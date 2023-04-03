from rest_framework.views import APIView
from rest_framework.response import Response
from asgiref.sync import async_to_sync
from django.core.cache import cache

from .players_detail import MbaPlayersDetail, NbaPlayersDetail
from .get_schedule import get_schedule, get_injury_news

import json
from datetime import timedelta


class RedisClient:

    @staticmethod
    def get_redis_data(redis_key_name):
        """
            Принимаю ключ, и возвращаю десериализованные из строки данные
        """
        data = cache.get(redis_key_name)
        if data:
            return json.loads(data)
        return None

    @staticmethod
    def set_redis_data(redis_key_name, data, expire=None):
        """
            Принимаю ключ, данные и срок жизни
            Сериализую данные и записывыю в redis
        """
        data = json.dumps(data)
        cache.set(redis_key_name, data, expire)


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

        schedule_key = "schedule"
        if RedisClient.get_redis_data(schedule_key):
            data = RedisClient.get_redis_data(schedule_key)
            return Response(data)

        data = self.get_data()
        if data:
            RedisClient.set_redis_data(schedule_key, data, timedelta(days=1).total_seconds())
            return Response(data)

        return Response(status=401)

    @async_to_sync
    async def get_data(self):
        return await get_schedule()


class GetInjuryNews(APIView):

    def post(self, request):
        data = self.get_data(request.data['date'], request.data['sport'])
        if not data:
            return Response(status=401)
        return Response(data)

    @async_to_sync
    async def get_data(self, date, sport):
        return await get_injury_news(date, sport)
