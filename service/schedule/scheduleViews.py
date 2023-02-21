from rest_framework.views import APIView
from rest_framework.response import Response
from asgiref.sync import async_to_sync

from .getSchedule import *

class GetSchesule(APIView):

    def post(self, request):
        data = self.getData()
        return Response(data)

    @async_to_sync
    async def getData(self):
        return await getSchedule()


class GetInjuryNews(APIView):

    def post(self, request):
        data = self.getData(request.data['date'],request.data['sport'])
        if data:
            return Response(data)
        else:
            return Response(status=500)

    @async_to_sync
    async def getData(self, date,sport):

        try:
            return await getInjuryNews(date,sport)
        except:
            return None