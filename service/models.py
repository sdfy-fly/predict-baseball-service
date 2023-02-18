from django.db import models

# Create your models here.
class Users(models.Model):
    # ник, user id, сколько потрачено , срок подписки, последняя активность
      
    nickname = models.CharField(max_length=150, verbose_name='Никнейм')
    user_id = models.CharField(max_length=150, verbose_name='User ID')
    subscription_date = models.DateField(verbose_name='Срок активной подписки')
    total_amount = models.DecimalField(max_digits=8 , decimal_places=2,verbose_name='Общая сумма')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Дата регистрации')
    last_visit = models.DateTimeField(verbose_name='Был онлайн')


    def __str__(self) -> str:
        return self.nickname

    class Meta() :
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']