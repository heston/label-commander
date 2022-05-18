# Label Commander

A voice-activated label printer utilizing Google Assistant, a Raspberry Pi, and a Dymo
LabelWriter.

> OK Google, print a label called "Awesome"

## Overview

This is a client that runs on a Raspberry Pi connected to a Dymo LabelWriter. The Pi
should have CUPS installed, along with the appropriate Dymo drivers. Technically, this
doesn't have to run on a Pi. It can run on any computer that has access to a CUPS print
queue. However, I've only tested it on a Raspberry Pi.

There is also [a server (of sorts)](https://github.com/heston/label-commander-server),
in the form of Firebase Cloud Functions.

Finally, an [IFTTT applet](https://ifttt.com/google_assistant) listens for
commands from Google Assistant and dispatches requests to the Cloud Function endpoint
(via a Webhook action).

## Installation

### Python

This project is only compatible with Python 3. It will work with Python 3.7+ at least,
and may work with older versions of Python 3, but these haven't been tested. It is not
compatible with Python 2.

### CUPS & Dymo

Ensure you have a Dymo LabelWriter connected to a Unix-like system running CUPS,
and that the computer can print to the Dymo.

Setting that up is outside the scope of this document, but [this guide](https://www.baitando.com/it/2017/12/12/install-dymo-labelwriter-on-headless-linux)
is pretty helpful.

### LaTeX

Ensure `texlive` is installed on your system. If on a Raspberry Pi, it may be already installed.
Run `pdflatex` on the command line to find out. If not, it's fairly easy to install.

On the command line run:

```
sudo apt update
sudo apt install texlive
```

### Firebase

1. [Create a Firebase project](https://firebase.google.com/docs/web/setup#create-project).
1. [Create a Firebase Realtime Database](https://firebase.google.com/docs/database/web/start).
1. [Register a Web App](https://firebase.google.com/docs/web/setup#register-app).
1. Make note of (e.g. save somewhere) several values on the last screen of the previous step. You'll
    need these later:
    1. `apiKey`
    1. `databaseURL`
    1. `projectId`
1. Generate a new private key for your project:
    1. In the Firebase console, open **Settings > Service Accounts**.
    1. Click **Generate New Private Key**, then confirm by clicking **Generate Key**.
    1. Copy the downloaded file to the machine you will run this program on (i.e. the Raspberry Pi).
    1. Make note of the path to the file.
1. Clone this repo onto your Raspberry Pi (or other Linux system). `cd` into the cloned directory.
1. Copy `env.example.sh` to `env.sh`. e.g. `cp env.example.sh env.sh`.
1. Open `env.sh` and edit several values:
    1. Set `LC_FIREBASE_APP_NAME` to the value of `projectId`.
    1. Set `LC_FIREBASE_KEY_PATH` to the absolute path of the location where you copied the private key file.
    1. Set `LC_FIREBASE_API_KEY` to the value of `apiKey`.
    1. Set `LC_FIREBASE_DATABASE_URL` to the value of `databaseURL`.
    1. Set `LC_CUPS_PRINTER_NAME` to the name of the CUPS printer queue of your LabelWriter. This value will get turned into the command:
       ```
       lp -d LC_CUPS_PRINTER_NAME filename
       ```
       Ensure you can print to your Dymo this way from the command-line before proceeding.
    3. Save and close the file.
1. `make setup` to get your virtual environment bootstrapped.
1. `make run` to start the client.
1. If all is well, you should have a running client connected to your Firebase Realtime Database.
1. To have the client run automatically on boot: `sudo make install`.
1. To undo the previous step: `sudo make uninstall`.

### Cloud Functions

Now, head over to [Label Commander Server](https://github.com/heston/label-commander-server)
and follow the instructions there to get the cloud functions running and configure an IFTTT
applet to interface with them.

## Customizing

The `templates` directory contains a LaTeX template (label.tex) that defines the format of
the printed label. You can change this template to customize the size and content of the label.
