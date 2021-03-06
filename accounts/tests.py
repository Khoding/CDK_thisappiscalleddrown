from django.test import TestCase

from accounts.models import CustomUser


class UserTestCase(TestCase):
    """
    Classe de test des utilisateurs.
    """

    def setup(self):
        """
        Fonction de setup.
        """

        CustomUser.objects.create(
            email="rosier@test.com",
            first_name="Adrien Matthieu",
            last_name="Rossier",
            password="Pa$$w0rd",
            bio="...",
            locality="Bienne",
            npa=2134,
            address="Rue du sommeil 12",
            tel_mobile="+41 077 123 32 12",
            tel_pro="+41 069 696 96 96"
        )

        CustomUser.objects.create(
            email="monke@test.com",
            first_name="Monkey",
            last_name="Boi",
            password="Pa$$w0rd",
            bio="Ouh ouh ouh ! Ah ah !",
            locality="Les Breuleux",
            npa=2143,
            address="Rue de la banane 20",
            tel_pro="+41 078 982 12 32",
            tel_mobile="+41 076 213 32 41"
        )
