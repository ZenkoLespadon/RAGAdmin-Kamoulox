import os
from pathlib import Path


def fileOrFolder(path:str) -> str :
    """
        Fonction qui prend en paramette un chemin d'accès
    """
# Vérifier si le chemin est un dossier
    if os.path.isdir(path):
        #print(f"{path} est un dossier.")
        return "folder"
    # Vérifier si le chemin est un fichier
    elif os.path.isfile(path):
        #print(f"{path} est un fichier.")
        return "file"
    else:
        #print(f"{path} n'est ni un fichier ni un dossier.")
        return "unknow"

def delFileOfPath(path:str):
    return os.path.dirname(path)

def replace_backslashes(input_str: str) -> str:
    # Remplacer tous les antislashs par des slashs
    result = ""
    for letter in input_str:
        if letter == "\\" :
            result += "/"
        else:
            result += letter
    return result

def replaceFirstFolder(path:str,fileName:str) -> str :
    path = os.path.normpath(path)
    dossiers = path.split(os.sep)
    print(len(dossiers))

    if dossiers[0] != ".":
        dossiers[0] = "./" + fileName
    newPath=os.path.join(*dossiers)

    return  replace_backslashes(newPath)


def create_missing_directories(path: str) -> None:
    """
    Crée tous les répertoires manquants dans le chemin donné.

    :param path: Le chemin d'accès pour lequel les répertoires manquants doivent être créés.
    """

    path = os.path.normpath(path)
    folderPath = Path(os.path.dirname(path))
    folderPath.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":

    tab = ["./test","new/Subject1"]
    for path in tab:
        #res = delFileOfPath(path)
        #print("path = ",res, " new path = ",replaceFirstFolder(res,"docs"))
        create_missing_directories(path)


