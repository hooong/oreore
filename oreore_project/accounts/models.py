from django.db import models
from django.contrib.auth.models import User, BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, uid, name, age, sex, password=None):
        if not uid:
            raise ValueError('Users must have an id')

        user = self.model(
            uid=uid,
            name=name,
            age=age,
            sex=sex,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, uid, name, age, sex, password):
        user = self.create_user(
            uid,
            password=password,
            name=name,
            age=age,
            sex=sex
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    uid = models.CharField(
        verbose_name='uid',
        max_length=100,
        unique=True,
    )
    name = models.CharField(max_length=100, default='')
    age = models.IntegerField(default=0)
    sex = models.CharField(max_length=10, default='male') 
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'uid'
    REQUIRED_FIELDS = ['name','age','sex']

    def __str__(self):
        return self.uid

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
