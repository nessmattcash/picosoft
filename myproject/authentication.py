from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()

class EmailBackend(BaseBackend):
    """
    Authentification personnalisée basée sur l'email et le mot de passe.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        # Utilisation de l'email pour authentifier l'utilisateur
        try:
            # Rechercher l'utilisateur par email
            user = User.objects.get(email=username)
            # Vérifier si le mot de passe correspond
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
