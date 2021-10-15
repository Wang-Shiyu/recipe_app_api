from django.contrib.auth import get_user_model, authenticate
# django helper command for working with authentication system
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users objecy"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

        # validated_data will contain all of the data that was passed into
        # our serializer which would be the JSON data that was made in the
        # HTTP POST
    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    # validator checking inputs are correct
    # based off the default token serializer
    def validate(self, attrs):
        """Validate and authenticate the user"""
        # attrs(dict) is every fields makes up the serializer
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            # Access the context of the request
            # This Serializer class will be passed into view set
            # Restframework view set will pass the context into the serializer
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unbale to authenticate with provided credentials')
            # restframework will handle this error and send 400 response
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
