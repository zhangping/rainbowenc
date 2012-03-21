#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib

def savepass(password):
    if hashlib.md5(password.password_old).hexdigest() != open("passwd").readline():
      return "old password is invalid"

    if password.password_new != password.password_confirm:
      return "password unmatch"

    f = open("passwd", "w")
    f.write(hashlib.md5(password.password_new).hexdigest())
    f.close()

    return "OK"
