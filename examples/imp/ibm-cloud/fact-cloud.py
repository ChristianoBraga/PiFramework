from flask import Flask
import atexit
import cf_deployment_tracker
import os
import json

import fact

# Emit Bluemix deployment event
cf_deployment_tracker.track()

app = Flask(__name__)
client = None

# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

@app.route('/')
def home():
    return str(fact.fact(10))

@atexit.register
def shutdown():
    if client:
       client.disconnect()

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=port, debug=True)
