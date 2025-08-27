# 🤝 Contributing to BTP Automation System

> **Professional contribution guidelines for enterprise-grade development**

Thank you for your interest in contributing to the **BTP Automation System**! This document provides comprehensive guidelines for developers, data engineers, and security professionals who want to contribute to this enterprise construction management platform.

---

## 🎯 Code of Conduct

By participating in this project, you agree to maintain professional standards and follow our **[Code of Conduct](CODE_OF_CONDUCT.md)**. We are committed to providing a welcoming and inclusive environment for all contributors.

---

## 🚀 Getting Started

### Prerequisites

Before contributing, ensure you have the following installed:

```bash
# Required Software
- Python 3.11+ (recommended 3.12)
- Git 2.30+
- Docker & Docker Compose (optional)
- Node.js 18+ (for frontend tooling)

# Development Tools
- VS Code or PyCharm Professional
- GitHub CLI (optional but recommended)
```

### Development Environment Setup

1. **Fork the repository**
   ```bash
   gh repo fork OtmaneZ/btp-automation-system
   cd btp-automation-system
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # .venv\Scripts\activate   # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your local configuration
   ```

5. **Initialize database**
   ```bash
   python -c "
   from app import app, db
   with app.app_context():
       db.create_all()
       print('✅ Database initialized')
   "
   ```

6. **Run the application**
   ```bash
   python app.py
   # Application available at http://localhost:5000
   ```

---

## 🏗️ Development Workflow

### Branch Strategy

We follow **GitFlow** workflow with the following branch structure:

```
main            # Production-ready code
├── develop     # Integration branch for features
├── feature/*   # New features
├── hotfix/*    # Production bug fixes
├── release/*   # Release preparation
└── chore/*     # Maintenance tasks
```

### Creating a Contribution

1. **Create a feature branch**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, documented code
   - Follow our coding standards (see below)
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Run automated tests
   pytest

   # Check code quality
   black .
   flake8 .
   bandit -r .

   # Run security checks
   safety check
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add client analytics dashboard

   - Implement real-time KPI tracking
   - Add Chart.js visualizations
   - Include export functionality

   Closes #123"
   ```

5. **Push and create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   gh pr create --title "feat: add client analytics dashboard" --body "Description of changes"
   ```

---

## 📝 Coding Standards

### Python Code Style

We follow **PEP 8** with these specific guidelines:

```python
# ✅ Good
def generate_quote_pdf(client_data: dict, services: List[str]) -> str:
    """
    Generate a professional PDF quote for construction services.

    Args:
        client_data (dict): Client information including name, contact
        services (List[str]): List of requested services

    Returns:
        str: Path to generated PDF file

    Raises:
        ValidationError: If client data is invalid
    """
    try:
        # Implementation here
        return pdf_path
    except Exception as e:
        logger.error(f"PDF generation failed: {e}")
        raise

# ❌ Avoid
def gen_pdf(data,svcs):
    # No docstring, unclear variable names
    return "some_file.pdf"
```

### Code Formatting

**Required tools** (run before each commit):

```bash
# Auto-formatting
black .                    # Python code formatting
isort .                    # Import sorting

# Linting
flake8 .                   # Style guide enforcement
pylint app.py             # Advanced static analysis

# Security
bandit -r .               # Security issue detection
safety check              # Dependency vulnerability scan
```

### Database Migrations

For database changes, follow this pattern:

```python
# migrations/001_add_client_analytics.py
from flask_migrate import upgrade, downgrade

def upgrade():
    """Add analytics table for client metrics."""
    op.create_table(
        'client_analytics',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('client_id', sa.Integer, sa.ForeignKey('clients.id')),
        sa.Column('metric_name', sa.String(100), nullable=False),
        sa.Column('metric_value', sa.Float, nullable=False),
        sa.Column('recorded_at', sa.DateTime, default=datetime.utcnow)
    )

def downgrade():
    """Remove analytics table."""
    op.drop_table('client_analytics')
```

---

## 🧪 Testing Guidelines

### Test Structure

We use **pytest** with comprehensive test coverage:

```python
# tests/test_quote_generation.py
import pytest
from app import app, db
from models import Client, Quote

class TestQuoteGeneration:
    """Test suite for PDF quote generation functionality."""

    @pytest.fixture
    def client_data(self):
        """Sample client data for testing."""
        return {
            'name': 'Test Construction Ltd',
            'email': 'test@construction.com',
            'phone': '+33 1 23 45 67 89',
            'address': '123 Test Street, Nice, France'
        }

    def test_quote_generation_success(self, client_data):
        """Test successful PDF quote generation."""
        with app.test_client() as client:
            response = client.post('/admin/generate-quote',
                                 json=client_data)
            assert response.status_code == 200
            assert 'pdf_url' in response.json

    def test_quote_generation_invalid_data(self):
        """Test quote generation with invalid data."""
        with app.test_client() as client:
            response = client.post('/admin/generate-quote',
                                 json={'invalid': 'data'})
            assert response.status_code == 400
```

### Test Categories

1. **Unit Tests**: Test individual functions and methods
2. **Integration Tests**: Test component interactions
3. **End-to-End Tests**: Test complete user workflows
4. **Performance Tests**: Load and stress testing
5. **Security Tests**: Authentication and authorization

### Running Tests

```bash
# All tests with coverage
pytest --cov=. --cov-report=html

# Specific test categories
pytest tests/unit/           # Unit tests only
pytest tests/integration/    # Integration tests
pytest tests/e2e/           # End-to-end tests

# Performance testing
locust --host=http://localhost:5000
```

---

## 🔒 Security Guidelines

### Secure Coding Practices

1. **Input Validation**
   ```python
   from wtforms import validators

   class ClientForm(FlaskForm):
       email = StringField('Email', [
           validators.Email(message='Invalid email address'),
           validators.Length(max=255)
       ])
       phone = StringField('Phone', [
           validators.Regexp(r'^\+[1-9]\d{1,14}$',
                           message='Invalid phone format')
       ])
   ```

2. **SQL Injection Prevention**
   ```python
   # ✅ Use parameterized queries
   clients = Client.query.filter_by(email=email).all()

   # ❌ Never use string concatenation
   # cursor.execute(f"SELECT * FROM clients WHERE email = '{email}'")
   ```

3. **XSS Protection**
   ```python
   from markupsafe import escape

   @app.route('/client/<name>')
   def client_profile(name):
       safe_name = escape(name)
       return render_template('client.html', name=safe_name)
   ```

### Security Checklist

Before submitting any code:

- [ ] All user inputs are validated and sanitized
- [ ] No hardcoded secrets or credentials
- [ ] Database queries use parameterization
- [ ] Authentication and authorization checks are in place
- [ ] Security headers are properly configured
- [ ] Error messages don't expose sensitive information

---

## 📊 Data Engineering Contributions

### Database Design

Follow these principles for database modifications:

1. **Normalization**: Minimize data redundancy
2. **Indexing**: Add indexes for frequently queried columns
3. **Constraints**: Use foreign keys and check constraints
4. **Documentation**: Document all schema changes

```sql
-- Example: Adding analytics table
CREATE TABLE client_analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER REFERENCES clients(id) ON DELETE CASCADE,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(10,2) NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Indexes for performance
    INDEX idx_client_analytics_client_id (client_id),
    INDEX idx_client_analytics_date (recorded_at),
    INDEX idx_client_analytics_metric (metric_name)
);
```

### Analytics & Reporting

When adding new analytics features:

1. **Performance**: Use database views for complex queries
2. **Caching**: Implement Redis caching for expensive operations
3. **Batch Processing**: Use background tasks for heavy computations
4. **Data Validation**: Ensure data quality and consistency

---

## 📚 Documentation Standards

### Code Documentation

```python
def calculate_project_cost(
    services: List[str],
    client_type: str,
    urgency_factor: float = 1.0
) -> Dict[str, Union[float, str]]:
    """
    Calculate total project cost based on services and client parameters.

    This function implements the core pricing algorithm for construction
    projects, taking into account service complexity, client history,
    and urgency requirements.

    Args:
        services (List[str]): List of service codes (e.g., ['DEMO', 'RENO'])
        client_type (str): Client category ('individual', 'commercial', 'industrial')
        urgency_factor (float, optional): Multiplier for urgent projects. Defaults to 1.0.

    Returns:
        Dict[str, Union[float, str]]: Dictionary containing:
            - 'total_cost': Total project cost in EUR
            - 'breakdown': Detailed cost breakdown
            - 'estimated_duration': Project duration in days
            - 'quote_reference': Unique quote identifier

    Raises:
        ValueError: If services list is empty or contains invalid codes
        TypeError: If urgency_factor is not a number

    Example:
        >>> calculate_project_cost(['DEMO', 'RENO'], 'commercial', 1.5)
        {
            'total_cost': 15750.0,
            'breakdown': 'Demolition: €7500, Renovation: €7500, Urgency: +50%',
            'estimated_duration': 12,
            'quote_reference': 'QUO-2025-001'
        }

    Note:
        This function uses the current pricing matrix stored in the database.
        Prices are automatically updated based on market conditions.
    """
```

### API Documentation

Use OpenAPI/Swagger format for API endpoints:

```python
@app.route('/api/quotes', methods=['POST'])
def create_quote():
    """
    Create a new construction quote.
    ---
    tags:
      - Quotes
    parameters:
      - in: body
        name: quote_data
        description: Quote information
        required: true
        schema:
          type: object
          required:
            - client_name
            - services
          properties:
            client_name:
              type: string
              example: "NFS BÂTIMENT Client"
            services:
              type: array
              items:
                type: string
              example: ["demolition", "renovation"]
    responses:
      201:
        description: Quote created successfully
        schema:
          type: object
          properties:
            quote_id:
              type: string
              example: "QUO-2025-001"
            pdf_url:
              type: string
              example: "/static/quotes/quote-001.pdf"
      400:
        description: Invalid input data
    """
```

---

## 🔄 Pull Request Process

### PR Requirements

Every Pull Request must include:

1. **Clear Description**: Explain what changes were made and why
2. **Issue Reference**: Link to related GitHub issues
3. **Test Coverage**: Include tests for new functionality
4. **Documentation**: Update relevant documentation
5. **Screenshots**: For UI changes, include before/after images

### PR Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Security scan completed

## Screenshots (if applicable)
[Include screenshots for UI changes]

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes

## Related Issues
Closes #[issue_number]
```

### Review Process

1. **Automated Checks**: All CI/CD pipeline tests must pass
2. **Code Review**: At least one maintainer approval required
3. **Security Review**: Security-sensitive changes need security team approval
4. **Performance Review**: Changes affecting performance need benchmarking

---

## 🎯 Contribution Areas

### High Priority Areas

1. **Performance Optimization**
   - Database query optimization
   - Caching implementation
   - Frontend loading speed improvements

2. **Security Enhancements**
   - Advanced authentication (2FA)
   - API rate limiting
   - Security monitoring

3. **Analytics & Reporting**
   - Advanced dashboard features
   - Export capabilities
   - Predictive analytics

4. **Client Experience**
   - Mobile responsiveness
   - Accessibility improvements
   - User interface enhancements

### Data Engineering Focus Areas

1. **ETL Pipelines**
   - Client data import/export
   - Analytics data processing
   - Automated reporting

2. **Database Architecture**
   - Performance optimization
   - Scalability improvements
   - Data quality monitoring

3. **Business Intelligence**
   - Advanced KPI calculations
   - Forecasting algorithms
   - Market trend analysis

---

## 📞 Getting Help

### Community Support

- **GitHub Discussions**: For general questions and ideas
- **GitHub Issues**: For bug reports and feature requests
- **Email**: `hello@zineinsight.com` for private inquiries

### Maintainers

- **Lead Developer**: Otmane Boulahia ([@OtmaneZ](https://github.com/OtmaneZ))
- **Security Team**: `security@zineinsight.com`
- **Data Engineering**: `data@zineinsight.com`

### Development Resources

- **Architecture Documentation**: `/docs/architecture/`
- **API Documentation**: `/docs/api/`
- **Database Schema**: `/docs/database/`
- **Deployment Guide**: `/docs/deployment/`

---

## 🏆 Recognition

Contributors will be recognized in:

- **README.md**: Contributors section
- **CHANGELOG.md**: Release notes
- **GitHub**: Contributor insights
- **Professional Network**: LinkedIn recommendations for significant contributions

---

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project.

---

<div align="center">

**🤝 Thank you for contributing to BTP Automation System!**

*Building the future of construction management together*

**© 2025 ZineInsight. Professional development community.**

</div>
