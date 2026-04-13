import pyperclip
import requests
import socket
import urllib
import subprocess

pyperclip.copy("هذا النص تم نسخه إلى الحافظة!")  # نسخ
text = pyperclip.paste()  # لصق
print(text)