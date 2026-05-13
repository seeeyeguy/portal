from django.test import Client
from django.contrib.auth.models import User

client = Client()
user = User.objects.first()
print(user)
client.force_login(user)



