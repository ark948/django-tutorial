# these commands must be ran in django shell, this is just a reference
from django.test.utils import setup_test_environment
setup_test_environment()

from django.test import Client
client = Client()

resposne = client.get("/")
# expected 404

resposne.status_code
# 404

from django.urls import reverse
response = client.get(reverse("polls:index"))
resposne.status_code
# expected 200
 
response.content
# html code

response.context["latest_question_list"]