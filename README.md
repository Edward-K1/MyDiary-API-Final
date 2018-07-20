[![Build Status](https://travis-ci.org/Edward-K1/MyDiary-API.svg?branch=develop)](https://travis-ci.org/Edward-K1/MyDiary-API)
[![Coverage Status](https://coveralls.io/repos/github/Edward-K1/MyDiary-API/badge.svg?branch=feature)](https://coveralls.io/github/Edward-K1/MyDiary-API?branch=feature)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/bcdc7f46a0df4609a99c7fccf0281ec0)](https://www.codacy.com/app/Edward-K1/MyDiary-API?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Edward-K1/MyDiary-API&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/5a4da4bfaef192469018/maintainability)](https://codeclimate.com/github/Edward-K1/MyDiary-API/maintainability)

# MyDiary-API
This is an API to power MyDiary Front-End Pages

## How to run the tests:

 cd into API root directory, i.e /MyDiary-API/

 run the following command on a terminal: pytest ./v1/tests or: nosetests -v ./v1/tests


## Features

### The API can presently register two entities: user, and entry

#### The user entity accepts GET and POST requests

 The following fields are required for the user post request:

   firstname -> str , lastname -> str, username -> str, email -> str, password -> str

#### The entry entity accepts GET, POST, PUT, and DELETE requests:

 PUT and DELETE requests require an Id in the URL. The GET request for a specific entry also requires an Id.

 The fields required for POST and PUT are: title -> str and content -> str

### The api prefix is: /api/v1/

### The complete URLs for the entries are:

Locally:

user: http://127.0.0.1:5000/api/v1/user

entry: http://127.0.0.1:5000/api/v1/entry


On Heroku:

user: https://ek-mydiary-api.herokuapp.com/api/v1/user

entry: https://ek-mydiary-api.herokuapp.com/api/v1/entry

