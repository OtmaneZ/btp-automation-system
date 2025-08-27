# 📸 Guide Photos Galerie - NFS BÂTIMENT

## 📋 Structure de Nommage

Pour que les photos s'affichent correctement, utilisez exactement ces noms :

### 🚽 Rénovation WC
- `wc_1.jpg`
- `wc_2.jpg`
- `wc_3.jpg` (optionnel)

### 🛋️ Rénovation Salon
- `salon_1.jpg`
- `salon_2.jpg`
- `salon_3.jpg` (optionnel)

### 🍳 Rénovation Cuisine
- `cuisine_1.jpg`
- `cuisine_2.jpg`
- `cuisine_3.jpg` (optionnel)

### 🏠 Pose de Faux-Plafond
- `plafond_1.jpg`
- `plafond_2.jpg`
- `plafond_3.jpg` (optionnel)

## 📁 Emplacement

Toutes les photos doivent être placées dans :
```
/static/img/
```

## 🔧 Comment Ajouter des Photos

1. **Renommer vos photos** selon la nomenclature ci-dessus
2. **Les glisser** dans le dossier `/Users/otmaneboulahia/Documents/Projet devis - facture/static/img/`
3. **Modifier le fichier galerie.html** ligne ~280 pour ajouter les nouveaux noms :

```javascript
const photosByCategory = {
    wc: ['wc_1.jpg', 'wc_2.jpg', 'wc_3.jpg'],  // Ajouter wc_3.jpg
    salon: ['salon_1.jpg', 'salon_2.jpg'],
    cuisine: ['cuisine_1.jpg', 'cuisine_2.jpg'],
    plafond: ['plafond_1.jpg', 'plafond_2.jpg']
};
```

4. **Redéployer** le site sur Render

## ✅ Fonctionnement

- **Clic sur une catégorie** → Modal s'ouvre
- **Photos dans le modal** → Cliquables pour agrandir
- **Auto-responsive** → S'adapte mobile/desktop

**Prêt à recevoir tes photos ! 📸**
