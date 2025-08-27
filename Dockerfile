# ============================================
# BTP Automation System - Production Docker
# ============================================
# Multi-stage build for optimal security & performance
# Built for enterprise deployment standards

# ==========================================
# Stage 1: Python Dependencies Builder
# ==========================================
FROM python:3.12-slim as builder

LABEL maintainer="Otmane Boulahia <hello@zineinsight.com>"
LABEL description="BTP Automation System - Enterprise Construction Management"
LABEL version="2.0"

# Set build arguments
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION

# Add metadata
LABEL org.label-schema.build-date=$BUILD_DATE \
    org.label-schema.name="BTP Automation System" \
    org.label-schema.description="Enterprise-grade construction management platform" \
    org.label-schema.url="https://nfs-batiment-devis.onrender.com" \
    org.label-schema.vcs-ref=$VCS_REF \
    org.label-schema.vcs-url="https://github.com/OtmaneZ/btp-automation-system" \
    org.label-schema.vendor="ZineInsight" \
    org.label-schema.version=$VERSION \
    org.label-schema.schema-version="1.0"

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create application user and directory
RUN groupadd -r appuser && useradd -r -g appuser appuser
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ==========================================
# Stage 2: Production Runtime
# ==========================================
FROM python:3.12-slim as production

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Create app directory with proper permissions
WORKDIR /app
RUN chown -R appuser:appuser /app

# Copy Python packages from builder stage
COPY --from=builder /root/.local /home/appuser/.local
RUN chown -R appuser:appuser /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser . .

# Create necessary directories with proper permissions
RUN mkdir -p /app/uploads /app/static/qr_codes /app/instance \
    && chown -R appuser:appuser /app/uploads /app/static /app/instance

# Switch to non-root user
USER appuser

# Set environment variables
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Security: Remove sensitive files
RUN rm -f .env .env.example .env.production 2>/dev/null || true

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-5000}/health || exit 1

# Expose port (will be set by Render.com)
EXPOSE $PORT

# Production startup command with Gunicorn
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 4 --worker-class gthread --max-requests 1000 --max-requests-jitter 100 --preload --log-level info --access-logfile - --error-logfile - app:app"]

# ==========================================
# Stage 3: Development Environment
# ==========================================
FROM production as development

USER root

# Install development dependencies
RUN apt-get update && apt-get install -y \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Install development Python packages
RUN pip install --no-cache-dir \
    pytest \
    pytest-cov \
    pytest-flask \
    black \
    flake8 \
    bandit \
    safety

USER appuser

# Development startup (with hot reload)
CMD ["python", "app.py"]
