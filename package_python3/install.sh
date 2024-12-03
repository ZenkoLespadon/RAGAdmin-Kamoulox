#!/bin/bash

# Demander les privilèges administrateur au début
echo "Ce script nécessite des privilèges administratifs. Veuillez entrer votre mot de passe."
sudo -v  # Vérifie les privilèges sudo avant de continuer

# Si la commande échoue, le script s'arrête immédiatement
set -e

# Récupérer le répertoire où se trouve ce script
script_dir=$(dirname "$0")

# Sauvegarder le répertoire de travail actuel
actual_dir=$(pwd)

# Changer pour le répertoire où se trouve ce script
cd "$script_dir"

# Installer les paquets .deb pour python312
cd python312
echo "Installation des paquets pour python312..."
sudo dpkg -i *.deb
cd ..

# Installer les paquets .deb pour pip_install
cd pip_install
echo "Installation des paquets pour pip_install..."
sudo dpkg -i *.deb
cd ..

# Installer les paquets .deb pour python312_venv
#cd python312_venv
#echo "Installation des paquets pour python312_venv..."
#sudo dpkg -i *.deb
#cd ../..

# Créer et activer l'environnement virtuel Python
#echo "Création et activation de l'environnement virtuel Python..."
#python3 -m venv .
#source bin/activate

cd "$script_dir"
# Installer les paquets Python via pip
cd packages/chromadb
echo "Installation des paquets pour chroma..."
pip install *.whl
cd ../PyPDF2
echo "Installation des paquets pour PyPDF2..."
pip install *.whl
cd ../watchdog
echo "Installation des paquets pour watchdog..."
pip install *.whl

# Revenir au répertoire d'origine
cd "$actual_dir"
echo "Script terminé avec succès !"

# cd package_python3 && chmod a+x install.sh && ./install.sh

# cd python_package/packages/PyPDF2