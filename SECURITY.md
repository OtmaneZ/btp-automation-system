# 🔒 Guide de Sécurité - NFS BÂTIMENT

## ⚠️ PROBLÈMES CORRIGÉS

### Avant (RISQUES ÉLEVÉS)
- ❌ Email admin visible : `admin@nfs-batiment.fr` dans le placeholder
- ❌ Mot de passe faible : `nfs2025`
- ❌ Clé secrète statique dans le code
- ❌ Pas de protection force brute
- ❌ Pas d'headers de sécurité

### Après (SÉCURISÉ) ✅
- ✅ **Identifiants cachés** : Variables d'environnement uniquement
- ✅ **Protection brute force** : Blocage IP 5 min après 5 tentatives
- ✅ **Headers sécurisés** : XSS, CSRF, content-type protection
- ✅ **Clé secrète** : 32 caractères aléatoires depuis env
- ✅ **Mot de passe fort** : Complexité enforced

---

## 🔧 Configuration Sécurisée sur Render

### 1. Variables d'environnement à ajouter :

```bash
# Générer une clé sécurisée (32+ caractères)
SECRET_KEY=a1b2c3d4e5f6789abcdef0123456789abcdef0123456789abcdef
ADMIN_EMAIL=votre-email-admin@domain.com
ADMIN_PASSWORD=MotDePasseTresSecurise123!@#$
EMAIL_PASSWORD=votre-app-password-gmail
```

### 2. Comment générer une clé sécurisée :

```python
# Dans un terminal Python :
import secrets
print(secrets.token_hex(32))
# Copier le résultat dans SECRET_KEY
```

### 3. Étapes sur Render.com :

1. **Aller dans votre projet** → Environment
2. **Ajouter ces 4 variables** avec vos valeurs
3. **Deploy** → Le site redémarrera automatiquement

---

## 🛡️ Fonctionnalités de Sécurité Actives

### Protection Force Brute
- **5 tentatives maximum** par IP
- **Blocage 5 minutes** après échec
- **Reset automatique** après timeout

### Headers de Sécurité HTTP
```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
Referrer-Policy: strict-origin-when-cross-origin
```

### Protection des Sessions
- **Clé secrète aléatoire** pour chiffrement
- **Timeout automatique** des sessions
- **Logout sécurisé** avec nettoyage

---

## 📊 Diagnostic Sécurité

### Endpoint de vérification (admin uniquement) :
`GET /admin/security-status`

Retourne :
```json
{
  "security_status": {
    "secret_key_secure": true,
    "email_configured": true,
    "admin_email_from_env": true,
    "admin_password_from_env": true,
    "using_https": true
  },
  "blocked_ips": 0,
  "recommendations": []
}
```

---

## 🎯 Recommandations Continues

### Pour ta sœur (utilisatrice) :
1. **Mot de passe fort** : 12+ caractères, majuscules, chiffres, symboles
2. **Déconnexion systématique** après usage
3. **Accès uniquement HTTPS** (forcé automatiquement)
4. **Pas de partage d'identifiants**

### Pour l'admin technique :
1. **Rotation périodique** des mots de passe (6 mois)
2. **Monitoring des tentatives** de connexion suspectes
3. **Backup des variables** d'environnement
4. **Test régulier** du endpoint `/admin/security-status`

---

## 🚨 En cas de Problème

### Si connexion impossible :
1. **Vérifier** que les 4 variables sont bien définies sur Render
2. **Tester** le diagnostic : `/admin/security-status`
3. **Redéployer** manuellement sur Render
4. **Attendre 5 min** si blocage IP activé

### Si email admin oublié :
- **Plus jamais visible** dans l'interface (sécurité)
- **Consulter** les variables Render pour retrouver `ADMIN_EMAIL`

**🔒 SÉCURITÉ NIVEAU ENTREPRISE MAINTENANT ACTIVE !**
