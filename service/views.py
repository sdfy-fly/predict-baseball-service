import datetime

from django.shortcuts import render, redirect

from service.payment.paymentViews import CreatePaymentUrl, PaymentHandler
from service.sorareCards.cardViews import UserCards
from service.schedule.scheduleViews import GetSchesule , GetInjuryNews
from service.playerDetails.playerDetailsViews import PlayersDetail

from .auth_sorare import AuthWithSorare

from .models import Users
from asgiref.sync import sync_to_async, async_to_sync

from rest_framework.views import APIView
from rest_framework.response import Response


async def index(request):
    return render(request, 'service/index.html')


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

    def post(self, request):

        code = request.data.get('code')   
        userInfo : dict = self._auth(code)

        if not userInfo : 
            return Response(status=403)

        return Response(userInfo)

    @async_to_sync
    async def _auth(self, code):
        try:

            # Получение userInfo, добавление в базу пользователя, и если он новый юзер то выдаю подписку на 5 месяцев

            userInfo = await AuthWithSorare().getUserInfo(code)

            user, status = await Users.objects.aget_or_create(
                nickname = userInfo['nickname'] , 
                user_id = userInfo['userID'] , 
                defaults={'last_visit':datetime.datetime.now()}
            )
            if (not status):
                userInfo["subscription_date"] = user.subscription_date
                await sync_to_async(user.save)()
            else : 
                userInfo["subscription_date"] = datetime.datetime.today() + datetime.timedelta(weeks=4*5)
            
        except:
            return None

        return {'userInfo': userInfo}
