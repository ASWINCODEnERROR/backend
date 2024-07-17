from rest_framework import serializers
from .models import User  # Make sure this is your custom user model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'phone_number', 'sub_admin', 'roles')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            sub_admin=validated_data['sub_admin'],
            roles=validated_data['roles']
        )
        user.set_password(validated_data['password'])
        user.is_active = False  # User is inactive until email verification
        user.save()
        return user
