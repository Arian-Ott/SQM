
#   <one line to give the program's name and a brief idea of what it does.>
#      Copyright (c) 2024,.  Arian Ott
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

import hashlib
import os
from multiprocessing import Process

from django.contrib.auth.models import AbstractUser, User
from django.db import models

from SQM.settings import HIGH_SEC


class UserRecovery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    recovery_token = models.BinaryField()
    salt = models.BinaryField()

    def _calc_function(self, HIGH_lol):

        match HIGH_lol:
            case "AREA51":
                hashname = "SHA3_512"
                dklen = 256
                it = 1_000_000
            case "INSANE":
                hashname = "SHA3_512"
                dklen = 128
                it = 900_000
            case "HIGH":
                hashname = "SHA3_512"
                dklen = 128
                it = 700_000
            case "NORMAL":
                hashname = "SHA3_256"
                dklen = 64
                it = 700_000
            case "LOW":
                hashname = "SHA_256"
                dklen = 64
                it = 100_000
            case _:
                raise Exception(
                    "Wrong mode selected, please choose either 'AREA51' or 'INSANE' or 'HIGH' or 'NORMAL' or 'LOW'")

        self.recovery_token = hashlib.pbkdf2_hmac(hash_name=hashname, password=self.recovery, salt=self.salt,
                                                  iterations=it, dklen=dklen)

    def _calc_salt(self):

        self.salt = hashlib.sha3_512(bytes(os.urandom(129))).digest()
        self._calc_function(HIGH_SEC)

    def recovery_token_lul(self):
        p1 = Process(target=self._calc_salt, args=(self,))

        print("p1 start")

        p1.start()

        p1.join(
        )

        print(self.recovery_token
              )
        print("p2 start")

        print("p2 join")

    def __init__(self):
        super().__init__()

        self.recovery_token_lul()
