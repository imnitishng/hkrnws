from django.db.models.expressions import RawSQL
from hkrnws.accounts.models import User
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError


class UserRegistrationSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
          'password': {'write_only': True},
		}

    def validate_username(self, value):
        if len(value) <= 6:
            raise ValidationError('Username must be greater than 6 charachters.', code=status.HTTP_400_BAD_REQUEST)
        return value

    def	save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            password=self.validated_data['password']
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise ValidationError('Passwords must match.', code=status.HTTP_400_BAD_REQUEST)
        
        user.save()
        return user