Phimp.me Generator
=======

The whole project includes this repo and the Android app. It aims to create a photo sharing app and a generator that can customize it. This repo is the generator part, which is a website where users can customerize their own photo app with their own name and own set of functions.

Installation
-------

This repo contains a Django website, and the generator script ([gen_script.py](phimpme/generator/blob/master/Phimpme/Phimpme/settings.py)).
To test the whole website:

1. [Install Django](https://www.djangoproject.com/download/)
2. Go to `Phimpme/Phimpme/apps/appshop/gen_script.py` you will see  
`template_path = "/Users/yzq/Documents/GitHub/phimpme-android/Phimpme"`  
Change it to the path of the source code of Phimp.me Android app.
3. Create a `local.properties` file in Phimp.me Android app, as described in [the app wiki](https://github.com/phimpme/android/wiki#build-in-command-line).
3. Go to the root of this repo and execute `python manage.py syncdb` to create the SQLite database file and create admin account.
4. Execute `python manage.py loaddata Phimpme/apps/appshop/appshop.json` to load settings.
5. Execute `python manage.py runserver` to start the web server.
6. Then you will see the website through http://localhost.

Also you need the Android SDK to run the generator script. You can see details in [the wiki of Phimp.me Android app](https://github.com/phimpme/android/wiki#build-in-command-line).

To test the generator script alone, open the py file and the last several lines will help you.

If you want to deploy this website into a production environment, **DO NOT FOLLOW THE STEPS ABOVE**. See the [deployment part in the wiki](../../wiki#deployment) instead.

Development Environment
-------

Django 1.6.5

Python 2.7.5

Project Details
-------

For detailed information of this project, please visit the [wiki](../../wiki) of this repo.
