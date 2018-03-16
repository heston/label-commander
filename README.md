# Label Commander

A voice-activated label printer utilizing Google Assistant, a Raspberry Pi, and a Dymo
LabelWriter.

> OK Google, print a label called "Awesome"

## Overview

This is a client that runs on a RaspberryPi connected to a Dymo LabelWriter. The Pi
should have CUPS installed, along with the appropriate Dymo drivers.

There is also [a server (of sorts)](https://github.com/heston/label-commander-server),
in the form of a Firebase Cloud Function. This should be configured and running on
a Firebase account. The Firebase key for that account needs to be copied onto the Pi
at the location specified in [env.sh](env.example.sh).

Finally, an [IFTTT applet](https://ifttt.com/google_assistant) listens for 
commands from Google Assistant and dispatches requests to the Cloud Function endpoint
(via a Webhook action).

## Installation

If anyone is interested in more detailed set up instructions, open a Github issue, and
I'll see what I can do.
