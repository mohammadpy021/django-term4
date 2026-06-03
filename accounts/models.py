from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

class CustomUserManager(UserManager):
    ''' custom user manager '''

    # def _create_user(self, email, password, **extra_fields):
    #     if not email:
    #         raise ValueError("The given email must be set")
    #     extra_fields.setdefault("is_staff", False)
    #     extra_fields.setdefault("is_superuser", False)
    #     email = self.normalize_email(email)
    #     user = self.model( email=email, **extra_fields)
    #     user.password = make_password(password)
    #     # user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        if not email:
            raise ValueError("The given email must be set")
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        email = self.normalize_email(email)
        user = self.model( email=email, **extra_fields)
        user.password = make_password(password)
        # user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        # super(self).create_superuser(self, username, email=None, password=None, **extra_fields)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)#custom

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_verified") is not True:#custom
            raise ValueError("Superuser must have is_verified=True.")

        return self.create_user( email, password, **extra_fields)

class User(AbstractUser):
    username = models.CharField(("username"), max_length=150,      
        help_text=("150 characters or fewer. Letters, digits and @/./+/-/_ only."),
    )
    is_verified = models.BooleanField(("verified"),
        default=False,
        help_text=("user verification by email"),)
    email = models.EmailField(("email address"), unique=True)
    courses = models.ManyToManyField("article.course",verbose_name=_("دوره های کاربر") )
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    def __str__(self) -> str:
        return self.username


def set_username(sender, instance, **kwargs):
    if not instance.username:
        instance.username = instance.email.split('@')[0]
models.signals.pre_save.connect(set_username, sender=User)


# class Profile(models.Model):
 #   ''' got error '''
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
#     first_name = models.CharField(max_length=255, blank=True, null=True)
#     last_name = models.CharField(max_length=255, blank=True, null=True)
#     image = models.ImageField(_("image"), upload_to='profile', blank=True)   

# def create_profile(sender, instance, **kwargs):
#     Profile.objects.create(first_name = "s")
# models.signals.post_save.connect(create_profile, sender=User)