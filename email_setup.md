# 📧 CONFIGURATION EMAILJS POUR NFS BÂTIMENT

## 🚀 ÉTAPES POUR ACTIVER L'ENVOI D'EMAIL

### 1. Créer un compte EmailJS (GRATUIT)
- Va sur https://www.emailjs.com/
- Créer un compte gratuit (200 emails/mois)
- Confirme ton email

### 2. Créer un service email
- Dashboard → Email Services → Add New Service
- Choisis "Gmail" ou "Outlook" selon ton email pro
- Connecte ton compte email NFS

### 3. Créer un template d'email
- Dashboard → Email Templates → Create New Template
- Template ID: `nfs_devis_template`
- Sujet: `Votre devis NFS BÂTIMENT N°{{devis_numero}}`

**Contenu du template :**
```
Bonjour {{to_name}},

Vous trouverez en pièce jointe votre devis personnalisé N°{{devis_numero}}.

Ce devis est valable 30 jours à compter de sa date d'émission.

Détails du devis :
• Client : {{client_name}}
• Date : {{date}}
• Total : {{total_ttc}}

Pour toute question, n'hésitez pas à nous contacter.

Cordialement,
L'équipe {{company_name}}

---
NFS BÂTIMENT
Email: contact@nfs-batiment.fr
Téléphone: XX XX XX XX XX
```

### 4. Récupérer les clés
- Dashboard → Integration
- Copie ton **Public Key**
- Copie ton **Service ID**
- Copie ton **Template ID**

### 5. Configuration dans l'app
Remplace dans `templates/index.html` :

```javascript
emailjs.init("YOUR_PUBLIC_KEY");        // → Ta clé publique
'YOUR_SERVICE_ID',                      // → Ton service ID
'YOUR_TEMPLATE_ID',                     // → Ton template ID
```

### 6. Test
- Remplis un devis avec ton email
- Génère → Tu recevras l'email !

## 🎯 RÉSULTAT
- **Client reçoit** un email professionnel avec le PDF
- **Tracking** des emails envoyés
- **Gratuit** jusqu'à 200 emails/mois

## 🔧 ALTERNATIVE SIMPLE (SIMULATION)
En attendant de configurer EmailJS, l'app simule l'envoi et affiche "Email envoyé" !
