# 📧 Guide Configuration Email - NFS BÂTIMENT

## ✅ Statut Actuel

### QR Code - FONCTIONNE ✅
- **URL QR Code** : `https://nfs-batiment-devis.onrender.com/demande-client`
- **Fonctionnalité** : Clients scannent et accèdent directement au formulaire
- **Test** : QR code testé et opérationnel

### Email - PRÊT À CONFIGURER 📧
- **Système** : SMTP Gmail intégré
- **Status** : Attend configuration du mot de passe

---

## 🔧 Configuration Email (5 minutes)

### Étape 1 : Générer un mot de passe d'application Gmail

1. **Aller sur** : https://myaccount.google.com/security
2. **Activer "Validation en 2 étapes"** (si pas déjà fait)
3. **Cliquer sur "Mots de passe d'application"**
4. **Sélectionner "Autre" et saisir** : `NFS BATIMENT DEVIS`
5. **Copier le mot de passe généré** (format : `abcd efgh ijkl mnop`)

### Étape 2 : Configurer sur Render

1. **Aller sur** : https://render.com/
2. **Se connecter et aller sur le projet "nfs-batiment-devis"**
3. **Cliquer sur "Environment"**
4. **Ajouter une variable** :
   - **Nom** : `EMAIL_PASSWORD`
   - **Valeur** : coller le mot de passe d'application

### Étape 3 : Redémarrer le service

1. **Dans Render, cliquer "Manual Deploy"**
2. **Attendre le redéploiement (2-3 minutes)**

---

## 📋 Test de l'Email

### Test Simple
1. **Générer un devis** sur le site
2. **Cocher "Envoyer par email"**
3. **Saisir un email de test**
4. **Cliquer "Générer & Envoyer"**

### Messages d'erreur possibles
- `📧 Email non configuré` → EMAIL_PASSWORD manquant
- `📧 Email envoyé avec succès !` → ✅ Fonctionne
- `⚠️ Erreur email` → Vérifier le mot de passe

---

## 🎯 Fonctionnalités Email

### Ce qui fonctionne maintenant :
- ✅ **PDF automatique** joint à l'email
- ✅ **Template professionnel** avec logo NFS BÂTIMENT
- ✅ **Informations complètes** : devis, contact, SIRET
- ✅ **Envoi sécurisé** via Gmail SMTP
- ✅ **Gestion d'erreurs** avec messages clairs

### Format de l'email envoyé :
```
🏗️ SASU NFS BATIMENT
Votre devis personnalisé

Bonjour [NOM CLIENT],

Nous avons le plaisir de vous transmettre votre devis
personnalisé pour votre projet.

Détails du devis :
📋 Référence : DEVIS-20250827
📅 Date : 27/08/2025
💰 Montant total : [MONTANT] € TTC

Le devis détaillé est joint à cet email au format PDF.

[PDF EN PIÈCE JOINTE]
```

---

## 🚀 Utilisation Quotidienne

### Avec QR Code :
1. **Imprimer ou partager** le QR code depuis `/admin/qr-code`
2. **Clients scannent** → formulaire automatique
3. **Demandes arrivent** dans `/admin/demandes`
4. **Traiter et répondre** directement

### Avec Email :
1. **Générer devis** normalement
2. **Cocher "Envoyer par email"**
3. **Client reçoit PDF** instantanément
4. **Suivi professionnel** garanti

---

## 📞 Support

En cas de problème :
- **QR Code** : Tester l'URL `https://nfs-batiment-devis.onrender.com/demande-client`
- **Email** : Vérifier la variable `EMAIL_PASSWORD` sur Render
- **Gmail** : S'assurer que la validation 2 étapes est active

**Tout est prêt ! Il suffit de configurer le mot de passe Gmail sur Render. 🚀**
