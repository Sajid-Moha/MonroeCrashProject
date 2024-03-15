from flask import session, flash
import googlemaps

from scripts.ResultsHelpers import check_in_monroe, predict_new

# Define API keys
maps = googlemaps.Client(key='AIzaSyA0d67PUz3V85_QpTCcnQ9AdAEka9AJGHM')

def CalculateResult():
  routeID_map = {}
  pred_crashes_map = {}


  # "Where"
  # e.g. 'Cloverleaf South Reastaurant, IN'
  origin = session['start_address']
  destination = session['end_address']

  # "When"
  month = session['month']
  day = session['dayOfWeek']
  hour = session['hour']

  # Request route from Directions API
  try:
    routes = maps.directions(origin, destination, mode="driving", alternatives=True)
  except Exception as e:
     flash(f'Error retrieving direction from Google Maps : {e}', 'error')
  routeCtr = 1

  # Extract route steps
  for route in routes: 
      try:
        routeID_map[routeCtr] = route
        pred_crashes_map[routeCtr] = 0
        
        steps = route['legs'][0]['steps']
      except Exception as e:
         flash(e)
         raise(e)
      
      try:
        # Check if origin or destination address is in Monroe County
        if not check_in_monroe(steps[0]['start_location'], maps):
            flash(f'Start address not in Monroe County: ({ origin }), {steps[0]["start_location"]}', 'error')
            raise('Start address not in Monroe County')
        if not check_in_monroe(steps[len(steps)-1]['end_location'], maps):
            flash(f'Destination address not in Monroe County: ({ destination }), {steps[len(steps)-1]["end_location"]}', 'error')
            raise('Destination address not in Monroe County')
      except Exception as e:
         print('ouch')
         flash(f'{e}')
      
      # Iterate over steps
      for step in steps:
          start_point = step['start_location']
          end_point = step['end_location']

          try:
            # Request latitude and longitude for start point
            start_address = maps.reverse_geocode((start_point['lat'], start_point['lng']))

            # Request latitude and longitude for end point
            end_address = maps.reverse_geocode((end_point['lat'], end_point['lng']))
          except Exception as e:
             flash(f'Error requesting lat/long for start/end: {e}')
             raise('Error requesting lat/long for start/end')

          ##############
          print('model')
          # TODO: Run model on end_point latitude/longitude + time (month, day, hour)
          # Run model on end_point latitude, end_point longitude, month, day, hour
          X_new_features = [end_point['lat'], end_point['lng'], month, day, hour]
          try:
            model_result = predict_new(X_new_features)
          except:
             flash("model exception")
             raise("model exception")
          if model_result == 1:
              pred_crashes_map[routeCtr] += 1
          print('model success')
              
          #print(f"Start: {start_address[0]['formatted_address']} ({start_point['lat']}, {start_point['lng']})")
          #print(f"End: {end_address[0]['formatted_address']} ({end_point['lat']}, {end_point['lng']})")
          #print('---')
          
      routeCtr += 1
  # Calculate safest route (least "Yes" crash predictions
  min_routeID = min(pred_crashes_map, key=pred_crashes_map.get)
  safest_route = routeID_map[min_routeID]
  session['result'] = safest_route


