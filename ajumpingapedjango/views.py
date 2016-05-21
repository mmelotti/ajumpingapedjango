

from django.shortcuts import render
from django.contrib.auth.models import User
from ajumpingapedjango.serializers import UserSerializer

def home_view(request):
    return render(request, 'home.html')

	
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer