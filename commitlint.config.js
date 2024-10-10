module.exports = {
    // Configuration des types de commits autorisés
    extends: ['@commitlint/config-conventional'],
    rules: {
      // Désactiver la vérification de la casse du sujet
      'subject-case': [0, 'never', ['sentence-case', 'start-case', 'pascal-case', 'upper-case']],
      
      // Optionnel : s'assurer que le message de commit contient un type valide
      'type-enum': [
        2,
        'always',
        [
          'feat',    // pour les nouvelles fonctionnalités
          'fix',     // pour les corrections de bugs
          'docs',    // pour la documentation
          'style',   // pour les modifications de style (espace, formatage, etc.)
          'refactor',// pour les refactorisations
          'perf',    // pour les améliorations de performance
          'test',    // pour les tests ajoutés ou modifiés
          'chore',   // pour les tâches de maintenance
        ],
      ],
      // Optionnel : s'assurer que le sujet du commit ne dépasse pas 72 caractères
      'header-max-length': [2, 'always', 72],
    },
  };
  