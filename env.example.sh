########################################
##          System Settings           ##
########################################

##
## Firebase (required)
##
## These settings configure how the client communicates with the server.
## The values will be specific to your Firebase server deployment.
##

export LC_FIREBASE_APP_NAME=my-app
export LC_FIREBASE_KEY_PATH=/home/pi/firebasekey.json
export LC_FIREBASE_API_KEY=key
export LC_FIREBASE_DATABASE_URL=https://my-app-name-default-rtdb.firebaseio.com/


## The name of the LabelWriter printer as it appears in CUPS

export LC_CUPS_PRINTER_NAME=DYMO_LabelWriter_330


## The desired log level
## This should probably be ERROR or INFO during normal usage

export LC_LOGGING_LEVEL=DEBUG
