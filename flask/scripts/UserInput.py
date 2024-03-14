
from flask import session, flash

# Getting the "where"
def SetAddress(start_address, end_address):
  error = False

  try:
    session['start_address'] = start_address
  except:
    flash(f'Error storing start address: ({ start_address })', 'error')
    error = True

  try:
    session['end_address'] = end_address
  except:
    flash(f'Error storing end address: ({ end_address })', 'error')
    error = True

  if error:
    raise('invalid start or end address')

    

def SetTime(month, dayOfWeek, time):
  month = int(month)
  dayOfWeek = int(dayOfWeek)
  error = False

  try:
    session['month'] = month
  except:
      flash(f'Error getting Month value with index ({ month })', 'error')
      error = True

  try:
    session['dayOfWeek'] = dayOfWeek
    
    if dayOfWeek == 6 or dayOfWeek == 7:
      session['weekend?'] = 1
    else:
      session['weekend?'] = 0
  except:
      flash(f'Error getting Day of Week value with index ({ dayOfWeek })', 'error')
      error = True


  try:
    # time is given as "hh:mm" in 24 hour format
    session['hour'] = int(time[0:2])
  except:
      flash(f'Error getting hour from Time ({time})', 'error')
      error = True

  if error:
    raise('invalid time input/s')
