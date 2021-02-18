# Tinder-like-API
## Tinder-like-API on django rest framework

### Technology stack:
* [Django](https://github.com/django/django)
* [Django Rest Framework](https://github.com/encode/django-rest-framework)
* [SimpleJWT](https://github.com/SimpleJWT/django-rest-framework-simplejwt)
* [GeoDjango](https://docs.djangoproject.com/en/3.1/ref/contrib/gis/)
* [PostgreSQL](https://www.postgresql.org/) [(PostGIS extension)](https://postgis.net/)
* [django-rest-framework-gis](https://github.com/openwisp/django-rest-framework-gis)

### What is it about:
* User is able to create account
* User has subscription and location
* User can add posts to the account
* User can swipe (like in Tinder). He can see swipes limited amount per day (depends on subscription).
  Swipe consists of one post of random people around (range depends on subscription).
  User can like the post or skip to next swipe (go to the same endpoint). 
  User can't find the post of the person whose post he has already seen (excepts if user cleared his viewed list in profile).
  After two users liked posts of one another, the match chat is started where they can converse. 
  Any of participants can delete chat, so the chat will be finished.
