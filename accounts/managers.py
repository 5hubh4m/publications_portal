from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        """
        Create a user object given an Email and Password.
        """

        if not email:
            raise ValueError('Email must be set.')

        user = self.model(
            email=self.normalize_email(email),
            is_active=True,
            is_staff=False,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(
            email=email,
            is_superuser=True,
            is_staff=True,
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)

        return user
