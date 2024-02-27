from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, AbstractUser
from django.core.validators import EmailValidator
from PIL import Image
import random

# django default login --> username, password
# django default register --> firstname, lastname, username, email, password


class CustomUser(BaseUserManager):
    def create_user(self, email, firstname, lastname, gender, birthday, password=None):
        if not email:
            raise ValueError("Iltimos email kiriting")
        if not password or len(password) < 4:
            raise ValueError(
                "Parol kiritishda hatolik yoki parolingiz 4ta harfdan kam")

        user = self.model(
            email=self.normalize_email(email),
            firstname=firstname,
            lastname=lastname,
            gender=gender,
            birthday=birthday,
            password=password,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstname, lastname, gender, birthday, password):
        if not email:
            raise ValueError("Iltimos email kiriting")
        if not password or len(password) < 4:
            raise ValueError(
                "Parol kiritishda hatolik yoki parolingiz 4ta harfdan kam")

        user = self.create_user(
            email=email,
            firstname=firstname,
            lastname=lastname,
            gender=gender,
            birthday=birthday,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    GENDER = [("Male", "Male"), ("Female", "Female")]
    unique_id = models.IntegerField(null=True, unique=True)
    firstname = models.CharField(max_length=100, db_index=True)
    lastname = models.CharField(max_length=100, db_index=True)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    birthday = models.DateField()
    gender = models.CharField(max_length=20, choices=GENDER)
    is_admin = models.BooleanField(default=False, null=True)
    is_active = models.BooleanField(default=True, null=True)
    objects = CustomUser()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["firstname", "lastname", "birthday", "gender"]

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @staticmethod  # decorative function
    def _generate_unique_id():
        return random.randint(100000, 999999)

    def save(self, *args, **kwargs):
        if not self.unique_id:
            ids = User.objects.values_list('unique_id', flat=True)
            unique_id = self._generate_unique_id()
            while unique_id in ids:
                unique_id = self._generate_unique_id()
            self.unique_id = unique_id
        super().save(*args, **kwargs)

    def friend_send_status(self, other_user):
        # Check if a friend request has been sent from self to other_user
        # agar men tomonimdan boshqa userga do'stlik yuborsam
        # True
        # False
        return self.requester.filter(receiver=other_user).exists() or \
            self.friendship_user2.filter(user1=other_user).exists() or \
            self.friendship_user1.filter(user2=other_user).exists()

    def __str__(self):
        return self.firstname


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    banner = models.ImageField(
        upload_to="profile/", blank=True, default="banner2.png")
    avatar = models.ImageField(
        upload_to="profile/", blank=True, default="avatar.png")
    bio = models.TextField(blank=True)

    # def save(self, *args, **kwargs):
    #     super().save()
    #     if self.avatar:
    #         img = Image.open(self.avatar.path)

    #         if img.height > 168 and img.width > 168:
    #             new_img = (168, 168)
    #             img.thumbnail(new_img)
    #             img.save(self.avatar.path)

    def __str__(self):
        return f"{self.user.firstname} {self.user.lastname} profili"


class About(models.Model):
    CITY = [
        ("Shaxarni tanlang", "Shaxarni tanlang"),
        ("Andijan", "Andijan"),
        ("Tashkent", "Tashkent"),
        ("Bukhara", "Bukhara"),
        ("Namangan", "Namangan"),
        ("Sirdaryo", "Sirdaryo"),
    ]
    MAKTAB = [
        ("15-Umumiy O'rta talim maktabi (Izboskan)",
         "15-Umumiy O'rta talim maktabi (Izboskan)")
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=30, choices=CITY)
    description = models.TextField()
    school = models.CharField(max_length=200, choices=MAKTAB, default=CITY[5])
    is_graduated = models.BooleanField(default=False)

    def __str__(self):
        return self.user.firstname


class FriendRequest(models.Model):
    """
    Request Friend -- do'st bo'lish uchun so'rov tashlash
    """
    PENDING = 'pending'  # kutilyabdi
    DECLINED = 'declined'  # rad etish
    ACCEPTED = 'accepted'  # qabul qildi

    STATUS_CHOICES = [
        ("PENDING", 'pending'),
        ("DECLINED", 'declined'),
        ("ACCEPTED", 'accepted')
    ]

    requester = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='requester')  # yuboruvchi
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver")  # qabul qiluvchi
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default=PENDING)

    class Meta:
        """
        yuboruvchi va qabul qiluvchi yagona bo'lishi kerak
        """
        unique_together = ("requester", "receiver")

    def __str__(self):
        return f"{self.requester.firstname} {self.requester.lastname} {self.receiver.firstname} {self.receiver.lastname}ga do'stlik sorovini yubordi. Holati {self.status}"


class Friendship(models.Model):
    user1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friendship_user1"
    )
    user2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friendship_user2"
    )

    class Meta:
        unique_together = ("user1", "user2")

    def __str__(self):
        return f"{self.user1}--{self.user2} do'stlar"
