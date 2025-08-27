# 🏗️ BTP Automation System

> **Enterprise-grade construction management platform with advanced analytics and automation**

<div align="center">

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-nfs--batiment--devis.onrender.com-2ea44f?style=for-the-badge)](https://nfs-batiment-devis.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.12+-3776ab?style=for-the-badge&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com)
[![Uptime](https://img.shields.io/badge/Uptime-99.267%25-00d26a?style=for-the-badge)](https://stats.uptimerobot.com/)
[![Build](https://img.shields.io/badge/Build-Passing-00d26a?style=for-the-badge)](https://nfs-batiment-devis.onrender.com)

</div>

## 🎯 Overview

**BTP Automation System** is a comprehensive digital transformation solution for construction companies, featuring automated quote generation, client relationship management, and business intelligence analytics. Built for **NFS BÂTIMENT**, a specialized construction firm in Nice, France.

### Key Business Impact
- **80% reduction** in administrative overhead
- **60% increase** in quote conversion rates
- **Real-time analytics** for strategic decision making
- **Automated workflow** from lead to invoice

---

## ✨ Core Features

### 🏠 **Public Website**
- **Modern glassmorphism design** with responsive layout
- Professional portfolio showcasing completed projects
- **QR Code integration** for instant client inquiries
- SEO-optimized pages with structured data

### 📊 **Analytics Dashboard**
- **Real-time KPIs**: Monthly/annual revenue, client metrics, conversion rates
- **Interactive visualizations**: Chart.js powered business intelligence
- **Performance tracking**: 101 generated quotes, 24 active clients
- **Predictive analytics** for revenue forecasting

### 🔐 **Admin Interface**
- **Secure authentication** with brute force protection
- **PDF generation engine**: Automated quotes with custom templates
- **Client management system**: Complete interaction history
- **Project calendar**: FullCalendar.js with drag & drop scheduling

### 📱 **Client Portal**
- **QR Code workflow**: Instant quote requests via mobile
- **Photo upload capability** for accurate project assessment
- **Status tracking** for submitted requests
- **Automated email notifications**

### 💼 **Invoice Management**
- **Quote-to-invoice** conversion workflow
- **Payment tracking** and status management
- **Financial reporting** with export capabilities
- **Client billing history**

---

## 🛠️ Technical Architecture

### Backend Stack
```python
Flask 3.0.0          # Web framework
SQLite              # Database engine
ReportLab           # PDF generation
QRCode              # QR code generation
PIL/Pillow          # Image processing
```

### Frontend Stack
```javascript
Bootstrap 5         # UI framework
Chart.js           # Data visualization
FullCalendar.js    # Calendar component
Font Awesome       # Icon library
Custom CSS         # Glassmorphism design
```

### Infrastructure
```yaml
Hosting:     Render.com (Auto-deploy)
Monitoring:  UptimeRobot (99.267% uptime)
CI/CD:       GitHub Actions integration
Security:    HTTPS enforced, XSS protection
```

---

## 📈 Business Intelligence

### Analytics Capabilities
- **Revenue tracking**: Real-time financial KPIs
- **Client analytics**: Acquisition cost, lifetime value
- **Performance metrics**: Quote conversion rates, service popularity
- **Operational insights**: Resource allocation, project timelines

### Data Points
- ✅ **17 specialized services** (renovation, demolition, decontamination)
- ✅ **101 automated quotes** generated
- ✅ **24 active clients** with complete history
- ✅ **5 concurrent projects** in planning system
- ✅ **99.267% uptime** monitoring

---

## 🚀 Quick Start

### Local Development
```bash
# Clone repository
git clone https://github.com/OtmaneZ/btp-automation-system.git
cd btp-automation-system

# Setup virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

### Production Deployment
```bash
# Automated deployment via Render.com
git push origin main

# Environment variables required:
# SECRET_KEY, ADMIN_EMAIL, ADMIN_PASSWORD, EMAIL_PASSWORD
```

---

## � Security Features

- **🛡️ Brute force protection**: IP blocking after 5 failed attempts
- **🔐 Secure headers**: XSS, CSRF, Content-Type protection
- **🔑 Environment variables**: No hardcoded credentials
- **🔒 Session management**: Secure tokens with expiration
- **🌐 HTTPS enforced**: Automatic secure redirects

---

## 📊 Performance Metrics

| Metric | Value | Status |
|--------|--------|---------|
| **Uptime** | 99.267% | 🟢 Excellent |
| **Response Time** | <200ms | 🟢 Fast |
| **Quote Generation** | 101 completed | 🟢 Active |
| **Client Satisfaction** | 100% retention | 🟢 High |
| **Revenue Impact** | +60% conversion | 🟢 Positive |

---

## 🏢 Case Study

**Client**: NFS BÂTIMENT SASU
**Industry**: Construction & Renovation
**Location**: Nice, Alpes-Maritimes, France

### Business Challenge
- Manual quote generation taking 2+ hours per estimate
- Inefficient client communication and follow-up
- Limited visibility into business performance metrics
- Paper-based processes hindering growth scalability

### Technical Solution
- **Automated PDF generation** reducing quote time to 5 minutes
- **QR Code workflow** enabling instant client submissions
- **Real-time dashboard** providing business intelligence
- **Digital transformation** of entire client lifecycle

### Results Achieved
- **80% reduction** in administrative overhead
- **60% increase** in quote-to-contract conversion
- **100% client retention** rate improvement
- **Real-time insights** enabling data-driven decisions

---

## 🔧 Configuration

### Admin Panel Access
```
URL: /admin/dashboard
Features: Quote generation, client management, analytics
Security: Session-based authentication with IP protection
```

### API Endpoints
```
/api/generate-quote    # PDF quote generation
/api/submit-demande    # Client request submission
/api/qr-code          # QR code generation
/admin/security-status # Security diagnostics
```

---

## 🎯 Roadmap

- [ ] **Mobile app** for client interactions
- [ ] **Advanced analytics** with machine learning insights
- [ ] **Multi-language** support for international expansion
- [ ] **API integration** with accounting software
- [ ] **White-label** solution for other construction companies

---

## � Professional Services

**Developed by**: [Otmane Boulahia](https://zineinsight.com) - Senior Data Engineer
**Company**: ZineInsight - Digital Transformation Solutions
**Specialization**: Data Engineering, Business Intelligence, Automation

### Contact
- 🌐 **Portfolio**: [zineinsight.com](https://zineinsight.com)
- � **Email**: hello@zineinsight.com
- 💼 **LinkedIn**: [OtmaneZ](https://linkedin.com/in/otmanez)

---

## 📄 License

This project is proprietary software developed for NFS BÂTIMENT.

**© 2025 ZineInsight. All rights reserved.**

---

<div align="center">

**Built with ❤️ in Nice, France**

*Transforming traditional construction businesses through innovative digital solutions*

</div>