
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class MyAccountManager(BaseUserManager):

	def create_user(self, email, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		#if not username:
		#	raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password):
		user = self.create_user(
			email=self.normalize_email(email),
		)
		user.is_admin = True
		user.is_active = True
		user.is_staff = True
		user.is_superuser = True
		user.set_password(password)
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	email 					= models.EmailField(verbose_name="email", max_length=60,unique=True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.SmallIntegerField(default=False)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	type_of_user            = models.SmallIntegerField(default=3)
	password_reset			= models.BooleanField(default=False)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True


class AccountDetail(models.Model):
	account=models.ForeignKey(Account, on_delete=models.CASCADE)
	user_last_name =models.CharField(max_length=30,null=True)
	user_first_name         =models.CharField(max_length=30,null=True)
	phone                   = models.CharField(max_length=30,null=True,blank=True)
	address                 = models.TextField(null=True)
	def _str_(self):
		return self.user_first_name