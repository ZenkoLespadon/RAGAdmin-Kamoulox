#!/bin/bash

# Lire le message du commit
COMMIT_MSG=$(git log -1 --pretty=%B | xargs)

# Extraire l'ID du commit
COMMIT_ID=$(git log -1 --pretty=%h)

# Vérifier si le commit message n'est pas vide
if [ -z "$COMMIT_MSG" ]; then
    echo "Erreur: Le message du commit est vide."
    exit 1
fi

# Extraire le type et la description du commit (ex: feat: nouvelle feature)
TYPE=$(echo "$COMMIT_MSG" | cut -d: -f1 | xargs)
DESCRIPTION=$(echo "$COMMIT_MSG" | cut -d: -f2 | xargs)

# Vérifier que le type et la description ne sont pas vides
if [ -z "$TYPE" ] || [ -z "$DESCRIPTION" ]; then
    echo "Erreur: Le type ou la description du commit est vide."
    exit 1
fi

# Déterminer le type du commit pour Towncrier (feature, bugfix, etc.)
case $TYPE in
    feat)
        FRAGMENT_TYPE="feature"
        ;;
    fix)
        FRAGMENT_TYPE="bugfix"
        ;;
    docs)
        FRAGMENT_TYPE="doc"
        ;;
    style)
        FRAGMENT_TYPE="style"
        ;;
    refactor)
        FRAGMENT_TYPE="refactor"
        ;;
    perf)
        FRAGMENT_TYPE="performance"
        ;;
    test)
        FRAGMENT_TYPE="test"
        ;;
    chore)
        FRAGMENT_TYPE="chore"
        ;;
    *)
        FRAGMENT_TYPE="misc"
        ;;
esac

# Vérifier si le dossier changelog.d existe, sinon le créer
if [ ! -d "changelog.d" ]; then
    mkdir changelog.d
fi

# Créer le fichier de fragment dans changelog.d avec l'ID du commit
FRAGMENT_FILE="changelog.d/${COMMIT_ID}.${FRAGMENT_TYPE}"

# Écrire la description du commit dans le fichier de fragment
echo "$DESCRIPTION ([$COMMIT_ID](https://github.com/SaitamTheBest/RAGAdmin/commit/$COMMIT_ID))" > "$FRAGMENT_FILE"

echo "Fragment créé: $FRAGMENT_FILE"
