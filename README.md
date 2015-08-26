42-test template
===========================

A Django 1.6+ project template

Use fortytwo_test_task.settings when deploying with getbarista.com

### Local testing
* create virtualenv, install requirements from requirements.txt with pip
* make syncdb - runs syncdb
* make migrate - runs migrations
* make test - executes tests
* make run - runs local development server


### Recomendations
* apps in apps/ folder
* use per-app templates folders
* use per-app static folders
* use migrations
* use settings.local for different environments
* common templates live in templates/
* common static lives in assets/
* management commands should be proxied to single word make commands, e.g make test

