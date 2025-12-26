# Deployment Guide

## 🚀 Complete Deployment Instructions

This guide covers deploying both the **Streamlit Web Application** and the **Flask REST API** for production use.

---

## 📋 Prerequisites

- Python 3.8+
- pip package manager
- Git (optional, for version control)
- Virtual environment tool (recommended)

---

## 🔧 Initial Setup

### 1. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Verify Data File
Ensure `countries.csv` is in the `data/` directory.

---

## 🌐 Deploying Streamlit Application

### Local Development

```bash
cd deployment
streamlit run app.py
```

Access at: `http://localhost:8501`

### Production Deployment

#### Option 1: Streamlit Cloud (Recommended)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [streamlit.io/cloud](https://streamlit.io/cloud)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `deployment/app.py`
   - Click "Deploy"

3. **Configure Secrets (if needed)**
   - In Streamlit Cloud dashboard
   - Go to App settings → Secrets
   - Add any API keys or credentials

#### Option 2: Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "deployment/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t country-aid-clustering .
docker run -p 8501:8501 country-aid-clustering
```

#### Option 3: Heroku Deployment

1. **Create `setup.sh`**:
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

2. **Create `Procfile`**:
```
web: sh setup.sh && streamlit run deployment/app.py
```

3. **Deploy**:
```bash
heroku create your-app-name
git push heroku main
```

---

## 🔌 Deploying Flask API

### Local Development

```bash
cd deployment
python api.py
```

API available at: `http://localhost:5000`

### Production Deployment

#### Option 1: Using Gunicorn (Recommended for Production)

1. **Install Gunicorn**:
```bash
pip install gunicorn
```

2. **Run with Gunicorn**:
```bash
gunicorn --bind 0.0.0.0:5000 deployment.api:app
```

#### Option 2: Docker Deployment

Create `Dockerfile.api`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "deployment.api:app"]
```

Build and run:
```bash
docker build -f Dockerfile.api -t country-aid-api .
docker run -p 5000:5000 country-aid-api
```

#### Option 3: Heroku Deployment

1. **Create `Procfile.api`**:
```
web: gunicorn deployment.api:app
```

2. **Deploy**:
```bash
heroku create your-api-name
git push heroku main
```

#### Option 4: AWS EC2 Deployment

1. **Launch EC2 Instance** (Ubuntu recommended)

2. **SSH into instance**:
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

3. **Install dependencies**:
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

4. **Clone repository and setup**:
```bash
git clone <your-repo>
cd ClusteringCountriesAid
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

5. **Create systemd service** (`/etc/systemd/system/flask-api.service`):
```ini
[Unit]
Description=Flask API for Country Aid Clustering
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/ClusteringCountriesAid
Environment="PATH=/home/ubuntu/ClusteringCountriesAid/venv/bin"
ExecStart=/home/ubuntu/ClusteringCountriesAid/venv/bin/gunicorn --bind 0.0.0.0:5000 deployment.api:app

[Install]
WantedBy=multi-user.target
```

6. **Start service**:
```bash
sudo systemctl start flask-api
sudo systemctl enable flask-api
```

7. **Configure Nginx** (`/etc/nginx/sites-available/api`):
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

8. **Enable and restart Nginx**:
```bash
sudo ln -s /etc/nginx/sites-available/api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🐳 Docker Compose (Both Services)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  streamlit:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    restart: unless-stopped

  flask-api:
    build:
      context: .
      dockerfile: Dockerfile.api
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    restart: unless-stopped
```

Run both:
```bash
docker-compose up -d
```

---

## 🔐 Security Considerations

### API Security

1. **Add API Key Authentication**:

Add to `api.py`:
```python
from functools import wraps
from flask import request

API_KEY = os.getenv('API_KEY', 'your-secret-key')

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('X-API-Key') != API_KEY:
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Apply to routes
@app.route('/predict', methods=['POST'])
@require_api_key
def predict():
    # ...
```

2. **Enable HTTPS**:
- Use Let's Encrypt for SSL certificates
- Configure Nginx for HTTPS

3. **Rate Limiting**:
```bash
pip install flask-limiter
```

Add to `api.py`:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

### Streamlit Security

1. **Authentication** (Streamlit Cloud):
- Enable in app settings
- Restrict to GitHub organization

2. **Environment Variables**:
Use `.streamlit/secrets.toml` for sensitive data

---

## 📊 Monitoring & Logging

### Application Logging

Update `config.py` logging settings:
```python
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'log_file': '/var/log/country-aid/app.log'
}
```

### Performance Monitoring

1. **Add Application Insights** (for Flask):
```bash
pip install applicationinsights
```

2. **Use Monitoring Services**:
- Datadog
- New Relic
- AWS CloudWatch

---

## 🔄 CI/CD Pipeline

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: |
        pytest tests/

    - name: Deploy to Heroku
      env:
        HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}
      run: |
        git push https://heroku:$HEROKU_API_KEY@git.heroku.com/your-app.git main
```

---

## 🧪 Testing Deployment

### Test Streamlit App
```bash
curl http://localhost:8501
```

### Test Flask API

**Health Check**:
```bash
curl http://localhost:5000/health
```

**Prediction**:
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "child_mort": 25.0,
    "exports": 28.5,
    "health": 5.2,
    "imports": 32.1,
    "income": 8500.0,
    "inflation": 6.3,
    "life_expec": 68.5,
    "total_fer": 3.1,
    "gdpp": 7200.0
  }'
```

---

## 📈 Scaling Considerations

### Horizontal Scaling

1. **Load Balancer**: Use Nginx or cloud load balancers
2. **Multiple Instances**: Deploy multiple API instances
3. **Database**: If adding data persistence, use PostgreSQL/MySQL
4. **Caching**: Implement Redis for model caching

### Performance Optimization

1. **Model Caching**: Cache loaded models in memory
2. **Data Caching**: Cache preprocessed data
3. **Async Processing**: Use Celery for long-running tasks
4. **CDN**: Serve static assets via CDN

---

## 🆘 Troubleshooting

### Common Issues

**Issue**: Port already in use
```bash
# Find process
lsof -i :5000
# Kill process
kill -9 <PID>
```

**Issue**: Module not found
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

**Issue**: Data file not found
- Check data path in `config.py`
- Ensure `countries.csv` exists in `data/`

---

## 📞 Support & Maintenance

### Regular Maintenance Tasks

1. **Update Dependencies**:
```bash
pip list --outdated
pip install --upgrade <package>
pip freeze > requirements.txt
```

2. **Monitor Logs**:
```bash
tail -f logs/app.log
```

3. **Backup Models**:
```bash
tar -czf models-backup-$(date +%Y%m%d).tar.gz models/
```

4. **Database Backups** (if applicable)

---

## ✅ Deployment Checklist

- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] Data file in correct location
- [ ] Configuration updated for production
- [ ] Environment variables set
- [ ] Tests passing
- [ ] Security measures implemented
- [ ] Logging configured
- [ ] Monitoring set up
- [ ] Backup strategy in place
- [ ] Documentation updated
- [ ] Team trained on deployment process

---

## 🎉 Success!

Your Country Aid Clustering application is now deployed!

**Streamlit App**: Interactive dashboard for stakeholders
**Flask API**: RESTful service for programmatic access

For questions or issues, refer to the main [README.md](README.md) or create an issue in the repository.
