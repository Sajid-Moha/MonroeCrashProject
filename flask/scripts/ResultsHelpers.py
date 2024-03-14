from flask import flash

# location {location object} - location we want to verify is in Monroe county, IN
# api - Google Maps API instance we will use to 
def check_in_monroe(location, api):
    # Reverse geocode to get address components
    try:
      reverse_geocode_result = api.reverse_geocode((location['lat'], location['lng']))
    except:
       raise('error attempting to retrieve location info from lat/lng')
       return
    print(county_name, state_name)

    if reverse_geocode_result:
      try:
        county_info = reverse_geocode_result['address_components'][4]
        county_name = county_info['long_name']
        state_info = reverse_geocode_result['address_components'][5]
        state_name = state_info['long_name']
      except:
         raise('Error attempting to get county info')
         return

      if (county_name == 'Monroe County' and state_name == 'Indiana'):
         return True
    
    return False
