from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User
from django.urls import reverse
import pytest
import datetime
from pytest_django.asserts import assertTemplateUsed


### All de user app was made with the django built-in package, so for that it has no sense to write test to it.

### Only it will be tested the Profile model attached to the User Model.

@pytest.fixture
def creation_of_user():
    user = User.objects.create(username = 'TestUser', first_name = 'John Doe', email = 'Johndoe@gmail.com', password = 'asd123')
    return user

@pytest.mark.django_db
def test_creation_user(creation_of_user):
    user = creation_of_user
    user_db = User.objects.all()
    profile = Profile.objects.create(user=user,date_of_birth = '2022-05-03')
    assert user.username == user_db[0].username


@pytest.mark.django_db
def test_creation_profile(creation_of_user):
    profile = Profile.objects.create(user=creation_of_user,date_of_birth = '2022-05-03')
    assert profile.user.username == 'TestUser'
    assert profile.date_of_birth == '2022-05-03'

@pytest.mark.django_db
def test_creation_user_form(client):
    data = {'username' : 'TestUser',
            'first_name' : 'John',
            'email' : 'johndoe@gmail.com',
            'password' : 'asd123',
            'password2' : 'asd123'}

    url_form = reverse('register')
    response = client.post(url_form, data = data)
    user = User.objects.all()[0]
    profile = Profile.objects.all()[0]

    assert response.status_code == 200
    assert profile.user == user
    assert user.username == 'TestUser'
    assertTemplateUsed(response, "account/register_done.html")

@pytest.mark.django_db
def test_edit_profile_form(client,creation_of_user):
    user = creation_of_user
    Profile.objects.create(user=user)
    client.force_login(user)
    first_name_used = Profile.objects.all()[0].user.first_name
    assert first_name_used == 'John Doe'

    data = {'date_of_birth' : '2022-05-03',
    'first_name':'Maquinola'}

    url_form = reverse('edit')
    response = client.post(url_form, data = data)
    profile_created = Profile.objects.all()[0]
    
    assert response.status_code == 200
    assert str(profile_created.date_of_birth) == '2022-05-03'
    assert str(profile_created.user.first_name) == 'Maquinola'
    assertTemplateUsed(response, "account/edit.html")




# Create your tests here.
