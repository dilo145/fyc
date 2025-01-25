# FYC

Ce document explique comment configurer et lancer le projet FYC.

## Prérequis

Avant de commencer, assurez-vous d'avoir **Python** installé sur votre machine.

### Vérification de l'installation Python

1. Téléchargez Python depuis [python.org](https://www.python.org/) si ce n'est pas déjà fait
2. Vérifiez votre installation en ouvrant un terminal et en exécutant :

```bash
python --version
```

ou selon votre configuration :

```bash
python3 --version
```

## Installation

### Configuration de l'environnement virtuel (recommandé)

Il est fortement recommandé d'utiliser un environnement virtuel pour éviter les conflits entre les dépendances de différents projets.

1. Création de l'environnement virtuel :

```bash
# Windows
python -m venv venv

# Linux/MacOS
python3 -m venv venv
```

2. Activation de l'environnement virtuel :

```bash
# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Linux/MacOS
source venv/bin/activate
```

> **Note** : Votre invite de commande devrait maintenant afficher `(venv)` au début, indiquant que l'environnement virtuel est activé.

### Installation des dépendances

Une fois l'environnement virtuel activé, vous pouvez installer les dépendances :

#### Méthode 1 : Via requirements.txt (recommandée)

```bash
pip install -r requirements.txt
```

#### Méthode 2 : Installation manuelle

Si le fichier `requirements.txt` n'est pas disponible :

```bash
pip install arcade
```

> **Note** : Avec l'environnement virtuel activé, vous n'avez pas besoin d'utiliser `pip3`, `pip` suffit.

### Désactivation de l'environnement virtuel

Quand vous avez terminé de travailler sur le projet :

```bash
deactivate
```

## Lancement du jeu

Assurez-vous que l'environnement virtuel est activé, puis exécutez :

```bash
python main.py
```

## Support et aides

Si vous rencontrez des difficultés :

- Vérifiez que :
  - L'environnement virtuel est bien activé
  - Toutes les dépendances sont correctement installées
  - Vous utilisez la bonne version de Python
- Ouvrez une issue dans le dépôt du projet
- Contactez directement le développeur

---

Pour toute question supplémentaire, n'hésitez pas à nous contacter.
