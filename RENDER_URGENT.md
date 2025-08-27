# 🚀 Configuration Render - Variables Sécurisées

## ⚡ ACTIONS URGENTES (5 minutes)

Le site va planter sans ces variables ! À configurer MAINTENANT sur Render :

### 1. Aller sur Render.com
- **Se connecter** à votre compte
- **Cliquer** sur le projet `nfs-batiment-devis`
- **Onglet "Environment"**

### 2. Ajouter ces 4 variables :

```bash
SECRET_KEY
a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890

ADMIN_EMAIL
admin@nfs-batiment.fr

ADMIN_PASSWORD
NFS@2025#Secure!

EMAIL_PASSWORD
[votre-mot-de-passe-gmail-app]
```

### 3. Cliquer "Save Changes"
Le site va redémarrer automatiquement (2-3 minutes)

---

## 🔐 Génération Clé Sécurisée (optionnel)

Pour une sécurité maximale, générer votre propre SECRET_KEY :

1. **Ouvrir un terminal/PowerShell**
2. **Taper** : `python3 -c "import secrets; print(secrets.token_hex(32))"`
3. **Copier** le résultat dans SECRET_KEY sur Render

---

## ✅ Vérification

Après redéploiement :
- **Tester** : https://nfs-batiment-devis.onrender.com/admin/login
- **Plus d'email visible** dans le champ
- **Diagnostic** : https://nfs-batiment-devis.onrender.com/admin/security-status

**⚠️ URGENT : Sans ces variables, le site ne fonctionnera plus après le déploiement !**
