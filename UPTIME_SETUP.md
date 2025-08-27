# Configuration UptimeRobot pour maintenir l'app active

## Service de monitoring gratuit pour éviter les cold starts Render

### 1. S'inscrire sur UptimeRobot (gratuit)
https://uptimerobot.com/

### 2. Ajouter un monitor HTTP(S)
- **URL à surveiller:** https://nfs-batiment-devis.onrender.com/health
- **Type:** HTTP(S)
- **Intervalle:** 5 minutes (plan gratuit)
- **Nom:** NFS Bâtiment Dashboard

### 3. Alertes (optionnel)
- Email si l'app tombe
- Webhook vers Discord/Slack

## Alternative GitHub Actions (gratuit)

Workflow qui ping l'app toutes les heures :

```yaml
name: Keep App Alive
on:
  schedule:
    - cron: '0 */1 * * *'  # Toutes les heures
  workflow_dispatch:

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping App
        run: |
          curl -f https://nfs-batiment-devis.onrender.com/health || exit 1
          echo "✅ App is alive"
```

## Comparaison solutions:

| Solution | Coût | Efficacité | Maintenance |
|----------|------|------------|-------------|
| UptimeRobot | Gratuit | ⭐⭐⭐⭐⭐ | Zéro |
| GitHub Actions | Gratuit | ⭐⭐⭐⭐ | Faible |
| Script local | Gratuit | ⭐⭐⭐ | Moyenne |
| Render Paid | 7$/mois | ⭐⭐⭐⭐⭐ | Zéro |

**Recommandation:** UptimeRobot pour démarrer (setup en 2 minutes)
