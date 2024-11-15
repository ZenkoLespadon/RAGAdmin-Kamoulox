import os



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

def replaceFirstFolder(path:str,fileName:str) -> str :
    path = os.path.normpath(path)
    dossiers = path.split(os.sep)
    print(len(dossiers))

    if dossiers[0] != ".":
        dossiers[0] = fileName
    return os.path.join(*dossiers)

if __name__ == "__main__":

    tab = ["./test","files/Subject1","files/Subject1/test.txt"]
    for path in tab:
        res = delFileOfPath(path)
        print("path = ",res, " new path = ",replaceFirstFolder(res,"docs"))


