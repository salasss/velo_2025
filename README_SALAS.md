# 🚴 Velo 2025 - Extension & Industrialisation

> **Auteur :** Salas Alkama
> **Statut :** ✅ Projet Complet + Extension DevOps

## 📝 Contexte du Projet

Ce dépôt contient ma réalisation du projet académique de simulation de vélos partagés.
J'ai finalisé l'ensemble des fonctionnalités requises :
* Implémentation des 4 approches de simulation (Basic, Serial, Parallel, Cluster).
* Génération des graphiques (`--plot`) pour l'analyse des résultats.
* Conteneurisation (Docker & Singularity).

**Au-delà du cahier des charges**, j'ai choisi d'appliquer des pratiques **DevOps** et **Data Engineering** pour transformer ce projet scolaire en une projet pour mon portfolio.

---

## 🚀 Synthèse des Contributions Supplémentaires (Bonus)

J'ai implémenté deux axes d'amélioration majeurs pour garantir la qualité et la reproductibilité du projet :

### 1️⃣ Pipeline CI/CD (GitHub Actions) 🔄
Pour garantir la fiabilité du code, j'ai mis en place une chaîne d'intégration continue (CI).

* **Tests Unitaires & d'Intégration :**
    * Création d'une suite de tests (`tests/`) qui valide la logique mathématique.
    * Vérification automatique de l'exécution des scripts dans chaque dossier (1, 2, 3) à chaque `git push`.
    * Configuration avancée de la CI pour installer les dépendances système (OpenMPI) avant les tests.
* **Validation Docker :**
    * Vérification automatique que le `Dockerfile` compile correctement.
* **Résultat :** Une "Green Build" ✅ qui assure que le projet est toujours fonctionnel.

### 2️⃣ Infrastructure as Code (Terraform / GCP) ☁️
J'ai conçu l'architecture pour déployer ce projet sur un environnement Google Cloud Platform (GCP).

* **Architecture :** Définition complète d'un réseau privé (VPC), d'un pare-feu et d'une VM de calcul optimisée.
* **Automatisation :** Utilisation d'un `startup-script` qui installe Docker, clone le dépôt et lance la simulation MPI automatiquement au démarrage de la machine.
* **État :** pas tester encore (trouvable dans dev)

---

## 📂 Organisation du Projet

Voici la structure du projet, mettant en évidence les ajouts DevOps :

```text
velo_2025/
├── .github/workflows/          # [BONUS] Pipelines CI/CD
│   ├── tests.yml               # Tests Python & MPI
│   └── docker-build.yml        # Test de build Docker
├── infra/                      # [BONUS] Infrastructure as Code (Terraform)
│   ├── main.tf
│   └── variables.tf
├── tests/                      # [BONUS] Suite de tests
│   ├── test_model.py           # Tests unitaires
│   └── test_integration.py     # Tests d'intégration
├── 1_basic_single_sim/         # Simulation simple
├── 2_serial_param_sweep/       # Balayage + Plotting
├── 3_parallel_local/           # HPC Local + Plotting
├── 4_cluster_slurm/            # Cluster SLURM
├── Dockerfile                  # Image Docker
├── velo_python_3.12.def        # Image Singularity
└── README_SALAS.md             # Ce fichier
```

---

## 🛠️ Guide d'Utilisation

### 1. Installation

```bash
git clone https://github.com/salasss/velo_2025.git
cd velo_2025
pip install -r requirements.txt
```

### 2. Lancer les Tests (Vérification du code)

```bash
# Lance toute la suite de tests (Unitaires + Intégration)
pytest tests/ -v
```

### 3. Exécuter une Simulation (Ex: MPI)

```bash
cd 3_parallel_local
mpirun -n 4 python run_mpi.py --params params.csv --out-dir results_mpi --plot
```

### 4. Déploiement Cloud (Terraform)

> **Note :** Nécessite un compte GCP actif avec les crédits disponibles.

```bash
cd infra
# Initialisation et validation
terraform init
terraform plan
# Déploiement
terraform apply
```

---

## Perspectives d'Évolution

Pour continuer l'industrialisation de ce projet, les prochaines étapes seraient :

### 1. Dashboard Web (Streamlit ou autre) 
Créer une interface interactive pour visualiser les résultats en temps réel :
* Upload de fichiers de paramètres
* Graphiques dynamiques des simulations
* Comparaison entre différents scénarios
* Export des résultats en PDF/Excel

### 2. Orchestration Kubernetes 
Remplacer la VM Terraform par un cluster Kubernetes pour orchestrer les conteneurs à grande échelle :
* Déploiement multi-nœud automatisé
* Auto-scaling basé sur la charge de travail
* Intégration avec Cloud Build pour CI/CD avancée
* Monitoring avec Prometheus & Grafana

### 3. Base de Données (PostgreSQL/BigQuery) 
Ajouter une couche de persistance pour :
* Archiver tous les résultats de simulation
* Requêtes optimisées sur historique complet
* Dashboards analytiques avancés

### 4. API REST (FastAPI) 
Exposer les simulations via une API :
* Lancer des simulations à la demande
* Récupérer les résultats programmatiquement
* Intégration avec d'autres systèmes