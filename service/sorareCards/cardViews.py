from rest_framework.views import APIView
from rest_framework.response import Response

from .sorareCards import MBACards, NBACards

from asgiref.sync import async_to_sync

class UserCards(APIView):

    def post(self, request):
        x_algolia_api_key = request.data['x-algolia-api-key']
        x_algolia_application_id = request.data['x-algolia-application-id']
        userID = request.data['userID']
        sport = request.data['sport']

        cards = self.getCards(sport,x_algolia_api_key, x_algolia_application_id, userID)
        return Response(cards)

    @async_to_sync
    async def getCards(self,sport:str,x_algolia_api_key, x_algolia_application_id, userID):

        cards = None
        if sport.lower() == 'mba' :
            cards = await MBACards().getCards(x_algolia_api_key, x_algolia_application_id, userID)

        if sport.lower() == 'nba' :
            cards = await NBACards().getCards(x_algolia_api_key, x_algolia_application_id, userID)
        return cards