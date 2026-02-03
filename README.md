# 📡 Outil de Dimensionnement LTE (4G)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)

## 📝 Description

Ce projet est une application de bureau complète permettant d'effectuer le dimensionnement et la planification radio d'un réseau mobile LTE (4G). Il est conçu pour aider les ingénieurs télécoms et les étudiants à calculer le nombre de sites (eNodeB) nécessaires pour couvrir une zone donnée en fonction du trafic et des paramètres RF.

L'outil intègre les modèles de propagation (Okumura-Hata) et génère des rapports de bilan de liaison.

## ✨ Fonctionnalités Principales

* **Dimensionnement de couverture :** Calcul du rayon de cellule basé sur le modèle Cost-231 Hata.
* **Dimensionnement de capacité :** Estimation du nombre de sites selon la densité d'utilisateurs et le débit cible.
* **Calculs RF avancés :** Bilan de liaison (Link Budget) UL/DL, pertes de propagation (MAPL).
* **Cartographie :** Visualisation graphique simulée des positions des cellules et des eNodeB.
* **Exportation :** Interface prête pour l'exportation des résultats.

## 🛠️ Installation et Lancement

### Prérequis
* Python 3.x installé sur votre machine.
* Les bibliothèques listées dans `requirements.txt`.

### Installation locale (Pour les développeurs)

1.  **Cloner le dépôt :**
    ```bash
    git clone [https://github.com/TON_USER/TON_REPO.git](https://github.com/TON_USER/TON_REPO.git)
    cd TON_REPO
    ```

2.  **Installer les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Lancer l'application :**
    ```bash
    python main.py
    ```

### Téléchargement (Pour les utilisateurs)
Si vous ne souhaitez pas installer Python, vous pouvez télécharger la version exécutable (.exe) directement depuis l'onglet **[Releases](https://github.com/TON_USER/TON_REPO/releases)** de ce dépôt (Windows uniquement).

## 🧮 Aperçu technique

L'application utilise les technologies suivantes :
* **Interface Graphique :** Tkinter (Standard Python GUI)
* **Calculs Mathématiques :** NumPy, Math
* **Visualisation :** Matplotlib (pour les graphes de couverture)

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👤 Auteur

Développé par Diaga NGOM et MMB
