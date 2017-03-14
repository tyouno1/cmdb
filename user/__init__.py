#encoding: utf-8
from flask import Flask
import os
app = Flask(__name__)
# 生成随机32位的KEY, os.urandom(32)
app.secret_key = '\x11\x1fL\x931M\x16I\x8f\xddR\xc2jk\xe37\xdf\xbd\x8f\xd1\x9c\x9e\x1c\x1c\x89o\xc8\xa7\xf2\xe7H^'
#app.secret_key = os.urandom(32)

import views
