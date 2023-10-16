from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomerDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')
        

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')        


class UserLoggedInSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email')
        

class UserListSerializer(UserLoggedInSerializer):
    
    class Meta(UserLoggedInSerializer.Meta):
        fields = UserLoggedInSerializer.Meta.fields + ('is_active', 'is_staff', 'is_blocked')
        
       
class UserDisplaySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email')