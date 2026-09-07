from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Read-only view of a user — used in login response & employee list."""

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'phone', 'role', 'is_active', 'created_at']


class CreateEmployeeSerializer(serializers.ModelSerializer):
    """Used by the admin to create a new employee account."""

    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'name', 'email', 'phone']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(role=User.EMPLOYEE, **validated_data)
        user.set_password(password)
        user.save()
        return user
