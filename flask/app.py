# Flask : the app that creates web environment
# url_for : returns path to files & site path to function
# render_template: provide jinja template for use as return value
from flask import Flask, url_for, render_template

# request : get data from client
# redircet : transfer client to other URL
# session: store information in cookies
from flask import request, redirect, session, flash

# address, time value verifier
from scripts.UserInput import SetAddress, SetTime

# get safest path
from scripts.CalculateResults import CalculateResult

app = Flask(__name__)
app.secret_key = 'doesntmatter'

@app.route('/', methods=['GET'])
def Home():
    return render_template('home.html')

@app.route('/processing/', methods=['POST'])
def ProcessResults():
    try:
      SetAddress(request.form.get('startAddress'),
                  request.form.get('endAddress'))
      SetTime(request.form.get('month'),
              request.form.get('dayOfWeek'),
              request.form.get('time'))
    except:
      return redirect( url_for('Home') )
    
    try:
       CalculateResult()
    except:
      flash(f'Error Calculating Route', 'error')
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

      # result
      session['result']
    except:
       return redirect( url_for('Home') )       
    
    return render_template('results.html')
