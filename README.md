# Jetson nano

This sections contains example where a Jetson Nano controls a Lego Technic Hub


## Prerequisites

Jetson Nano with the intel wifi + bluetooth card.

Flask is needed to execture the flask_app

    pip3 install flask --user




pygatt package is used to connect to the Lego Hub

    pip3 install pygatt --user

This fork of pylgbst which can be installed by cloning this repo and then:

    python3 setup.py install --user


## Starting the app
To start the app
    sudo python3 examples/jetson_nano/flask_app.py

