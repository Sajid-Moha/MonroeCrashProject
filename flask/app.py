# Flask : the app that creates web environment
# url_for : returns path to files & site path to function
# render_template: provide jinja template for use as return value
from flask import Flask, url_for, render_template

# escape : prevents code injection into returned html
from markupsafe import escape

# request : get data from client
# redircet : transfer client to other URL
from flask import request, redirect

from flask import session, flash, get_flashed_messages

from scripts.UserInput import SetLatLong

app = Flask(__name__)
app.secret_key = 'doesntmatter'

@app.route('/', methods=['GET'])
def Home():
    return render_template('home.html')

@app.route('/processing/', methods=['POST'])
def ProcessResults():
    try:
      SetLatLong(request.form.get('Latitude'),
                  request.form.get('Longitude'))
    except:
      return redirect( url_for('Home') )
    
    return redirect( url_for('Results') )

@app.route('/results/')
def Results():
    try:
      latitude = session['lat']
      longitude = session['long']
    except:
       return redirect( url_for('Home') )       
    
    return f'Results Page For Latitude {escape(latitude)} and Longitude {escape(longitude)}'
