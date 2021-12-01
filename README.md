# thisappiscalleddrown

## Documentation

Si vous voulez l'essayer: _Prend en compte que vous savez faire ce genre de choses, si vous avez un problème, n'hésitez pas à checker sur StackOverflow_.

1. Cloner cette repository.
2. Créer une database nommée `thisappiscalleddrown` dans localhost (Avec wamp ou xampp, il faut installer les timezones).
3. `pip install -r requirements.txt` dans un venv.
4. Créer une copie de `.env.example` et la nommer `.env`, remplir les données comme nécessaire.
5. `python manage.py makemigrations accounts`.
6. `python manage.py makemigrations thisappiscalleddrown`.
7. `python manage.py makemigrations`.
8. `python manage.py migrate`.
9. `python manage.py loaddata ./fixtures/fixtures.json`.
10. `cd thisappiscalleddrown/static/vendor`.
11. `npm install`.
12. Générer le CSS à partir du SCSS, en utilisant un compilateur.
