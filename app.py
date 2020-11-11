from dash import Dash
import dash_html_components as html
import os
from flask import Flask
from flask_simpleldap import LDAP


# Make Dash run on a Flask server
app = Dash(__name__, server=Flask(__name__))

# The Dash app
app.layout = html.P('Hello world!')

# Configure LDAP
app.server.config.update({
    'LDAP_BASE_DN': 'OU=users,dc=example,dc=org',
    'LDAP_USERNAME': 'CN=user,OU=Users,DC=example,DC=org',
    'LDAP_PASSWORD': os.getenv('LDAP_PASSWORD')})

# Protect view functions with LDAP authentication
for view_func in app.server.view_functions:
    app.server.view_functions[view_func] = LDAP(app.server).basic_auth_required(app.server.view_functions[view_func])

# Run Flask server
if __name__ == '__main__':
    app.run_server()

# For gunicorn
server = app.server
