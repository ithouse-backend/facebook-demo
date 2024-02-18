from django.db import models
from django.utils import timezone
from datetime import timedelta

from apps.authentication.models import User


class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='story/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Story'
        verbose_name_plural = "Stories"

    def __str__(self):
        return "%s %s posted story at %s" % (self.user.firstname, self.user.lastname, str(self.created_at))

    def is_expired(self):
        """
        Har bir joylangan storyni shu funksiya orqali, joylaniga 24 soat bo'ldimi yoki yo'q
        bunda faqat True, False qiymat qaytaradi
        now -- joriy vaqtni olish
        expiration_time = tugash vaqti bunda story yaratilgan vaqt + 24 soat qo'shilmoqda
        agar now(joriy vaqt) katta bo'lib ketsa tugash vaqtidan bizga True yoki False qaytaradi agar tugamagan bo'lsa
        """
        now = timezone.now()
        expiration_time = self.created_at + timedelta(hours=24)
        return now >= expiration_time

    @classmethod
    def delete_expired_stories(cls):
        """
        bu funksiya auto storyni o'chirib yuborish uchun
        Bu yerda @classmethod -- to'gridan to'gri class bilan ishlash uchun ishlatiladi
        cls -- bu Story modeli
        created_at__lte -- yaratilgan vaqt kichik yoki teng 24 soatga yani ayirib yubordim
        expired_stories.delete() -- filter qilingan modelni o'chirib yuboradi
        Lekin bu funksiyani chaqirib ishlatish kerak, yokida ishlamaydi
        """
        expired_stories = cls.objects.filter(
            created_at__lte=timezone.now() - timedelta(hours=24))
        expired_stories.delete()
