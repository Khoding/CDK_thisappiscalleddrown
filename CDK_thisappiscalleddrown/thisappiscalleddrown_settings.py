"""
Paramètres de configuration exclusifs à l'application thisappiscalleddrown.
"""

# Nombre maximum d'invitations par utilisateur.
MAX_INVITATION_NUMBER_BY_USER = 25

# Contributeurs au projet
CONTRIBUTORS = [
    {
        "name": "Julien Rutscho",
        "citation": "I am Vengeance ! I am the Night ! I am Batman !!!",
        "email": "julien.rutscho@ceff.ch",
        "year_when_contr": 3,
        "contribs": [
            {
                "name": '"Initiateur" du projet refonte',
                "desc": "A proposé Django, ce qui a mené à la refonte",
                "credits": 75,
            },
            {"name": "Développeur", "desc": "A contribué au code", "credits": 200},
            {"name": "Designer", "desc": "A contribué au design", "credits": 75},
            {"name": "Maniac", "desc": "Se plaignait de tout ce qui n'était pas parfait", "credits": 100},
        ],
        "aka": "Le parfois très efficace... seulement parfois... vraiment parfois...",
    },
    {
        "name": "Nicolas Schwab",
        "citation": "3 glocks 20 blocks",
        "icon": "fas fa-leaf",
        "email": "nicolas.schwab@ceff.ch",
        "year_when_contr": 4,
        "contribs": [
            {
                "name": "Plus grand contributeur",
                "desc": "A apporté la contribution la plus conséquente au projet",
                "credits": 500,
            },
            {"name": "Designer Principal", "desc": "A créé le design", "credits": 250},
            {"name": "Développeur", "desc": "A contribué au code", "credits": 200},
        ],
        "aka": "Le trop efficace",
    },
    {
        "name": "Lorenzo Di Benedetto",
        "citation": "Galaxy brain",
        "icon": "fas fa-brain",
        "email": "lorenzo.dibenedetto@ceff.ch",
        "year_when_contr": 4,
        "contribs": [
            {"name": "Développeur", "desc": "A contribué au code", "credits": 200},
            {"name": "Créateur des APIs", "desc": "A créé les APIs", "credits": 250},
            {"name": "Designer", "desc": "A contribué au design", "credits": 50},
        ],
        "aka": "L'Orakle du Python",
    },
    {
        "name": "Adrien Matthieu Rossier",
        "citation": "Toujours avoir le choix LOL",
        "icon": "fas fa-torii-gate",
        "email": "adrienmatthieu.rossier@ceff.ch",
        "year_when_contr": 4,
        "contribs": [
            {
                "name": "Migrations des données depuis l'ancien site",
                "desc": "A créé le script de migration (2x)",
                "credits": 250,
            },
            {"name": "Développeur", "desc": "A contribué au code", "credits": 100},
        ],
        "aka": "La belle au bois dormant",
    },
]
