import secrets


# Génère un ID de vanité
def generate_vanity(min_length, max_length):
    length = secrets.choice(range(min_length, max_length))
    choices = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRTSUVWXYZ1234567890"
    vanity = ""

    for i in range(0, length):
        vanity += choices[secrets.choice(range(0, len(choices)))]
    return vanity


# Génère un ID de vanité unique
def generate_unique_vanity(min_length, max_length, model):
    vanity = generate_vanity(min_length, max_length)

    if model.objects.filter(slug=vanity).exists():
        return generate_unique_vanity(min_length, max_length, model)
    return vanity
