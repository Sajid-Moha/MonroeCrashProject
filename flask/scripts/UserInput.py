
from flask import session, flash

# Getting the "where"
def SetLatLong(start_latitude, start_longitude,
               end_latitude, end_longitude):
    error = False

    try:
      session['start_lat'] = float(start_latitude)
    except:
      flash(f'Error converting value of Start Latitude ({start_latitude}) to a float', 'error')
      error = True
    
    try:
      session['start_long'] = float(start_longitude)
    except:
      flash(f'Error converting value of Start Longitude ({start_longitude}) to a float', 'error')
      error = True

    try:
      session['end_lat'] = float(end_latitude)
    except:
      flash(f'Error converting value of End Latitude ({end_latitude}) to a float', 'error')
      error = True
    
    try:
      session['end_long'] = float(end_longitude)
    except:
      flash(f'Error converting value of End Longitude ({end_longitude}) to a float', 'error')
      error = True

    if error:
      raise('invalid latitude or longitude')

    

  