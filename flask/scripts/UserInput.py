
from flask import session, flash

# Getting the "where"
def SetLatLong(latitude, longitude):
    error = False

    try:
      session['lat'] = float(latitude)
    except:
      flash(f'Error converting value of Latitude ({latitude}) to a float', 'error')
      error = True
    
    try:
      session['long'] = float(longitude)
    except:
      flash(f'Error converting value of Longitude ({longitude}) to a float', 'error')
      error = True

    if error:
      raise('invalid latitude or longitude')
    
# Getting the "when"

    

  