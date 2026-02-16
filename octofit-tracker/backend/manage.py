#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octofit_tracker.settings')
    # Gestion de l'absence de la base MongoDB : avertissement mais ne bloque pas le serveur
    try:
        from django.core.management import execute_from_command_line
        # Test rapide de connexion à la base uniquement pour les commandes qui nécessitent la base
        if len(sys.argv) > 1 and sys.argv[1] in ['runserver', 'shell', 'test']:
            try:
                from django.db import connections
                from django.db.utils import OperationalError
                db_conn = connections['default']
                db_conn.cursor()  # Tentative de connexion
            except Exception as e:
                print(f"\033[93m[AVERTISSEMENT] La base de données n'est pas accessible : {e}\033[0m")
                print("Le serveur démarre quand même, mais les endpoints dépendant de la base échoueront.")
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
