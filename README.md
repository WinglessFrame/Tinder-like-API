# Tinder-like API (DRF+JWT+PostGIS)
### Technology stack:
* [Django](https://github.com/django/django)
* [Django Rest Framework](https://github.com/encode/django-rest-framework)
* [SimpleJWT](https://github.com/SimpleJWT/django-rest-framework-simplejwt)
* [GeoDjango](https://docs.djangoproject.com/en/3.1/ref/contrib/gis/)
* [PostgreSQL](https://www.postgresql.org/) [(PostGIS extension)](https://postgis.net/)
* [django-rest-framework-gis](https://github.com/openwisp/django-rest-framework-gis)
* [drf-spectacuar](https://github.com/tfranzel/drf-spectacular)
### Things to do
- [x] Docker
- [ ] Refactor code (Business Logic -> utils.py
- [ ] Cover with test
  - [x] Cover accounts app with tests
  - [ ] Cover GinderApp app with tesst
### All api endpoints you can look in [schema.yml](schema.yml) file (copypaste file in this editor [swagger.io](https://editor.swagger.io/))

### What is it about:
* User is able to create account
* User has subscription and location
* User can add posts to the account
* User can update and destroy own posts
* User can swipe (like in Tinder). He can see swipes limited amount per day (depends on subscription).
  Swipe consists of one post of random people around (range depends on subscription).
  User can like the post or skip to next swipe (go to the same endpoint). 
  User can't find the post of the person whose post he has already seen (excepts if user cleared his viewed list in profile).
  After two users liked posts of one another, the match chat is started where they can converse. 
  Any of participants can delete chat, so the chat will be finished.
  * default - 20/day, 10 km radius
  * silver - 100/day, 20 km raius
  * gold - over 9 thousand  😅, any radius
#### Profile endpoint gives this-like response:
```json5
{
    "username": "WinglessFrame",
    "bio": "Gleb, 18",
    "location": {
        "type": "Point",
        "coordinates": [
            27.554644,
            53.909845
        ]
    },
    "subscription": "silver",
    "search_distance": 25,
    "update_search_distance_url": "http://127.0.0.1:8000/app/api/profile/change_distance",
    "create_post_url": "http://127.0.0.1:8000/app/api/profile/add_post",
    "clear_viewed_url": "http://127.0.0.1:8000/app/api/profile/clear",
    "matches": [
        {
            "participants": "WinglessFrame-admin",
            "chat_url": "http://127.0.0.1:8000/app/api/chat/4"
        }
    ],
    "posts": [
        {
            "image": "http://127.0.0.1:8000/media/posts/WinglessFrame/heart_RiUejOu.png",
            "description": "Love from WinglessFrame",
            "delete_update_url": "http://127.0.0.1:8000/app/api/profile/posts/5"
        },
        {
            "image": "http://127.0.0.1:8000/media/posts/WinglessFrame/certificate.png",
            "description": "My standard",
            "delete_update_url": "http://127.0.0.1:8000/app/api/profile/posts/6"
        }
    ]
}
```
###### location in JSON set like this
```json5
{"type": "Point", "coordinates": [27.554644, 53.909845]}
```
where first coordinate - **longitude** , second - **latitude**
