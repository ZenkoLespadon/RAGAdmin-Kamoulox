import os



def fileOrFolder(path:str):
# Vérifier si le chemin est un dossier
    if os.path.isdir(path):
        print(f"{path} est un dossier.")
    # Vérifier si le chemin est un fichier
    elif os.path.isfile(path):
        print(f"{path} est un fichier.")
    else:
        print(f"{path} n'est ni un fichier ni un dossier.")

if __name__ == "__main__":

    tab = ["./test","files/Subject1","files/Subject1/test.txt"]
    for path in tab:
        fileOrFolder(path)

