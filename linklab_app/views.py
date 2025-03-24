from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .middlewares import google_auth
from. serializers import UserProfileSerializer
from linklab_app.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status as http_status
from rest_framework import status
from django.utils import timezone
from django.shortcuts import get_object_or_404
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


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import ShortenedURL
# from .utils import generate_short_code

# Create Short URL
@api_view(['POST', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated])
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

        short_code = custom_url if custom_url else google_auth.generate_unique_referral_code(number)
        
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
            urls = ShortenedURL.objects.filter(email=request.user.email)
        data = []
        for url in urls:
            data.append({
                "id": url.id,
                "original_url": url.original_url,
                "short_url": url.short_code,
                "custom_url": url.custom_url or "",
                "user_id": url.email,
                "title": url.title
            })
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        urls = ShortenedURL.objects.filter(id=request.GET.get('id'))
        urls.delete()
        return Response({"msg": "All Short URLs deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    


# Get Short URL
@api_view(['GET'])
def get_short_url(request, short_code):
    url_entry = get_object_or_404(ShortenedURL, short_code=short_code)
    return Response({
        "id": url_entry.id,
        "original_url": url_entry.original_url,
        "short_url": url_entry.short_code,
        "custom_url": url_entry.short_code,
        "user_id": url_entry.user_id,
        "title": url_entry.title
    })


# Update Short URL
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_short_url(request, short_code):
    url_entry = get_object_or_404(ShortenedURL, short_code=short_code, user_id=request.user.id)
    data = request.data
    
    url_entry.title = data.get('title', url_entry.title)
    url_entry.original_url = data.get('original_url', url_entry.original_url)
    url_entry.save()

    return Response({"msg": "Short URL updated successfully"}, status=status.HTTP_200_OK)


# Delete Short URL
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_short_url(request, short_code):
    url_entry = get_object_or_404(ShortenedURL, short_code=short_code, user_id=request.user.id)
    url_entry.delete()
    return Response({"msg": "Short URL deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
