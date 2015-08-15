# django-heroku-settings
Manage Django settings via Heroku environment config variables

## Summary
This is an example of how to manage Django settings locally while hosting a Django web app on Heroku. 

The main concept here is that Heroku should contain most of the sensitive secret settings, such as the project's `SECRET_KEY`, database configs, and third party API keys, tokens, and passwords.

## Steps to add a setting
Here's the workflow:

###Add the setting to Heroku
Add the setting to Heroku *first*. Yes, even new ones that are in the process of being tested. You can either use the Heroku web console or the `heroku config:set` toolbelt command. More https://devcenter.heroku.com/articles/config-vars 
 
###Get the setting locally
Run the `export_envs.sh` script to bring those settings into your local environment. Note that some settings should diverge locally vs. production. For example, you probably want to use a local db instead of the prod db. The solution for these is to use the `local` arg when running `export_envs.sh`. So:

```bash
$ source ./export_envs.sh my-app-name local
```

###Launch your IDE
If you use an IDE, launch it from the shell that has these settings sourced:

```bash
$ source ./export_envs.sh my-app-name local
$ open /Applications/PyCharm.app
```

###Load settings in Django
In your Django `settings.py`, load those sensitive settings from the operating system evironment variables to make them available to your Django code.

Note that some settings are "required", so we use a little function that raises an error if the environment variable isn't set:

```python
SECRET_KEY = get_required_env_var("SECRET_KEY")
```

Others are more "optional" so we can just get them (and handle `None` in code):

```python
THIRD_PARTY_API_TOKEN = os.getenv("THIRD_PARTY_API_TOKEN")
```
