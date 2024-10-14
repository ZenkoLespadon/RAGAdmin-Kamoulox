#!/bin/bash

# Récupérer la dernière version à partir du dernier tag Git
LAST_VERSION=$(git describe --tags $(git rev-list --tags --max-count=1))

# Vérifier si un tag a été trouvé
if [ -z "$LAST_VERSION" ]; then
    echo "Erreur : Aucun tag Git trouvé. Assurez-vous d'avoir un tag versionné."
    exit 1
fi

# Générer le changelog à partir des fragments avec la version récupérée
towncrier build --version "$LAST_VERSION"

# Ajouter le changelog mis à jour dans le commit
git add CHANGELOG.md

# Amender le commit pour inclure le changelog sans changer le message
git commit --amend --no-edit

echo "Changelog généré pour la version : $LAST_VERSION"
