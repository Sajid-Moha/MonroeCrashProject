# Flask : the app that creates web environment
# url_for : returns path to files & site path to function
# render_template: provide jinja template for use as return value
from flask import Flask, url_for, render_template

# request : get data from client
# redircet : transfer client to other URL
# session: store information in cookies
from flask import request, redirect, session

# lat/longitude value verifier
from scripts.UserInput import SetLatLong, SetTime

app = Flask(__name__)
app.secret_key = 'doesntmatter'

@app.route('/', methods=['GET'])
def Home():
    return render_template('home.html')

@app.route('/processing/', methods=['POST'])
def ProcessResults():
    try:
      SetLatLong(request.form.get('startAddress'),
                  request.form.get('endAddress'))
      SetTime(request.form.get('month'),
              request.form.get('dayOfWeek'),
              request.form.get('time'))
    except:
      return redirect( url_for('Home') )
    
    return redirect( url_for('Results') )

@app.route('/results/')
def Results():
    try:
      # where
      session['start_address']
      session['end_address']

      # when
      session['month']
      session['dayOfWeek']
      session['weekend?']
      session['hour']
    except:
       return redirect( url_for('Home') )       
    
    # return render_template('results.html')

    from markupsafe import escape
    return (f'Start addy: {escape(session['start_address'])}' +
           f', End addy: {escape(session['end_address'])}' +
           f', Month: {escape(session['month'])}, dow: {escape(session['dayOfWeek'])}, w?: {escape(session['weekend?'])}, hour: {escape(session['hour'])}')
