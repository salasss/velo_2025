# CI/CD Pipeline - Velo 2025

Ce projet utilise GitHub Actions pour l'intégration continue et le déploiement continu.

## Workflows Activés

### 1. **Python Tests** (`.github/workflows/tests.yml`)
Déclenché à chaque `git push` sur les branches:
- `main`
- `develop`
- `feature/*`

**Actions:**
- ✅ Teste avec Python 3.10, 3.11, 3.12
- ✅ Installe les dépendances
- ✅ Lance les tests avec `pytest`
- ✅ Génère un rapport de couverture
- ✅ Envoie la couverture à Codecov

### 2. **Docker Build** (`.github/workflows/docker-build.yml`)
Déclenché à chaque modification:
- `Dockerfile`
- `requirements.txt`

**Actions:**
- ✅ Construit l'image Docker
- ✅ Vérifie qu'elle se compile sans erreur

## Comment Ça Marche

1. Tu fais `git push` sur GitHub
2. GitHub Actions détecte le push
3. Les workflows s'exécutent automatiquement
4. Tu reçois un rapport: ✅ PASS ou ❌ FAIL

## Voir les Résultats

1. Va sur ton repo GitHub
2. Clique sur l'onglet **Actions**
3. Clique sur le dernier workflow
4. Vois les détails du test

## Ajouter Plus de Tests

Pour ajouter des tests:
1. Crée des fichiers dans `tests/` qui commencent par `test_`
2. Écris des fonctions qui commencent par `test_`
3. Les tests s'exécutent automatiquement au prochain push

Exemple:
```python
def test_something():
    assert 1 + 1 == 2
```

## Exécuter les Tests Localement

```bash
pip install pytest pytest-cov
pytest tests/ -v
```

## Statut Badge

Ajoute ce badge à ton README principal:

```markdown
[![Python Tests](https://github.com/YOUR-USERNAME/velo_2025/actions/workflows/tests.yml/badge.svg)](https://github.com/YOUR-USERNAME/velo_2025/actions)
```
