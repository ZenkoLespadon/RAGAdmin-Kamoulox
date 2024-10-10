#!/bin/bash

# Lire le message du commit
COMMIT_MSG=$(git log -1 --pretty=%B)

# Extraire le type et la description du commit (ex: feat: nouvelle feature)
TYPE=$(echo "$COMMIT_MSG" | cut -d: -f1)
DESCRIPTION=$(echo "$COMMIT_MSG" | cut -d: -f2 | xargs)

# Générer un nom unique pour le fragment
FRAGMENT_NAME=$(date +"%Y%m%d%H%M%S")

# Déterminer le type du commit pour Towncrier (feature, bugfix, etc.)
if [[ $TYPE == "feat" ]]; then
    FRAGMENT_TYPE="feature"
elif [[ $TYPE == "fix" ]]; then
    FRAGMENT_TYPE="bugfix"
else
    FRAGMENT_TYPE="misc"
fi

# Créer le fichier de fragment dans changelog.d
FRAGMENT_FILE="changelog.d/${FRAGMENT_NAME}.${FRAGMENT_TYPE}"

# Écrire la description du commit dans le fichier de fragment
echo "$DESCRIPTION" > "$FRAGMENT_FILE"

echo "Fragment créé: $FRAGMENT_FILE"
