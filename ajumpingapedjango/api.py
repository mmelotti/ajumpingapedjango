
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDict
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework import parsers
from rest_framework import renderers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import DestroyAPIView, GenericAPIView, ListAPIView, ListCreateAPIView, UpdateAPIView, CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from ajumpingapedjango.serializers import ScoreSerializer, CreateUserSerializer, SavegameSerializer
from ajumpingapedjango.models import Score, Savegame

class ScoreAPI(ListCreateAPIView):
    #authentication_classes = (authentication.TokenAuthentication,)
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    
    def filter_queryset(self, queryset):
        return queryset.order_by('-score')[0:5]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

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
