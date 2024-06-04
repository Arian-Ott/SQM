import base64
import os
import uuid
from datetime import datetime, timedelta, timezone

from django.contrib.auth.models import User
from django.db import models
from cryptography.fernet import Fernet
from hashlib import sha512, pbkdf2_hmac
import mariadb


# Create your models here.
class DB(models.Model):
    name = models.CharField(max_length=254)
    db_host = models.CharField(max_length=255)
    db_port = models.IntegerField()
    db_root = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    root_pw = models.CharField(max_length=255)
    secret_key = models.BinaryField()
    salt = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.secret_key = Fernet.generate_key()
        self.salt = os.urandom(64).hex()

        # pbkdf2_hmac(hash_name='sha3_512', salt=self.salt.encode(),
        #  password=sha512(self.root_pw.encode(), usedforsecurity=True).hexdigest().encode(),
        # iterations=700000, dklen=127).hex()

        print(self.secret_key, self.salt, self.root_pw)
        super().save(*args, **kwargs)



    def __str__(self):
        return self.name

class Token(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    valid_till = models.DateTimeField()
    def save(self, *args, **kwargs):
        self.valid_till = datetime.now() + timedelta(minutes=10)
        self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)

class DBUser(models.Model):
    #db_schema = models.ForeignKey(DB, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):

        self.fernet = Fernet.generate_key()
        self.password = Fernet(self.fernet).encrypt(self.password.encode()).hex()
        super().save(*args, **kwargs)

