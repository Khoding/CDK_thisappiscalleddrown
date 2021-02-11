from django.test import TestCase

from accounts.models import CustomUser


class UserTestCase(TestCase):
    def setup(self):
        CustomUser.objects.create(
            email="rosier@test.com",
            first_name="Adrien Matthieu",
            last_name="Rossier",
            password="Pa$$w0rd",
            bio="Zzzzzzzzzzz...",
            locality="Bienne",
            npa=2134,
            address="Rue du sommeil 12",
            tel_m="+41 077 123 32 12",
            tel_p="+41 069 696 96 96"
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
            tel_p="+41 078 982 12 32",
            tel_m="+41 076 213 32 41"
        )