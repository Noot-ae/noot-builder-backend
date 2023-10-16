from rest_framework import serializers
from user.tokens import CustomTokenObtainPairSerializer
from user.serializers import SignUpSerializer
from .models import Client, Domain
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from user.models import User
from django.db import IntegrityError


class ClientUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only = True, source="password", style={'input_type' : 'password'})
    password2 = serializers.CharField(write_only = True, style={'input_type' : 'password'})

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['password'] != attrs['password2']:
            raise ValidationError("password do not match each other", code="invalid_passwords")
        attrs.pop('password2')
        validate_password(attrs['password'])
        return attrs

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        extra_kwargs = {
            'schema_name' : {"read_only" : True}
        }


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'
        extra_kwargs = {
            'tenant' : {"required" : False}
        }


class TenantSerializer(serializers.ModelSerializer):
    THEME_CHOICES =( 
        ("commerce", "commerce"),
        ("legacy", "legacy"),
        ("market", "market"),
        ("oasis", "oasis"),
        ("cosmetics", "cosmetics")
    )
    
    domain = DomainSerializer(required=True)
    user = ClientUserSerializer(required=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs['username'] = attrs['user']['username']
        return attrs

    def create(self, validated_data : dict):
        user_data = validated_data.pop('user', {})
        domain_data = validated_data.pop('domain')
        
        tenant : Client = super().create(validated_data)
        tenant.activate()
        user_data = self.create_user(user_data)
        domain_data['tenant'] = tenant
        
        try:
            domain = self.create_domain(domain_data)
        except IntegrityError as e:
            raise ValidationError(f"{e}", code="invalid_domain_data")
        
        tenant.user = user_data
        tenant.domain = domain
        return tenant
    
    def create_user(self, data):
        self.user_instance = User.objects.create_superuser(data.pop('username'), **data)
        user_data = SignUpSerializer(instance=self.user_instance).data
        return user_data
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['access_token'] = str(CustomTokenObtainPairSerializer.get_token(self.user_instance).access_token)
        return data

    def create_domain(self, data):
        domain = Domain.objects.create(**data)
        return domain        


    class Meta:
        model = Client
        fields = (
            'id', 'schema_name', 'username', 'domain', 'user'
        )
        extra_kwargs = {
            'schema_name' : {"read_only" : True}
        }



class TenantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('is_enabled', 'allow_purchase')
        

class TenantOwnerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('allow_purchase', )
        

