from django.db import models
from django.contrib.auth.models import(BaseUserManager, AbstractBaseUser, PermissionsMixin)

class CustomUserManage(BaseUserManager):
    def create_user(self, email, username, fullName, password=None):
        if not email or not username or not fullName:
            raise ValueError('bosh qatorlar bor')
        if not password and len(password) < 5:
            raise ValueError('parol notogri')


        user = self.model(
            email=self.normalize_email(email),
            username=username,
            fullName=fullName,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, fullName, password=None):
        user = self.create_user(
            email,
            username=username,
            fullName=fullName,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    fullName = models.CharField(max_length=50)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    step_completed =models.BooleanField(default=False)
    category = models.CharField(max_length=50, null=True)
    is_creator = models.BooleanField(default=False)
    is_salesman = models.BooleanField(default=False)
    objects = CustomUserManage()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'fullName']

    def __str__(self):
        return "{}- {}".format(self.username, self.fullName)
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True


    @property
    def is_staff(self):
        return self.is_active
    

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=150)
    avatar = models.ImageField(upload_to="profile/avatar/", null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    gender = models.CharField(max_length=50)
    
    def __str__(self):
        return "%sning profili" % self.user.fullName