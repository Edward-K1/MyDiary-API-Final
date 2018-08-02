[![Build Status](https://travis-ci.org/Edward-K1/MyDiary-API-Final.svg?branch=feature)](https://travis-ci.org/Edward-K1/MyDiary-API-Final)
[![Coverage Status](https://coveralls.io/repos/github/Edward-K1/MyDiary-API-Final/badge.svg)](https://coveralls.io/github/Edward-K1/MyDiary-API-Final)
[![Maintainability](https://api.codeclimate.com/v1/badges/3ef3d6259e631d10a56a/maintainability)](https://codeclimate.com/github/Edward-K1/MyDiary-API-Final/maintainability)


# MyDiary-API
This is an API to power MyDiary Front-End Pages

## Technologies used:
* Python 3
* Flask
* Virtualenv
* Postgres


## Getting Started:

Ensure the applications above are installed on your machine.

Clone the repo: `git clone https://github.com/Edward-K1/MyDiary-API-Final.git`

Create a virtual environment: `virtualenv venv`

Activate your virtual environment and install requirements:

(I'm assuming you're on windows)

```
$ cd venv/scripts
$ activate
$ cd ../..

$ pip install -r requirements.txt

```


## Features

The following endpoint are available:

|Http Method | Endpoint |  Functionality|
|------------- | :-------------: |  -------------|
| POST   | /api/v1/auth/signup      |  Registers a new user|
| POST   | /api/v1/auth/login       |  Logins a new user|
| POST   | /api/v1/entries          |  Registers a new diary entry|
| GET    | /api/v1/entries          |  Fetches a user's diary entries|
| GET    | /api/v1/entries/<entryId> | Gets a specific diary entry|
| PUT    | /api/v1/entries/<entryId> | Modifies a diary entry|
| DELETE | /api/v1/entries/<entryId> | Deletes a diary entry|

The API can be accessed on via the following URLs:

* Locally: http://localhost:5000

* On Heroku: https://ch3-api.herokuapp.com
