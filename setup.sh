#!/bin/bash
sudo apt-get install -y git python python-pip python-dev libssl-dev libmysqlclient-dev libffi-dev libjpeg-dev libcurl4-openssl-dev libmagickwand-dev
sudo pip install virtualenvwrapper
mkdir venv
virtualenv venv/
source venv/bin/activate && sudo pip install -r requirements.txt
