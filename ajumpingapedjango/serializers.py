
from django.contrib.auth.models import User
from rest_framework import serializers, filters
from ajumpingapedjango.models import Score, Savegame, Snippet

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ('id', 'score', 'owner_name', 'updated')

		
		
class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')
		
		
class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save() 
        return user


class SavegameSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'updated', 'file', 'type')
        model = Savegame

