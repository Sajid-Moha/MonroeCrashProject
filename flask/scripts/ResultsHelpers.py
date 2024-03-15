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

def preprocess(df):
    scaler = StandardScaler()

    cats = ['Month', 'Day', 'Hour']
    # Separate numerical and categorical columns
    numerical_cols = df.select_dtypes(include=['float64']).columns
    categorical_cols = [col for col in cats if col in df.columns]

    # One-hot encode categorical columns
    one_hot_encoded = pd.get_dummies(df[categorical_cols], columns=categorical_cols).astype(int)

    # Concatenate numerical columns and one-hot encoded categorical columns
    df = pd.concat([df[numerical_cols], one_hot_encoded], axis=1)

    df['Longitude'] = scaler.fit_transform(df['Longitude'].values.reshape(-1, 1))
    df['Latitude'] = scaler.fit_transform(df['Latitude'].values.reshape(-1, 1))
    return df

def predict_new(features):
    model = joblib.load('.\\model\\crash_prediction_model.joblib')
    X_new = pd.DataFrame([features], columns=['Latitude', 'Longitude', 'Month', 'Day', 'Hour'])
    X_new = preprocess(X_new)
    
    y_pred = model.predict(X_new)
    return y_pred
