#!/bin/bash

# Générer le changelog à partir des fragments avec Towncrier
towncrier build --yes

# Ajouter le changelog mis à jour dans le commit
git add CHANGELOG.md
git commit --amend --no-edit
