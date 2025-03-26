from django.dispatch import Signal, receiver
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from .models import ShortenedURL

import requests
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
# from .models import ShortenedURL, URLVisit

# def get_client_ip(request):
#     """Extract the IP address of the user"""
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         return x_forwarded_for.split(',')[0]
#     return request.META.get('REMOTE_ADDR')

def get_client_ip(request):
    """Extracts the client's IP address, even behind proxies"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    # Handle localhost IPs
    if ip in ("127.0.0.1", "::1"):
        ip = "8.8.8.8"  # Use Google's public IP for testing local requests

    return ip



def get_location(ip):
    """Fetch location data using IP address"""
    try:
        # response = requests.get(f'http://ipinfo.io/{ip}/json')
        response = requests.get(f'http://ip-api.com/json/{ip}')
        data = response.json()
        # Extract city, region, country, latitude, and longitude
        city = data.get('city', 'Unknown')
        region = data.get('regionName', 'Unknown')
        country = data.get('country', 'Unknown')
        lat = data.get('lat', 'Unknown')
        lon = data.get('lon', 'Unknown')
        return f"{city}, {region}, {country}, Latitude: {lat}, Longitude: {lon}"
        # return f"{data.get('city', 'Unknown')}, {data.get('region', 'Unknown')}, {data.get('country', 'Unknown')}, {data.get('Latitude / Longitude', 'Unknown')}"
    except Exception:
        return "Unknown location"

def get_device_type(user_agent):
    """Detect if the user is on Mobile or Desktop"""
    user_agent = user_agent.lower()
    if 'mobile' in user_agent:
        return 'Mobile'
    elif 'tablet' in user_agent:
        return 'Tablet'
    else:
        return 'Desktop'

# Define a custom signal
track_redirect_signal = Signal()

# Set up a receiver to listen for the signal
@receiver(track_redirect_signal)
def track_redirect(sender, request, short_code, **kwargs):
    """ Track IP, location, and device asynchronously after redirect starts """
    ip = get_client_ip(request)
    location = get_location(ip)
    user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')
    device_type = get_device_type(user_agent)

    # Log or store tracking info
    print(f"Tracked - Device: {device_type}, Location: {location}, IP: {ip}, Short Code: {short_code}")
