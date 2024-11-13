# Commit

## Types de `commit`

Voici les différents types de commit à respecter à chaque commit : 

<div align="center">

| Parameter | Type        | Description                                       |
| :-------- | :---------- | :------------------------------------------------ |
| `feat`    | `FEATURE`   | Ajout d'une nouvelle fonctionnalité               |
| `fix`     | `BUGFIX`    | Correction d'un bug                               |
| `docs`    | `DOCUMENTATION` | Modifications liées à la documentation          |
| `style`   | `STYLE`     | Modifications de style (formatage, espaces, etc.) |
| `refactor`| `REFACTORING`| Refactorisation du code sans ajout de fonctionnalité |
| `perf`    | `PERFORMANCE`| Améliorations de la performance                    |
| `test`    | `TEST`      | Ajout ou modification de tests                    |
| `chore`   | `CHORE`     | Tâches de maintenance (outils, configurations, etc.) |
| `misc`    | `MISCELLANEOUS`| Divers, autres changements qui ne correspondent pas aux catégories ci-dessus |

</div>

## Exemples de messages de commit

Voici des exemples pour chaque type de commit :

<div align="center">

| Type       | Exemple de message de commit                                |
| :--------- | :----------------------------------------------------------- |
| **feat**   | `feat: add user authentication feature`                      |
| **fix**    | `fix: resolve issue with login validation`                   |
| **docs**   | `docs: update API documentation for user endpoints`          |
| **style**  | `style: reformat code and fix indentation`                   |
| **refactor**| `refactor: simplify authentication logic`                   |
| **perf**   | `perf: optimize database queries for faster response time`   |
| **test**   | `test: add unit tests for authentication module`             |
| **chore**  | `chore: update dependencies and configure build tool`        |
| **misc**   | `misc: minor changes and clean up`                           |

</div>

Ces exemples permettent de mieux comprendre comment rédiger un message de commit suivant la convention établie.
## Comment bien `commit` ?

Pour un bon usage des commits et des versions, voici les étapes à suivre :

### 1. Commiter en local
Tout d'abord, assurez-vous de tout **commit** localement en respectant les conventions de commit. Utilisez les types de commits appropriés (comme `feat`, `fix`, etc.) pour décrire clairement les changements apportés.

Par exemple :
```bash
git add .
git commit -m "feat: add user authentication feature"
```

### 2. Utiliser Semantic Versioning 2.0.0
Une fois que vous avez terminé le développement d'une fonctionnalité ou une série de corrections, avant de pousser (`push`) vos changements sur le dépôt distant, il faut créer un nouveau `tag` en suivant le principe du [Semantic Versioning](https://semver.org/) (versionnement sémantique).

Semantic Versioning 2.0.0 suit le format `MAJOR.MINOR.PATCH` :

- **`MAJOR`**: une version majeure introduit des changements incompatibles avec les versions précédentes.
- **`MINOR`**: une version mineure ajoute des fonctionnalités tout en restant rétrocompatible.
- **`PATCH`**: une version de correction corrige des bugs, sans modifier l'API ou les fonctionnalités.
Par exemple, si vous venez d'ajouter une nouvelle fonctionnalité compatible avec la version précédente, tu dois incrémenter la version `MINOR`.

Création d'un tag avec version sémantique :

```bash
git tag v1.1.0
```
### 3. Pousser les changements et le tag
Une fois le tag créé, tu peux pousser les commits et le tag vers le dépôt distant :

```bash
git push origin main
git push origin v1.1.0
```