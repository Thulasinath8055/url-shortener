from django.contrib.auth.models import User
from rest_framework import serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Handles user registration.
    
    Key security principles:
    1. Password is write_only: it is accepted but NEVER returned.
    2. We validate that email is unique.
    3. We use create_user() which hashes the password with PBKDF2.
    """

    # write_only=True: the password field appears in input schema (Swagger),
    # but is stripped from every response.
    # min_length=8: enforces a basic strength rule at the API layer.
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}  # Renders as a password input in browsable API
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'email': {'required': True}  # Django's User model allows blank email by default
        }

    # -------------------------------------------------------------------------
    # VALIDATION
    # -------------------------------------------------------------------------

    def validate_email(self, value: str) -> str:
        """
        Custom validator for the 'email' field.
        Django's default User model does NOT enforce unique emails.
        We add that check here to prevent duplicate accounts.
        """
        normalized_email = value.lower().strip()
        if User.objects.filter(email=normalized_email).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return normalized_email

    # -------------------------------------------------------------------------
    # CREATE
    # -------------------------------------------------------------------------

    def create(self, validated_data: dict) -> User:
        """
        Create and return a new User instance, with the password properly hashed.
        
        CRITICAL: Never use User.objects.create() for passwords.
        create_user() automatically hashes the password using PBKDF2 with SHA256.
        """
        user = User.objects.create_user(**validated_data)
        return user