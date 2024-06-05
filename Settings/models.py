import base64
import os
import uuid
from datetime import datetime, timedelta, timezone

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db import models
from cryptography.fernet import Fernet, InvalidToken
from hashlib import sha512, pbkdf2_hmac
import mariadb


# Create your models here.
class DB(models.Model):
    """Every DB has an owner. The owner is the only person who owns this DB. Hence the root PW is encrypted by the Fernet of the owner.
    The DB itself has a Fernet key for encrypting DB related queries (for instance: User creates DB (this is encrypted by the DB Fernet))
    The salt is used for hashing DB related things e.g. Passwords.
    """
    name = models.CharField(max_length=254)
    db_host = models.CharField(max_length=255)
    db_port = models.IntegerField()
    db_root = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    root_pw = models.CharField(max_length=255)
    secret_key = models.BinaryField()
    salt = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    revocation_id = models.BinaryField()
    url_id = models.CharField(max_length=64)
    def save(self, *args, **kwargs):
        self.secret_key = Fernet.generate_key()
        self.salt = os.urandom(64).hex()
        self.url_id = uuid.uuid4().__str__()
        self.revocation_id = os.urandom(64)

        self.root_pw = Fernet(Token.objects.get(owner_id=self.owner.pk).fernet).encrypt(str(self.root_pw).encode()).hex()
        # pbkdf2_hmac(hash_name='sha3_512', salt=self.salt.encode(),
        #  password=sha512(self.root_pw.encode(), usedforsecurity=True).hexdigest().encode(),
        # iterations=700000, dklen=127).hex()

        print(self.secret_key, self.salt, self.root_pw)
        super().save(*args, **kwargs)

    def get_root_pw(self, owner):
        usr = User.objects.get(pk=owner)
        if usr != self.owner.pk:
            raise PermissionDenied("You are not allowed to access the DB root PW of other users")
        fernet = Token.objects.get(owner_id=self.owner.pk).fernet
        try:
            return Fernet(fernet.encode()).decrypt(str(self.root_pw).encode()).decode('utf-8')
        except InvalidToken:
            raise PermissionDenied("You are not allowed to access the DB root, because the secret key is invalid")




    def __str__(self):
        return self.name


class Token(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    fernet = models.BinaryField()
    def save(self, *args, **kwargs):

        self.uuid = uuid.uuid4()
        self.fernet = Fernet.generate_key()
        super().save(*args, **kwargs)


class DBUser(models.Model):
    # db_schema = models.ForeignKey(DB, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    fernet = models.BinaryField()



    def save(self, *args, **kwargs):
        self.fernet = Fernet.generate_key()
        self.password = Fernet(self.fernet).encrypt(self.password.encode()).hex()
        super().save(*args, **kwargs)


class UserTemp(models.Model):
    added_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    db = models.ForeignKey(DB, on_delete=models.CASCADE)
    db_user = models.ForeignKey(DBUser, on_delete=models.CASCADE)
