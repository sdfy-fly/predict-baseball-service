from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect

from asgiref.sync import sync_to_async, async_to_sync
import datetime

from .oauth_sorare import AuthWithSorare
from .sorare_user_cards import MBACards, NBACards
from .models import Users


class Auth(APIView):
    """
        В Post запросе принимаю email и password
        Возвращаю userInfo со всеми данными о юзере(Jwt, userId , nickname и тд)
    """

    def get(self, request):
        code = self.request.query_params.get('code', None)

        if not code:
            return redirect('http://sorareup.com')

        return redirect(f'http://sorareup.com?code={code}')


class GetUserInfo(APIView):
    """
        OAuth2 через Sorare, если пользователь первый раз авторизовывается,
        то он заносится в базу и получется подписку на 20 недель
    """

    def post(self, request):

        code = request.data.get('code')
        userInfo: dict = self._auth(code)

        if not userInfo:
            return Response(status=403)

        return Response(userInfo)

    @async_to_sync
    async def _auth(self, code):
        try:

            userInfo = await AuthWithSorare().getUserInfo(code)

            user, status = await Users.objects.aget_or_create(
                nickname=userInfo['nickname'],
                user_id=userInfo['userID'],
                defaults={'last_visit': datetime.datetime.now()}
            )

            if not status:
                userInfo["subscription_date"] = user.subscription_date
                await sync_to_async(user.save)()
            else:
                userInfo["subscription_date"] = datetime.datetime.today() + datetime.timedelta(weeks=4 * 5)

        except Exception as _ex:
            print(_ex)
            return None

        return {'userInfo': userInfo}


class GetUpdatedUserData(APIView):

    def post(self, request):
        user_id = request.data['userID']
        userInfo = self.get_user_data(user_id)
        return Response(userInfo)

    @async_to_sync
    async def get_user_data(self, user_id):
        user = await Users.objects.aget(user_id=user_id)
        userInfo = {
            'nickname': user.nickname,
            'created_at': user.created_at,
            'subscription_date': user.subscription_date
        }
        return {'userInfo': userInfo}


class UserCards(APIView):

    def post(self, request):
        x_algolia_api_key = request.data['x-algolia-api-key']
        x_algolia_application_id = request.data['x-algolia-application-id']
        userID = request.data['userID']
        sport = request.data['sport']

        cards = self.get_user_cards(sport, x_algolia_api_key, x_algolia_application_id, userID)
        return Response(cards)

    @async_to_sync
    async def get_user_cards(self, sport: str, x_algolia_api_key: str, x_algolia_application_id: str, userID: str):

        cards = None
        if sport.lower() == 'mba':
            cards = await MBACards(x_algolia_api_key, x_algolia_application_id, userID).getCards()
        if sport.lower() == 'nba':
            cards = await NBACards(x_algolia_api_key, x_algolia_application_id, userID).getCards()

        return cards
