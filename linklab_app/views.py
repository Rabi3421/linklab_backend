import requests
from .models import ShortenedURL
from django.utils import timezone
from rest_framework import status
from .middlewares import google_auth
from rest_framework.response import Response
from linklab_app.models import User, URLVisit
from. serializers import UserProfileSerializer
from django.shortcuts import get_object_or_404
from django.utils.timezone import now, timedelta
from django.http import HttpResponseRedirect, Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.exceptions import TokenError


# Create your views here.
@api_view(['GET'])
def hello_django(request):
    return Response({"message": "LinkLab! me aapka swagat hai!"})

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(["POST"])
def social_media_login_views(request):
    try:
        data = request.data
        user_data = {
            "email" : data["email"],
            "name" : data["name"],
            "profile_image" : data["picture"],
            # "db_name" : db_name_with_uuid
        }
        email = data["email"]
        # print("user_info", user_info)
        user = User.objects.filter(email=email).first()
                
        if not user:
            user_data["is_active"] = True
            user_data["password"] = ""
            user_data['referrer_by'] = ""
            user_data["phone"] = ""
            user_data["gender"] = ""
            user_data["dob"] = ""
            user_data["role"] = "user"
            user_data["special_offers"] = 0
            user_data["tc"] = "False"
            user_data["referral_code"] = f"Linklab_{google_auth.generate_unique_referral_code(number=8)}"
            user = google_auth.create_users(user_data)
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)
        else:
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            if not user.is_active:
                user.is_active = True  # Set is_activate to True
                user.save(update_fields=['is_active'])     
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Login Successful'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": "Social Media Login Failed"})
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    try:
        if request.method == 'GET':
            # print("email",request.user)
            serializer = UserProfileSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        # logger.error(f"error occured during user login && error is: {e}")
        return Response({'error': 'Profile Retrieval Failure'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user_info_views(request):
    try:
        data = request.data
        profileid = request.user.id

        # Get the user profile to be updated
        profile = get_object_or_404(User, id=profileid)
        # Update only provided fields
        allowed_fields = ['name', 'phone', 'city', 'country', 'dob', 'gender']
        for field in allowed_fields:
            if field in data:
                setattr(profile, field, data[field])
        profile.save()
        return Response({"msg": "Profile successfully updated"}, status=status.HTTP_202_ACCEPTED)
    except Exception as error:
        return Response({"error": f"Error during profile update: {str(error)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def user_logout_view(request):
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token is None:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken(refresh_token)
        token.blacklist()  # This method blacklists the token, invalidating it.

        return Response({'msg': 'Logout Successful'}, status=status.HTTP_200_OK)
    except TokenError as e:
        return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# from .utils import generate_short_code
from collections import Counter
# Create Short URL
@api_view(['POST', 'GET', 'DELETE'])
# @permission_classes([IsAuthenticated])
def create_short_url_views(request):
    if request.method == 'POST':
        data = request.data
        original_url = data.get('original_url')
        custom_url = data.get('custom_url')
        title = data.get('title', 'Untitled')
        qr = data.get('qr', None)
        number = 8
        if not original_url:
            return Response({'error': 'Original URL is required'}, status=status.HTTP_400_BAD_REQUEST)

        # short_code = custom_url if custom_url else google_auth.generate_short_url()
        short_code = google_auth.generate_short_url()
        
        if ShortenedURL.objects.filter(short_code=short_code).exists():
            return Response({'error': 'Custom URL already exists'}, status=status.HTTP_400_BAD_REQUEST)

        shortened_url = ShortenedURL.objects.create(
            email=request.user.email,
            original_url=original_url,
            short_code=short_code,
            custom_url=custom_url,
            title=title,
            qr=qr
        )

        return Response({
            "id": shortened_url.id,
            "original_url": shortened_url.original_url,
            "short_url": shortened_url.short_code,
            "custom_url": custom_url or "",
            "user_id": shortened_url.email,
            "title": shortened_url.title
        }, status=status.HTTP_201_CREATED)
    
    elif request.method == 'GET':
        url_id = request.GET.get('id')
        if url_id:
            urls = ShortenedURL.objects.filter(id=url_id)
        else:
            urls = ShortenedURL.objects.filter(email= request.user.email)
        data = []
        for url in urls:
            visits = URLVisit.objects.filter(short_url_id=url.id)
            visit_count = visits.count()

            # Extract country names from location field
            countries = []
            for visit in visits:
                if visit.location:
                    parts = visit.location.split(',')
                    if parts:
                        country = parts[-1].strip()
                        if country:
                            countries.append(country)

            # Find the most common country (top_country)
            top_country = ""
            if countries:
                top_country = Counter(countries).most_common(1)[0][0]
            data.append({
                "id": url.id,
                "original_url": url.original_url,
                "short_url": url.short_code,
                "custom_url": url.custom_url or "",
                "user_id": url.email,
                "title": url.title,
                "total_clicks": visit_count,
                "top_country": top_country,
                "created_at": url.created_at
            })
        return Response(data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        urls = ShortenedURL.objects.filter(id=request.GET.get('id'))
        urls.delete()

        return Response({"msg": "All Short URLs deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    




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
    """Fetches location data using IP address."""
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}')
        data = response.json()
        return (
            f"{data.get('city', 'Unknown')}, {data.get('region', 'Unknown')}, {data.get('country', 'Unknown')}",
            data.get('lat'),
            data.get('lon')
        )
    except Exception:
        return "Unknown", None, None

def get_device_type(user_agent):
    """Detect if the user is on Mobile or Desktop"""
    user_agent = user_agent.lower()
    if 'mobile' in user_agent:
        return 'Mobile'
    elif 'tablet' in user_agent:
        return 'Tablet'
    else:
        return 'Desktop'


@api_view(['GET'])
def redirect_to_original(request, short_code):
    try:
        # start_time = datetime.now()
        url_entry = get_object_or_404(ShortenedURL, short_code=short_code)
        ip = get_client_ip(request)
        # ip = "209.163.239.30"
        location, latitude, longitude = get_location(ip)
        user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')
        device_type = get_device_type(user_agent)
        referrer = request.META.get('HTTP_REFERER', '')
        
        # Check for a recent visit from this IP & User-Agent within 5 seconds
        recent_visit = URLVisit.objects.filter(
            short_url=ShortenedURL.objects.get(short_code=short_code),
            ip_address=ip,
            user_agent=user_agent,
            timestamp__gte=now() - timedelta(seconds=5)
        ).exists()
        if recent_visit:
            return HttpResponseRedirect(url_entry.original_url)
        # if recent_visit:
        track = URLVisit.objects.create(
            short_url=ShortenedURL.objects.get(short_code=short_code),
            ip_address=ip,
            location=location,
            latitude=latitude,
            longitude=longitude,
            user_agent=user_agent,
            device_type=device_type,
            browser="Unknown",
            os="Unknown",
            referrer=referrer
        )
        # Fire tracking signal asynchronously
        # track_redirect_signal.send(sender=None, request=request, short_code=short_code)
        # end_time = datetime.now()
        # time_taken = (end_time - start_time).total_seconds()
        return HttpResponseRedirect(url_entry.original_url)
    except ShortenedURL.DoesNotExist:
        return Response({"error": "Short URL not found"}, status=404)
    except:
        raise Http404("Short URL not found")


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_tracking_views(request):
    try:
        short_code = request.GET.get('short_code')
        if not short_code:
            return Response({'error': 'Short code is required'}, status=status.HTTP_400_BAD_REQUEST)

        url = get_object_or_404(ShortenedURL, short_code=short_code)
        visits = URLVisit.objects.filter(short_url=url).order_by('-timestamp')
        data = []
        for visit in visits:
            data.append({
                'timestamp': visit.timestamp,
                'ip_address': visit.ip_address,
                'location': visit.location,
                'user_agent': visit.user_agent,
                'device_type': visit.device_type,
                'browser': visit.browser,
                'os': visit.os,
                'referrer': visit.referrer,
                'latitude': visit.latitude,
                'longitude': visit.longitude

            })
        return Response(data, status=status.HTTP_200_OK)
    except:
        return Response({'error': 'Tracking data not found'}, status=status.HTTP_404_NOT_FOUND)