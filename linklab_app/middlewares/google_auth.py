import requests
import shortuuid
from ..models import User
# from expedichat_app.models import User
from django.contrib.auth.models import User
from linklab_app.serializers import UserRegistrationSerializerwithgoogle

from dotenv import dotenv_values

env_vars = dotenv_values()


ANDROID_CLIENT_ID_PRO = '71455877223-79an0acu3v0dh816720tscve697ntqhb.apps.googleusercontent.com'
# WEBAPP_CLIENT_ID_PRO = env_vars['WEBAPP_CLIENT_ID_PRO']
# IOS_CLIENT_ID_PRO = env_vars['IOS_CLIENT_ID_PRO']

VALID_CLIENT_IDS = {
    ANDROID_CLIENT_ID_PRO,
    # WEBAPP_CLIENT_ID_PRO,
    # IOS_CLIENT_ID_PRO
    
}


def verify_google_token(access_token, app_client):
  
    response = requests.get(f'https://www.googleapis.com/oauth2/v3/tokeninfo?access_token={access_token}')
    # print("response",response)
    if response.status_code == 200:
        token_info = response.json()
        if token_info['aud'] not in VALID_CLIENT_IDS:
            raise ValueError('Invalid audience')
        return token_info
    else:
        raise ValueError('Token verification failed')
       

def get_google_user_info(access_token):
    url = f"https://www.googleapis.com/oauth2/v1/userinfo"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad requests
        data = response.json()
        return data
  
    except requests.exceptions.RequestException as err:
        print("Something went wrong:", err)
        raise ValueError("Failed to retrieve user information")
    


def generate_unique_referral_code(number):
    return shortuuid.uuid()[:number]  


def create_users(user_data):
    try:
        serializer = UserRegistrationSerializerwithgoogle(data=user_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return user
    except Exception as error:
        return str(error)
