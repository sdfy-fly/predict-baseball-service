from rest_framework.views import APIView
from rest_framework.response import Response

from datetime import timedelta

from .paymentUrl import createPaymentUrl
from service.models import Users

from asgiref.sync import async_to_sync , sync_to_async

class CreatePaymentUrl(APIView):

    """
        Принимаю userId пользователя, сумму к оплате и срок продления
        Создаю платеж и возвращаю ссылку для оплаты
    """

    def post(self,request):
        
        userID = request.data['userID']
        amount = request.data['amount']
        subscriptionRange = request.data['subscriptionRange']

        order_id = f"{userID};{subscriptionRange}"

        paymentUrl = self.getPaymentUrl(order_id, amount)

        if paymentUrl:
            return Response(paymentUrl)
        else:
            return Response(status=500)

    @async_to_sync
    async def getPaymentUrl(self, order_id, amount):
        
        try: 
            return await createPaymentUrl(order_id=order_id, amount=amount)
        except Exception as _ex:
            print(_ex)
            return None


class PaymentHandler(APIView):
    
    def post(self, request):
        
        status = request.data['status']

        if status == 'success':

            userID , subscritionRange = request.data['order_id'].split(';')
    
            self.updateSubscrition(userID , subscritionRange)
            
        return Response(status=200)
    

    @async_to_sync
    async def updateSubscrition(self, userID,subscritionRange):

        user = await Users.objects.aget(user_id = userID)
        date = user.subscription_date + timedelta(weeks=4 * int(subscritionRange))
        user.subscription_date = date

        await sync_to_async(user.save)()


