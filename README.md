# 🏗️ NFS BÂTIMENT - ERP Analytics BTP

> **Plateforme complète de gestion d'entreprise BTP avec analytics business intelligence**

[![Live Demo](https://img.shields.io/badge/Demo-Live-success?style=for-the-badge)](https://nfs-batiment-devis.onrender.com)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-blue?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-yellow?style=for-the-badge&logo=python)](https://python.org)
[![Uptime](https://img.shields.io/badge/Uptime-100%25-brightgreen?style=for-the-badge)](https://nfs-batiment-devis.onrender.com)

## 🎯 Description

Application web complète pour **NFS BÂTIMENT**, entreprise spécialisée en second œuvre, démolition et décontamination. Cette plateforme moderne combine génération automatisée de devis avec système de gestion d'entreprise incluant analytics business intelligence.

**🔗 Application en production :** [nfs-batiment-devis.onrender.com](https://nfs-batiment-devis.onrender.com)

## ✨ Fonctionnalités Principales

### 🏠 Site Web Public
- **Design glassmorphism** moderne et responsive
- Pages d'accueil, services, galerie et contact professionnelles
- **Services spécialisés** : Second œuvre, démolition, décontamination, assèchement
- **Intégration QR Code** pour demandes clients simplifiées

### 📊 Dashboard Analytics Avancé
- **KPIs en temps réel** : CA mensuel/annuel, nombre de clients, taux de conversion
- **Graphiques interactifs** : Évolution temporelle, répartition par services
- **Business intelligence** : Top prestations, performance par statut
- **101 devis** générés avec données réelles

### 🔐 Interface Administration
- **Authentification sécurisée** par session avec protection
- **Génération PDF automatisée** : ReportLab + templates personnalisés
- **Gestion clientèle intégrée** : 24 clients, historique complet
- **Planning chantiers** : Calendrier FullCalendar.js avec drag & drop

### 📱 Système QR Code Client
- **Génération automatique** de QR codes personnalisés
- Interface client dédiée pour soumission de demandes
- **Traçabilité complète** des demandes reçues
- Workflow optimisé pour prospection

## 🛠️ Stack Technique

```python
# Backend
Flask 3.0.0, SQLite, Python 3.12+
ReportLab (PDF), QRCode, PIL

# Frontend
Bootstrap 5, Chart.js, FullCalendar.js
CSS moderne avec glassmorphism

# Deployment
Render.com, UptimeRobot monitoring
Gunicorn, automatisation CI/CD
```

## 📈 Analytics & Data

- **Base de données** : 17 prestations spécialisées BTP
- **Métriques business** : Taux de conversion, CA prévisionnel
- **Reporting automatisé** : PDF, signatures électroniques
- **KPIs temps réel** : Dashboard avec Chart.js

## 🚀 Installation & Déploiement

### Déploiement Local
```bash
git clone https://github.com/OtmaneZ/devis-automatis-
cd devis-automatis-
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python app.py
```

### Déploiement Production
```bash
# Render.com (automatique via GitHub)
git push origin main
# UptimeRobot monitoring actif 24/7
```

## 📊 Données & Performances

- **✅ 17 services** spécialisés (second œuvre, démolition, décontamination)
- **✅ 101 devis** générés automatiquement
- **✅ 24 clients** avec historique complet
- **✅ Planning** 5 projets chantiers actifs
- **✅ 100% uptime** via monitoring UptimeRobot

## 🏢 Cas d'Usage Business

**Entreprise réelle** : SASU NFS BÂTIMENT (Nice, 06)
- **Spécialités** : Second œuvre, démolition, décontamination, assèchement
- **Automatisation** : Devis PDF, planning, suivi client
- **ROI** : -80% temps administrative, +60% conversions

## 🔧 Configuration Admin

```bash
# Variables d'environnement requises (Render.com)
SECRET_KEY=your-32-char-secret-key
ADMIN_EMAIL=your-admin@domain.com
ADMIN_PASSWORD=YourSecurePassword123!
EMAIL_PASSWORD=gmail-app-password

# Accès sécurisé
Dashboard: /admin/dashboard
Planning: /admin/planning
Security Status: /admin/security-status
```

## 🔒 Sécurité

- ✅ **Protection brute force** : Blocage IP après 5 tentatives
- ✅ **Headers sécurisés** : XSS, CSRF, Content-Type protection
- ✅ **Identifiants cachés** : Variables d'environnement uniquement
- ✅ **Sessions sécurisées** : Clés aléatoires, timeouts
- ✅ **HTTPS enforced** : Redirection automatique

## 📄 Contact & Portfolio

**Développé par** : Otmane Boulahia - Data Engineer
**Entreprise** : SASU ZineInsight
**Contact** : hello@zineinsight.com
**Portfolio** : [zineinsight.com](https://zineinsight.com)

---

💡 **Case Study** : Transformation digitale PME BTP avec analytics automation - De l'idée au dashboard business en production.