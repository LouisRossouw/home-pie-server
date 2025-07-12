from django.shortcuts import render
from rest_framework import status
from drf_social_oauth2.views import TokenView as DRFSocialTokenView
from oauth2_provider.models import AccessToken, RefreshToken
from rest_framework.response import Response
from .serializers import CustomTokenSerializer
from rest_framework.permissions import AllowAny
from .serializers import CustomUserSerializer
from user.models import User
from shared.utils.printouts.views.printout_users import printout_CustomUserCreate
from rest_framework.views import APIView

# Manual log in

F = str(__name__)
CUC = "CustomUserCreate"


class CustomTokenView(DRFSocialTokenView):
    """ Sign in with the manual auth """

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # data = request.data

        if response.status_code == 200:
            token_data = response.data
            access_token = token_data.get('access_token')
            if access_token:
                try:
                    token_obj = AccessToken.objects.get(token=access_token)
                    custom_response_data = CustomTokenSerializer(token_obj).data  # nopep8
                    custom_response_data.update(token_data)

                    return Response(custom_response_data)
                except AccessToken.DoesNotExist:
                    return Response({'error': 'Token not found'}, status=404)
        return response


class CustomUserCreate(APIView):
    """ Create account """

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, format='json'):
        data = request.data

        email = data.get("email", "").lower()
        username = data.get("username", "").lower()

        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            error = False
            email_exists = User.objects.filter(email=email).exists()
            username_exists = User.objects.filter(
                username=username).exists()

            if email_exists:
                error = {'email': 'Email already being used'}
            if username_exists:
                error = {'username': 'Username already being used'}
            if username_exists and email_exists:
                error = {
                    'email': 'Email already being used',
                    'username': 'Username already being used'
                }

            if error == False:
                user = serializer.save()
                printout_CustomUserCreate(F, CUC, user)
                if user:
                    json = serializer.data
                    json['user_id'] = user.id

                    # BotNot.send_ADMIN_notification(new_user_format(username, 'Manual signup'))  # nopep8
                    return Response(json, status=status.HTTP_201_CREATED)

            else:
                print('Error:', error)
                return Response(error, status=status.HTTP_409_CONFLICT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
