from flask import flash

import numpy as np

import pandas as pd

import joblib

from sklearn.preprocessing import StandardScaler

# location {location object} - location we want to verify is in Monroe county, IN
# api - Google Maps API instance we will use to 
def check_in_monroe(location, api):
    # Reverse geocode to get address components
    try:
      reverse_geocode_result = api.reverse_geocode((location['lat'], location['lng']))
    except:
       raise('error attempting to retrieve location info from lat/lng')
       return

    if reverse_geocode_result:
      county_info = reverse_geocode_result[0]['address_components'][4]
      county_name = county_info['long_name']
      state_info = reverse_geocode_result[0]['address_components'][5]
      state_name = state_info['long_name']

      if (county_name == 'Monroe County' and state_name == 'Indiana'):
         print('county success')
         return True
    
    print('county fail')
    return False

def preprocess(df):
  data = pd.DataFrame({
      'Latitude': df['Latitude'],
      'Longitude': df['Longitude'],
      'Month': df['Month'],
      'Day': df['Day'],
      'Hour': df['Hour']
  })

  # Define the values for Month, Hour, and Day
  months = list(range(1, 13))
  hours = list(range(24))
  days = list(range(1, 8))

  # Convert Month, Hour, and Day columns to categorical dtype
  data['Month'] = pd.Categorical(data['Month'], categories=months)
  data['Hour'] = pd.Categorical(data['Hour'], categories=hours)
  data['Day'] = pd.Categorical(data['Day'], categories=days)

  # Perform one-hot encoding for Month, Hour, and Day columns
  encoded_data = pd.get_dummies(data, columns=['Month', 'Day', 'Hour']).astype(int)
  scaler = StandardScaler()
  encoded_data['Latitude'] = scaler.fit_transform(encoded_data['Latitude'].values.reshape(-1, 1))
  encoded_data['Longitude'] = scaler.fit_transform(encoded_data['Longitude'].values.reshape(-1, 1))
  return encoded_data

def predict_new(features):
    import os
    current_dir = os.path.dirname(__file__)
    relative_path = os.path.join(current_dir, 'model', 'crash_prediction_model.joblib')
    try:
      model = joblib.load(relative_path)
    except Exception as e:
       flash(f'error loading model: {e}')

    X_new = pd.DataFrame([features], columns=['Latitude', 'Longitude', 'Month', 'Day', 'Hour'])
    X_new = preprocess(X_new)

    print(X_new)
    try:
      y_pred = model.predict(X_new)
    except Exception as e:
       flash(f'predicting error: {e}')
    return y_pred
