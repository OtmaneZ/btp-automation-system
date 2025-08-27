#!/usr/bin/env python3
"""
Script pour maintenir l'app Render active (éviter les cold starts)
À lancer en local ou sur un serveur pour ping l'app toutes les 10 minutes
"""
import requests
import time
import schedule

APP_URL = "https://nfs-batiment-devis.onrender.com"

def ping_app():
    """Ping l'application pour éviter qu'elle s'endorme"""
    try:
        response = requests.get(APP_URL, timeout=10)
        if response.status_code == 200:
            print(f"✅ App active - {time.strftime('%H:%M:%S')}")
        else:
            print(f"⚠️  App répond mais status {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur ping: {e}")

if __name__ == "__main__":
    print(f"🏃 Démarrage keep-alive pour {APP_URL}")
    print("Ping toutes les 10 minutes pour éviter les cold starts...")

    # Ping immédiat
    ping_app()

    # Programmer les pings
    schedule.every(10).minutes.do(ping_app)

    # Boucle infinie
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n👋 Arrêt du keep-alive")
