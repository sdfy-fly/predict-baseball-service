from django.db import models
from datetime import datetime, timedelta


class Users(models.Model):
    nickname = models.CharField(max_length=150, verbose_name='Никнейм')
    user_id = models.CharField(max_length=150, verbose_name='User ID')
    subscription_date = models.DateField(verbose_name='Срок активной подписки',
                                         default=datetime.today() + timedelta(weeks=4 * 5))
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Общая сумма', default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    last_visit = models.DateTimeField(auto_now=True, verbose_name='Был онлайн')

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']
