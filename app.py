from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for, flash
import sqlite3
from datetime import datetime, timedelta
import os
import tempfile
import atexit
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
import glob
import qrcode
import io
import base64
from PIL import Image
from functools import wraps
import hashlib

app = Flask(__name__)
app.secret_key = 'nfs-batiment-secret-key-2025'  # Clé pour les sessions

# Configuration
DATABASE = 'devis.db'

# Informations entreprise
COMPANY_INFO = {
    'name': 'SASU NFS BATIMENT',
    'address': '23 RUE GUIGLIONDA DE STE AGATHE\n06300 NICE\nFrance',
    'phone': '07 62 72 35 12',
    'email': 'nfsbezzar@gmail.com',
    'siret': '911 840 122 00012',
    'rcs': '911 840 122 R.C.S. Nice',
    'tva': 'FR01911840122',
    'ape': '4334Z',
    'capital': '1500 €',
    'bank': {
        'name': 'CREDIT AGRICOLE',
        'iban': 'FR7619106006674369601820127',
        'bic': 'AGRIFRPP891'
    }
}

# Identifiants admin (en production, mettre dans des variables d'environnement)
ADMIN_CREDENTIALS = {
    'email': 'admin@nfs-batiment.fr',
    'password': hashlib.sha256('nfs2025'.encode()).hexdigest()  # Mot de passe: nfs2025
}

def login_required(f):
    """Décorateur pour protéger les routes admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Nettoyer les PDFs temporaires au démarrage et à l'arrêt
def cleanup_temp_pdfs():
    """Supprime tous les PDFs temporaires"""
    try:
        temp_dir = tempfile.gettempdir()
        pdf_files = glob.glob(os.path.join(temp_dir, "tmp*.pdf"))
        for pdf_file in pdf_files:
            try:
                os.unlink(pdf_file)
            except:
                pass
    except:
        pass

# Nettoyer au démarrage et à l'arrêt
atexit.register(cleanup_temp_pdfs)
cleanup_temp_pdfs()

def wrap_text(text, font_name, font_size, max_width):
    """Découpe le texte pour qu'il tienne dans la largeur donnée"""
    from reportlab.pdfbase.pdfmetrics import stringWidth

    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        if stringWidth(test_line, font_name, font_size) <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines

def init_db():
    """Initialise la base de données"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Table clients
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            adresse TEXT NOT NULL,
            telephone TEXT,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Table prestations prédéfinies
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prestations_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            unite TEXT NOT NULL,
            prix_unitaire REAL NOT NULL
        )
    ''')

    # Table devis
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT UNIQUE NOT NULL,
            client_id INTEGER,
            total_ht REAL NOT NULL,
            tva REAL NOT NULL,
            total_ttc REAL NOT NULL,
            statut TEXT DEFAULT 'brouillon',
            payment_mode TEXT DEFAULT 'virement',
            payment_deadline TEXT DEFAULT '30j',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients (id)
        )
    ''')

    # Table lignes de devis
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devis_lignes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            devis_id INTEGER,
            prestation_type_id INTEGER,
            description TEXT,
            quantite REAL NOT NULL,
            prix_unitaire REAL NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (devis_id) REFERENCES devis (id),
            FOREIGN KEY (prestation_type_id) REFERENCES prestations_types (id)
        )
    ''')

    # Table signatures électroniques
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS signatures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            devis_id INTEGER UNIQUE,
            signature_data TEXT NOT NULL,
            signed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            client_ip TEXT,
            FOREIGN KEY (devis_id) REFERENCES devis (id)
        )
    ''')

    # Table demandes clients via QR Code
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS demandes_clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            telephone TEXT NOT NULL,
            email TEXT,
            adresse TEXT,
            description TEXT NOT NULL,
            photo_path TEXT,
            statut TEXT DEFAULT 'nouvelle',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Table chantiers pour le planning
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chantiers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_chantier TEXT NOT NULL,
            client_nom TEXT NOT NULL,
            client_telephone TEXT,
            adresse TEXT NOT NULL,
            description TEXT,
            date_debut DATE NOT NULL,
            date_fin DATE,
            statut TEXT DEFAULT 'planifie',
            priorite TEXT DEFAULT 'normale',
            montant_prevu REAL,
            devis_id INTEGER,
            couleur TEXT DEFAULT '#667eea',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (devis_id) REFERENCES devis (id)
        )
    ''')

    # 22 prestations BTP propres
    prestations_btp = [
        ('Maçonnerie générale', 'm²', 45.0),
        ('Chape béton', 'm²', 22.0),
        ('Enduit façade', 'm²', 28.0),
        ('Dalle béton', 'm²', 45.0),
        ('Plomberie complète', 'forfait', 2500.0),
        ('Création point d\'eau', 'unité', 350.0),
        ('Installation WC', 'unité', 180.0),
        ('Électricité complète', 'forfait', 3500.0),
        ('Point luminaire', 'unité', 85.0),
        ('Prise électrique', 'unité', 65.0),
        ('Peinture murs', 'm²', 25.0),
        ('Peinture façade', 'm²', 35.0),
        ('Carrelage sol', 'm²', 35.0),
        ('Carrelage mural', 'm²', 42.0),
        ('Parquet flottant', 'm²', 28.0),
        ('Isolation combles', 'm²', 30.0),
        ('Cloisons placo', 'm²', 40.0),
        ('Porte intérieure', 'unité', 200.0),
        ('Fenêtre PVC', 'm²', 320.0),
        ('Couverture tuiles', 'm²', 55.0),
        ('Terrassement', 'm³', 25.0),
        ('Main d\'œuvre', 'heure', 45.0),
    ]

    # SUPPRIMER TOUS LES DOUBLONS AVANT INSERT
    cursor.execute('DELETE FROM prestations_types')

    cursor.executemany('''
        INSERT INTO prestations_types (nom, unite, prix_unitaire)
        VALUES (?, ?, ?)
    ''', prestations_btp)

    conn.commit()
    conn.close()

# Initialiser la base de données au démarrage
init_db()

@app.route('/')
def index():
    """Page d'accueil - Site vitrine"""
    return render_template('website/home.html', company_info=COMPANY_INFO)

@app.route('/admin/login')
def admin_login():
    """Page de connexion admin"""
    return render_template('admin/login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    """Traitement de la connexion admin"""
    email = request.form.get('email')
    password = request.form.get('password')

    if email == ADMIN_CREDENTIALS['email'] and hashlib.sha256(password.encode()).hexdigest() == ADMIN_CREDENTIALS['password']:
        session['admin_logged_in'] = True
        flash('Connexion réussie !', 'success')
        return redirect(url_for('admin_dashboard'))
    else:
        flash('Email ou mot de passe incorrect', 'error')
        return redirect(url_for('admin_login'))

@app.route('/admin/logout')
def admin_logout():
    """Déconnexion admin"""
    session.pop('admin_logged_in', None)
    flash('Vous êtes déconnecté', 'info')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Dashboard admin - Générateur de devis"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Récupérer les types de prestations
    cursor.execute('SELECT * FROM prestations_types ORDER BY nom')
    prestations = cursor.fetchall()

    conn.close()

    return render_template('admin/dashboard.html', prestations=prestations)

# ========================================
# ROUTES SITE VITRINE (PUBLIC)
# ========================================

@app.route('/services')
def services():
    """Page services"""
    return render_template('website/services.html', company_info=COMPANY_INFO)

@app.route('/galerie')
def galerie():
    """Page galerie projets"""
    return render_template('website/galerie.html', company_info=COMPANY_INFO)

@app.route('/contact')
def contact():
    """Page contact"""
    return render_template('website/contact.html', company_info=COMPANY_INFO)

@app.route('/api/contact', methods=['POST'])
def contact_form():
    """Traitement formulaire de contact"""
    try:
        data = request.json
        # Ici on pourrait envoyer un email ou sauvegarder en base
        # Pour le moment, on retourne juste un succès
        return jsonify({'success': True, 'message': 'Message envoyé avec succès!'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ========================================
# ROUTES ADMIN (PROTÉGÉES)
# ========================================

@app.route('/admin/planning')
@login_required
def admin_planning():
    """Planning des chantiers"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Récupérer tous les chantiers
    cursor.execute('''
        SELECT id, nom_chantier, client_nom, adresse, date_debut, date_fin, 
               statut, priorite, montant_prevu, couleur, description
        FROM chantiers 
        ORDER BY date_debut ASC
    ''')
    chantiers = cursor.fetchall()
    
    conn.close()
    
    return render_template('admin/planning.html', chantiers=chantiers)

@app.route('/api/chantiers', methods=['GET'])
@login_required
def get_chantiers():
    """API pour récupérer les chantiers (format FullCalendar)"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, nom_chantier, client_nom, date_debut, date_fin, 
               statut, couleur, montant_prevu, description
        FROM chantiers
    ''')
    chantiers = cursor.fetchall()
    conn.close()
    
    # Convertir en format FullCalendar
    events = []
    for chantier in chantiers:
        events.append({
            'id': chantier[0],
            'title': f"{chantier[1]} - {chantier[2]}",
            'start': chantier[3],
            'end': chantier[4] or chantier[3],  # Si pas de date fin, même jour
            'backgroundColor': chantier[6] or '#667eea',
            'borderColor': chantier[6] or '#667eea',
            'extendedProps': {
                'statut': chantier[5],
                'montant': chantier[7],
                'description': chantier[8]
            }
        })
    
    return jsonify(events)

@app.route('/api/chantiers', methods=['POST'])
@login_required
def create_chantier():
    """Créer un nouveau chantier"""
    try:
        data = request.json
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO chantiers (nom_chantier, client_nom, client_telephone, 
                                 adresse, description, date_debut, date_fin, 
                                 statut, priorite, montant_prevu, couleur)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['nom_chantier'],
            data['client_nom'],
            data.get('client_telephone', ''),
            data['adresse'],
            data.get('description', ''),
            data['date_debut'],
            data.get('date_fin'),
            data.get('statut', 'planifie'),
            data.get('priorite', 'normale'),
            data.get('montant_prevu', 0),
            data.get('couleur', '#667eea')
        ))
        
        chantier_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'id': chantier_id})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/chantiers/<int:chantier_id>', methods=['PUT'])
@login_required
def update_chantier(chantier_id):
    """Mettre à jour un chantier"""
    try:
        data = request.json
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE chantiers 
            SET nom_chantier=?, client_nom=?, adresse=?, date_debut=?, 
                date_fin=?, statut=?, couleur=?, montant_prevu=?, description=?
            WHERE id=?
        ''', (
            data['nom_chantier'],
            data['client_nom'],
            data['adresse'],
            data['date_debut'],
            data.get('date_fin'),
            data.get('statut', 'planifie'),
            data.get('couleur', '#667eea'),
            data.get('montant_prevu', 0),
            data.get('description', ''),
            chantier_id
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/historique')
@login_required
def historique():
    """Page d'historique des devis"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Récupérer tous les devis avec infos client
    cursor.execute('''
        SELECT d.id, d.numero, d.total_ht, d.tva, d.total_ttc, d.statut,
               d.created_at, c.nom, c.prenom, c.email
        FROM devis d
        JOIN clients c ON d.client_id = c.id
        ORDER BY d.created_at DESC
    ''')
    devis_list = cursor.fetchall()

    conn.close()

    return render_template('historique.html', devis=devis_list)

@app.route('/api/change-status', methods=['POST'])
def change_status():
    """Change le statut d'un devis"""
    data = request.json

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            'UPDATE devis SET statut = ? WHERE id = ?',
            (data['status'], data['devis_id'])
        )

        conn.commit()
        conn.close()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/generate-devis', methods=['POST'])
@login_required
def generate_devis():
    """Génère un devis PDF"""
    data = request.json

    # Debug : afficher les données reçues
    print("🔍 Données reçues:", data)
    if 'payment' in data:
        print("💳 Données paiement:", data['payment'])
    else:
        print("❌ Aucune donnée de paiement trouvée!")

    try:
        # Sauvegarder en base
        devis_id = save_devis_to_db(data)

        # Récupérer le numéro généré
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT numero FROM devis WHERE id = ?', (devis_id,))
        devis_numero = cursor.fetchone()[0]
        conn.close()

        # Générer le PDF avec le bon numéro
        print(f"🚀 AVANT generate_pdf - data contient: {list(data.keys())}")
        if 'payment' in data:
            print(f"💳 AVANT generate_pdf - payment: {data['payment']}")
        pdf_path = generate_pdf(devis_id, data, devis_numero)

        return jsonify({
            'success': True,
            'devis_id': devis_id,
            'pdf_url': f'/download-pdf/{devis_id}'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def save_devis_to_db(data):
    """Sauvegarde le devis en base de données"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Insérer le client
    cursor.execute('''
        INSERT INTO clients (nom, prenom, adresse, telephone, email)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        data['client']['nom'],
        data['client']['prenom'],
        data['client']['adresse'],
        data['client'].get('telephone', ''),
        data['client'].get('email', '')
    ))
    client_id = cursor.lastrowid

    # Calculer les totaux
    total_ht = sum(item['total'] for item in data['prestations'])
    tva = total_ht * 0.20  # TVA 20%
    total_ttc = total_ht + tva

    # Générer numéro de devis séquentiel avec protection contre doublons
    year = datetime.now().year
    attempt = 0
    max_attempts = 100

    while attempt < max_attempts:
        # Chercher le prochain numéro disponible
        cursor.execute('SELECT MAX(CAST(SUBSTR(numero, -4) AS INTEGER)) FROM devis WHERE numero LIKE ?',
                      (f"DEV-{year}-%",))
        result = cursor.fetchone()[0]
        next_num = (result + 1) if result else 1
        numero = f"DEV-{year}-{next_num:04d}"

        # Vérifier que ce numéro n'existe pas déjà (race condition protection)
        cursor.execute('SELECT id FROM devis WHERE numero = ?', (numero,))
        if not cursor.fetchone():
            break
        attempt += 1

    if attempt >= max_attempts:
        raise Exception("Impossible de générer un numéro de devis unique")

    # Insérer le devis
    payment_data = data.get('payment', {})
    payment_mode = payment_data.get('mode', 'virement')
    payment_deadline = payment_data.get('deadline', '30j')

    cursor.execute('''
        INSERT INTO devis (numero, client_id, total_ht, tva, total_ttc, payment_mode, payment_deadline)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (numero, client_id, total_ht, tva, total_ttc, payment_mode, payment_deadline))
    devis_id = cursor.lastrowid

    # Insérer les lignes de prestation
    for item in data['prestations']:
        cursor.execute('''
            INSERT INTO devis_lignes (devis_id, description, quantite, prix_unitaire, total)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            devis_id,
            item['description'],
            item['quantite'],
            item['prix_unitaire'],
            item['total']
        ))

    conn.commit()
    conn.close()

    return devis_id

def generate_pdf(devis_id, data, devis_numero=None):
    """Génère le PDF du devis"""
    # Créer un fichier temporaire
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf_path = temp_file.name
    temp_file.close()

    # Si pas de numéro fourni, le générer (fallback)
    if not devis_numero:
        devis_numero = f"DEV-{datetime.now().year}-{devis_id:04d}"

    # Extraire les données de paiement
    payment_data = data.get('payment', {})
    payment_mode = payment_data.get('mode', 'virement')
    payment_deadline = payment_data.get('deadline', '30j')

    print(f"🔍 EXTRACTED payment_mode: {payment_mode}")
    print(f"🔍 EXTRACTED payment_deadline: {payment_deadline}")
    print(f"🔍 RAW payment_data: {payment_data}")

    # Créer le PDF
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4    # En-tête avec logo et informations entreprise
    try:
        logo_path = os.path.join('static', 'img', 'logo-nfs.png')
        if os.path.exists(logo_path):
            # Ajouter le logo (redimensionné)
            c.drawImage(logo_path, 50, height - 80, width=80, height=40, mask='auto')

            # Informations entreprise à côté du logo
            c.setFont("Helvetica-Bold", 14)
            c.drawString(140, height - 45, COMPANY_INFO['name'])
            c.setFont("Helvetica", 9)
            c.drawString(140, height - 60, COMPANY_INFO['address'].split('\n')[0])
            c.drawString(140, height - 72, COMPANY_INFO['address'].split('\n')[1])
            c.drawString(140, height - 84, COMPANY_INFO['address'].split('\n')[2])
            c.drawString(140, height - 96, f"Tél: {COMPANY_INFO['phone']} | Email: {COMPANY_INFO['email']}")
        else:
            # Fallback sans logo
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, height - 45, COMPANY_INFO['name'])
            c.setFont("Helvetica", 9)
            c.drawString(50, height - 60, COMPANY_INFO['address'].split('\n')[0])
            c.drawString(50, height - 72, COMPANY_INFO['address'].split('\n')[1])
            c.drawString(50, height - 84, COMPANY_INFO['address'].split('\n')[2])
            c.drawString(50, height - 96, f"Tél: {COMPANY_INFO['phone']} | Email: {COMPANY_INFO['email']}")
    except Exception as e:
        # Fallback en cas d'erreur avec le logo
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 45, COMPANY_INFO['name'])
        c.setFont("Helvetica", 9)
        c.drawString(50, height - 60, "Entreprise générale du bâtiment")

    # Informations légales en haut à droite
    c.setFont("Helvetica", 8)
    legal_y = height - 45
    c.drawRightString(width - 50, legal_y, f"SIRET: {COMPANY_INFO['siret']}")
    legal_y -= 10
    c.drawRightString(width - 50, legal_y, COMPANY_INFO['rcs'])
    legal_y -= 10
    c.drawRightString(width - 50, legal_y, f"N° TVA: {COMPANY_INFO['tva']}")
    legal_y -= 10
    c.drawRightString(width - 50, legal_y, f"Code APE: {COMPANY_INFO['ape']}")
    legal_y -= 10
    c.drawRightString(width - 50, legal_y, f"Capital: {COMPANY_INFO['capital']}")

    # Titre
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(HexColor('#667eea'))
    c.drawCentredString(width/2, height - 130, "DEVIS")
    c.setFillColor(HexColor('#000000'))  # Retour au noir

    # Informations client
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 180, "CLIENT:")
    c.setFont("Helvetica", 10)
    y_pos = height - 200
    c.drawString(50, y_pos, f"{data['client']['prenom']} {data['client']['nom']}")
    y_pos -= 15
    c.drawString(50, y_pos, data['client']['adresse'])
    if data['client'].get('telephone'):
        y_pos -= 15
        c.drawString(50, y_pos, f"Tél: {data['client']['telephone']}")
    if data['client'].get('email'):
        y_pos -= 15
        c.drawString(50, y_pos, f"Email: {data['client']['email']}")

    # Date et numéro avec le vrai numéro de devis
    c.setFont("Helvetica", 10)
    c.drawRightString(width - 50, height - 180, f"Date: {datetime.now().strftime('%d/%m/%Y')}")
    c.drawRightString(width - 50, height - 195, f"Devis N°: {devis_numero}")

    # Tableau des prestations avec style amélioré
    y_pos = height - 280

    # En-tête du tableau simple sans fond coloré
    c.setFont("Helvetica-Bold", 10)
    c.drawString(60, y_pos, "Description")
    c.drawString(300, y_pos, "Qté")
    c.drawString(350, y_pos, "P.U.")
    c.drawString(450, y_pos, "Total HT")

    # Pas de ligne de séparation - plus propre
    y_pos -= 20

    # Prestations avec word wrap pour descriptions
    c.setFont("Helvetica", 9)
    total_ht = 0
    line_height = 12

    for i, item in enumerate(data['prestations']):
        # Découper la description en lignes
        description_lines = wrap_text(item['description'], "Helvetica", 9, 230)  # Max width 230px

        # Calculer la hauteur nécessaire pour cette prestation
        needed_height = max(25, len(description_lines) * line_height + 5)
        y_pos -= needed_height

        # Vérifier s'il faut une nouvelle page (garde 150px pour les totaux)
        if y_pos < 150:
            c.showPage()  # Nouvelle page
            # Redessiner l'en-tête sur la nouvelle page
            y_pos = height - 100
            c.setFont("Helvetica-Bold", 10)
            c.drawString(60, y_pos, "Description")
            c.drawString(300, y_pos, "Qté")
            c.drawString(350, y_pos, "P.U.")
            c.drawString(450, y_pos, "Total HT")
            y_pos -= 25
            c.setFont("Helvetica", 9)

        # Pas d'alternance de couleur - tableau simple et propre
        c.setFillColor(HexColor('#000000'))

        # Dessiner les lignes de description
        desc_y = y_pos + (needed_height - line_height) // 2
        for line in description_lines:
            c.drawString(60, desc_y, line)
            desc_y -= line_height

        # Dessiner les autres colonnes centrées verticalement
        middle_y = y_pos + (needed_height - line_height) // 2
        c.drawString(300, middle_y, str(item['quantite']))
        c.drawString(350, middle_y, f"{item['prix_unitaire']:.2f} €")
        c.drawString(450, middle_y, f"{item['total']:.2f} €")
        total_ht += item['total']

    # Vérifier s'il faut une nouvelle page pour les totaux et conditions
    if y_pos < 200:
        c.showPage()
        y_pos = height - 100

    # Totaux avec style amélioré
    y_pos -= 40

    # Totaux alignés avec les colonnes du tableau
    y_pos -= 20
    c.setFillColor(HexColor('#000000'))
    c.setFont("Helvetica-Bold", 11)

    # Aligner "Total HT:" avec la colonne "Total HT" du tableau
    c.drawRightString(440, y_pos, "Total HT:")
    c.drawString(450, y_pos, f"{total_ht:.2f} €")

    y_pos -= 18
    tva = total_ht * 0.20
    c.drawRightString(440, y_pos, "TVA (20%):")
    c.drawString(450, y_pos, f"{tva:.2f} €")

    y_pos -= 20
    total_ttc = total_ht + tva
    c.setFont("Helvetica-Bold", 14)
    c.drawRightString(440, y_pos, "Total TTC:")
    c.drawString(450, y_pos, f"{total_ttc:.2f} €")

    # Retour au noir pour la suite
    c.setFillColor(HexColor('#000000'))

    # Conditions avec style et vraies informations
    y_pos -= 60
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y_pos, "CONDITIONS GÉNÉRALES:")

    y_pos -= 20
    c.setFont("Helvetica", 9)

    # Générer les conditions dynamiquement
    payment_modes_fr = {
        'virement': 'Virement bancaire',
        'cheque': 'Chèque',
        'especes': 'Espèces',
        'cb': 'Carte bancaire'
    }

    payment_deadlines_fr = {
        'reception': 'à réception',
        '15j': '15 jours',
        '30j': '30 jours',
        '45j': '45 jours',
        '60j': '60 jours'
    }

    mode_fr = payment_modes_fr.get(payment_mode, 'Virement bancaire')
    deadline_fr = payment_deadlines_fr.get(payment_deadline, '30 jours')

    conditions = [
        "• Devis valable 30 jours à compter de la date d'émission",
        f"• Échéance de paiement : {deadline_fr}",
        f"• Mode de règlement : {mode_fr}",
        "• Intérêt de retard égal à 3 fois le taux d'intérêt légal",
        "• Prix exprimés en euros TTC",
        "• Travaux conformes aux règles de l'art et normes en vigueur"
    ]

    for condition in conditions:
        c.drawString(50, y_pos, condition)
        y_pos -= 15

    # Informations bancaires (seulement si virement)
    if payment_mode == 'virement':
        y_pos -= 20
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y_pos, "COORDONNÉES BANCAIRES:")

        y_pos -= 20
        c.setFont("Helvetica", 9)
        bank_info = [
            f"Notre domiciliation bancaire : {COMPANY_INFO['bank']['name']}",
            f"IBAN : {COMPANY_INFO['bank']['iban']}",
            f"BIC : {COMPANY_INFO['bank']['bic']}"
        ]

        for info in bank_info:
            c.drawString(50, y_pos, info)
            y_pos -= 15

    # Signature avec nom d'entreprise correct
    y_pos -= 30
    c.setFont("Helvetica", 10)
    c.drawString(50, y_pos, "Bon pour accord:")
    c.drawString(300, y_pos, COMPANY_INFO['name'])

    y_pos -= 20
    c.drawString(50, y_pos, "Date et signature client:")

    # Footer avec informations légales complètes
    c.setFont("Helvetica", 7)
    footer_y = 50
    c.drawCentredString(width/2, footer_y,
                     f"{COMPANY_INFO['name']} - {COMPANY_INFO['siret']} - {COMPANY_INFO['rcs']} - APE: {COMPANY_INFO['ape']}")
    c.drawCentredString(width/2, footer_y - 10,
                     f"Capital: {COMPANY_INFO['capital']} - TVA: {COMPANY_INFO['tva']}")

    c.save()

    # Nettoyer après un délai (pour laisser le temps au téléchargement)
    import threading
    def delayed_cleanup():
        import time
        time.sleep(60)  # Attendre 1 minute
        try:
            os.unlink(pdf_path)
        except:
            pass

    threading.Thread(target=delayed_cleanup).start()

    return pdf_path

@app.route('/download-pdf/<int:devis_id>')
def download_pdf(devis_id):
    """Télécharge le PDF d'un devis"""
    # Récupérer les données du devis
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT d.id, d.numero, d.client_id, d.total_ht, d.tva, d.total_ttc,
               d.statut, d.created_at, d.payment_mode, d.payment_deadline,
               c.nom, c.prenom, c.adresse, c.telephone, c.email
        FROM devis d
        JOIN clients c ON d.client_id = c.id
        WHERE d.id = ?
    ''', (devis_id,))
    devis_data = cursor.fetchone()

    cursor.execute('SELECT * FROM devis_lignes WHERE devis_id = ?', (devis_id,))
    lignes = cursor.fetchall()

    conn.close()

    if not devis_data:
        return "Devis non trouvé", 404

    # Reconstituer les données pour le PDF
    data = {
        'client': {
            'nom': devis_data[10],      # c.nom
            'prenom': devis_data[11],   # c.prenom
            'adresse': devis_data[12],  # c.adresse
            'telephone': devis_data[13], # c.telephone
            'email': devis_data[14]     # c.email
        },
        'prestations': [
            {
                'description': ligne[3],
                'quantite': ligne[4],
                'prix_unitaire': ligne[5],
                'total': ligne[6]
            } for ligne in lignes
        ],
        'payment': {
            'mode': devis_data[8],      # d.payment_mode
            'deadline': devis_data[9]   # d.payment_deadline
        }
    }

    # Passer le numéro de devis au PDF
    pdf_path = generate_pdf(devis_id, data, devis_data[1])  # numero est toujours à l'index 1
    return send_file(pdf_path, as_attachment=True, download_name=f"devis_{devis_data[1]}.pdf")

@app.route('/signature/<int:devis_id>')
def signature_page(devis_id):
    """Page de signature pour le client"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Vérifier si le devis existe
    cursor.execute('''
        SELECT d.id, d.numero, d.total_ttc, c.nom, c.prenom, c.email
        FROM devis d
        JOIN clients c ON d.client_id = c.id
        WHERE d.id = ?
    ''', (devis_id,))
    devis_data = cursor.fetchone()

    if not devis_data:
        conn.close()
        return "Devis non trouvé", 404

    # Vérifier si déjà signé
    cursor.execute('SELECT signed_at FROM signatures WHERE devis_id = ?', (devis_id,))
    signature = cursor.fetchone()

    conn.close()

    return render_template('signature.html',
                         devis=devis_data,
                         already_signed=signature is not None,
                         signed_at=signature[0] if signature else None)

@app.route('/api/sign-devis', methods=['POST'])
def sign_devis():
    """Enregistre la signature du devis"""
    data = request.json

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Vérifier si le devis existe et n'est pas déjà signé
        cursor.execute('SELECT id FROM signatures WHERE devis_id = ?', (data['devis_id'],))
        existing = cursor.fetchone()

        if existing:
            return jsonify({'success': False, 'error': 'Devis déjà signé'}), 400

        # Enregistrer la signature
        cursor.execute('''
            INSERT INTO signatures (devis_id, signature_data, client_ip)
            VALUES (?, ?, ?)
        ''', (
            data['devis_id'],
            data['signature_data'],
            request.remote_addr
        ))

        # Mettre à jour le statut du devis
        cursor.execute('UPDATE devis SET statut = ? WHERE id = ?', ('accepte', data['devis_id']))

        conn.commit()
        conn.close()

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/email-templates')
def get_email_templates():
    """Retourne les templates email disponibles"""
    templates = {
        'standard': {
            'name': 'Envoi Standard',
            'subject': 'Votre devis BTP #{numero} - NFS',
            'body': '''Bonjour {prenom} {nom},

Nous avons le plaisir de vous transmettre votre devis pour vos travaux BTP.

📋 Devis N° : {numero}
💰 Montant : {montant} € TTC
📅 Date : {date}

Vous trouverez en pièce jointe le devis détaillé au format PDF.

Pour toute question, n'hésitez pas à nous contacter.

Cordialement,
L'équipe NFS
📞 Tél : 06 XX XX XX XX
📧 Email : contact@nfs-btp.fr'''
        },
        'relance': {
            'name': 'Relance Client',
            'subject': 'Relance - Devis BTP #{numero} - NFS',
            'body': '''Bonjour {prenom} {nom},

Nous espérons que vous allez bien.

Nous vous avons transmis le devis #{numero} d'un montant de {montant} € TTC le {date}.

Avez-vous eu l'occasion de l'examiner ? Nous restons à votre disposition pour tout complément d'information.

🔗 Lien de signature : {lien_signature}

N'hésitez pas à nous contacter si vous avez des questions.

Cordialement,
L'équipe NFS
📞 Tél : 06 XX XX XX XX
📧 Email : contact@nfs-btp.fr'''
        },
        'accepte': {
            'name': 'Devis Accepté',
            'subject': 'Confirmation - Devis #{numero} accepté - NFS',
            'body': '''Bonjour {prenom} {nom},

Nous vous remercions d'avoir accepté notre devis #{numero} !

✅ Devis accepté le : {date_signature}
💰 Montant validé : {montant} € TTC

Prochaines étapes :
• Nous vous recontacterons sous 48h pour planifier les travaux
• Un planning détaillé vous sera transmis
• Les travaux débuteront selon les modalités convenues

Nous sommes ravis de collaborer avec vous sur ce projet.

Cordialement,
L'équipe NFS
📞 Tél : 06 XX XX XX XX
📧 Email : contact@nfs-btp.fr'''
        },
        'signature': {
            'name': 'Demande de Signature',
            'subject': 'Signature électronique - Devis #{numero} - NFS',
            'body': '''Bonjour {prenom} {nom},

Votre devis BTP est prêt et n'attend plus que votre signature !

📋 Devis N° : {numero}
💰 Montant : {montant} € TTC

✍️ Signez en ligne en 1 clic : {lien_signature}

La signature électronique est :
• Sécurisée et horodatée
• Juridiquement valable
• Simple et rapide

Une fois signé, nous pourrons démarrer votre projet dans les meilleurs délais.

Cordialement,
L'équipe NFS
📞 Tél : 06 XX XX XX XX
📧 Email : contact@nfs-btp.fr'''
        }
    }
    return jsonify(templates)

# ========================================
# SYSTÈME QR CODE POUR DEMANDES CLIENTS
# ========================================

@app.route('/admin/qr-code')
@login_required
def generate_qr_code():
    """Génère un QR code pour les demandes clients"""
    # URL vers le formulaire client
    client_url = request.url_root + 'demande-client'

    # Créer le QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(client_url)
    qr.make(fit=True)

    # Créer l'image
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Convertir en base64 pour l'affichage web
    buffered = io.BytesIO()
    qr_img.save(buffered, format="PNG")
    qr_img_str = base64.b64encode(buffered.getvalue()).decode()

    return render_template('qr_generator.html',
                         qr_code=qr_img_str,
                         client_url=client_url)

@app.route('/demande-client')
def client_request_form():
    """Formulaire de demande client via QR code"""
    return render_template('client_request.html')

@app.route('/api/submit-demande', methods=['POST'])
def submit_client_request():
    """Soumission d'une demande client"""
    try:
        # Récupérer les données du formulaire
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        telephone = request.form.get('telephone')
        email = request.form.get('email', '')
        adresse = request.form.get('adresse', '')
        description = request.form.get('description')

        # Gestion de la photo
        photo_path = None
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo.filename and photo.filename != '':
                # Créer le dossier uploads s'il n'existe pas
                upload_dir = 'static/uploads'
                os.makedirs(upload_dir, exist_ok=True)

                # Sauvegarder avec un nom unique
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{photo.filename}"
                photo_path = os.path.join(upload_dir, filename)
                photo.save(photo_path)

        # Sauvegarder en base
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO demandes_clients (nom, prenom, telephone, email, adresse, description, photo_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nom, prenom, telephone, email, adresse, description, photo_path))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Demande envoyée avec succès!'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/admin/demandes')
@login_required
def client_requests():
    """Page de gestion des demandes clients"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM demandes_clients ORDER BY created_at DESC')
    demandes = cursor.fetchall()

    conn.close()

    return render_template('client_requests_admin.html', demandes=demandes)

@app.route('/api/change-demande-status', methods=['POST'])
def change_demande_status():
    """Change le statut d'une demande client"""
    try:
        data = request.json
        demande_id = data.get('demande_id')
        new_status = data.get('status')

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE demandes_clients
            SET statut = ?
            WHERE id = ?
        ''', (new_status, demande_id))

        conn.commit()
        conn.close()

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # Initialiser la base de données
    init_db()

    # Lancer l'application
    print("🚀 Générateur de devis BTP - NFS")
    print("📋 Interface disponible sur: http://localhost:5001")
    print("🎯 Prêt pour la démo !")

    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)
