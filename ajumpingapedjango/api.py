
from django.core import serializers
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDict
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework import parsers
from rest_framework import renderers
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import DestroyAPIView, GenericAPIView, ListAPIView, ListCreateAPIView, UpdateAPIView, CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from ajumpingapedjango.serializers import ScoreSerializer, CreateUserSerializer, SavegameSerializer, GameBalanceSerializer
from ajumpingapedjango.models import Score, Savegame, GameBalance
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json


class MyScoreAPI(APIView):
    """
    Return Score
    """
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):    
        return Response('content')
		
    def post(self, request, format=None):    
        return Response('contenpostt')

		

class GameBalanceAPI(APIView):
    #authentication_classes = (authentication.TokenAuthentication,)
    #permission_classes = (permissions.AllowAny,)
    """
    Return Game Balance Parameters
    """
	
    def get(self, request, format=None): 
        #serialized_obj = serializers.serialize('json', [ GameBalance.objects.all()[:1].get(), ])
        obj = GameBalance.objects.all()[:1].get()
        return Response({'playerHorizontalSpeed': obj.playerHorizontalSpeed, 'brainSpawDeltaY': obj.brainSpawDeltaY, 'bananaSpawDeltaY': obj.bananaSpawDeltaY, 'jumpForce': obj.jumpForce, 'startJumpForce': obj.startJumpForce})
     
class ScoreAPI(ListCreateAPIView):
    #authentication_classes = (authentication.TokenAuthentication,) no need
    #permission_classes = (permissions.AllowAny,)    no need
	
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
	
    def filter_queryset(self, queryset):
        return queryset.order_by('-score')[0:5]
	
		
class ScorAPI(ListCreateAPIView):

	def responder(request):
	#this works, too!
		return HttpResponse('Hello world')		
		
class UserAPI(DestroyAPIView, CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    def perform_destroy(self, instance):
        user = User.objects.get(username=self.request.data['username'], email=self.request.data['email'])
        if user.check_password(self.request.data['password']) is False:
            return Response('You are not authorized to do that.', status=status.HTTP_401_UNAUTHORIZED)
        instance.delete()

class GetAuthToken(GenericAPIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

class SavegameAPI(ListCreateAPIView, UpdateAPIView, DestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SavegameSerializer

    def get_queryset(self):
        qs = Savegame.objects.all().filter(owner=self.request.user)
        return qs
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
		
    def list(self, request, *args, **kwargs):
        savegameType = ''
        if 'SavegameType' in self.request.data: 
            savegameType = self.request.data['SavegameType']

        instance = self.get_queryset().filter(type=savegameType)
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)
