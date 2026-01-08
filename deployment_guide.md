# ระบบตรวจโครงงาน AI - คู่มือการ Deploy

## 📋 สารบัญ
1. [Local Development](#local-development)
2. [Heroku Deployment](#heroku-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Google Cloud Deployment](#google-cloud-deployment)
5. [AWS Deployment](#aws-deployment)

---

## Local Development

### ขั้นตอนที่ 1: ติดตั้ง Dependencies
```bash
# สร้าง virtual environment (optional)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# ติดตั้ง dependencies
pip install -r requirements.txt
```

### ขั้นตอนที่ 2: ตั้งค่า Environment Variables
```bash
# สร้างไฟล์ .env
cp .env.example .env

# แก้ไข .env และใส่ API Key ของคุณ
GOOGLE_API_KEY=your_api_key_here
```

### ขั้นตอนที่ 3: รันแอป
```bash
streamlit run student_view.py
```

แอปจะเปิดที่ `http://localhost:8502`

---

## Heroku Deployment

### ขั้นตอนที่ 1: ติดตั้ง Heroku CLI
- Download จาก [heroku.com/cli](https://devcenter.heroku.com/articles/heroku-cli)

### ขั้นตอนที่ 2: Login to Heroku
```bash
heroku login
```

### ขั้นตอนที่ 3: สร้าง Heroku App
```bash
heroku create your-app-name
```

### ขั้นตอนที่ 4: ตั้งค่า Environment Variables
```bash
heroku config:set GOOGLE_API_KEY=your_api_key_here
heroku config:set DATABASE_FILE=analysis.db
# สำหรับ Email (optional)
# heroku config:set EMAIL_SENDER=your-email@gmail.com
# heroku config:set EMAIL_PASSWORD=your-app-password
```

### ขั้นตอนที่ 5: Deploy to Heroku
```bash
# Commit changes
git add .
git commit -m "Ready for Heroku deployment"

# Push to Heroku
git push heroku main
```

### ขั้นตอนที่ 6: View Logs
```bash
heroku logs --tail
```

### URL ของแอป
```
https://your-app-name.herokuapp.com
```

---

## Docker Deployment

### ขั้นตอนที่ 1: Build Docker Image
```bash
docker build -t ai-grader:latest .
```

### ขั้นตอนที่ 2: Run Container Locally
```bash
docker run -p 8502:8502 \
  -e GOOGLE_API_KEY=your_api_key \
  -e DATABASE_FILE=analysis.db \
  ai-grader:latest
```

### ขั้นตอนที่ 3: Deploy to Docker Hub (Optional)
```bash
# Tag image
docker tag ai-grader:latest your-username/ai-grader:latest

# Push to Docker Hub
docker login
docker push your-username/ai-grader:latest
```

### ขั้นตอนที่ 4: Docker Compose (For Multi-Container Setup)
```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    image: ai-grader:latest
    ports:
      - "8502:8502"
    environment:
      GOOGLE_API_KEY: ${GOOGLE_API_KEY}
      DATABASE_FILE: analysis.db
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  # Database (Optional - for future SQLite shared storage)
  # db:
  #   image: postgres:15
  #   environment:
  #     POSTGRES_PASSWORD: password
  #   volumes:
  #     - postgres_data:/var/lib/postgresql/data

# volumes:
#   postgres_data:
```

Run with: `docker-compose up -d`

---

## Google Cloud Deployment

### ขั้นตอนที่ 1: Setup Google Cloud Project
```bash
gcloud projects create ai-grader-project
gcloud config set project ai-grader-project
gcloud auth login
```

### ขั้นตอนที่ 2: Deploy to Cloud Run
```bash
gcloud run deploy ai-grader \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=your_api_key
```

### ขั้นตอนที่ 3: Cloud Storage (For Database Backup)
```bash
gsutil mb gs://ai-grader-db
gsutil cp analysis.db gs://ai-grader-db/
```

---

## AWS Deployment

### ขั้นตอนที่ 1: Setup AWS Account
- ติดตั้ง AWS CLI
- Configure: `aws configure`

### ขั้นตอนที่ 2: Create EC2 Instance
```bash
# Launch EC2 instance (Ubuntu 22.04)
# Security group: Allow port 8502

# Connect to instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Install dependencies
sudo apt update
sudo apt install -y python3-pip git

# Clone repository
git clone your-repo-url
cd your-repo

# Install Python dependencies
pip3 install -r requirements.txt

# Run with PM2 (recommended)
sudo npm install -g pm2
pm2 start "streamlit run student_view.py" --name ai-grader
pm2 save
pm2 startup
```

### ขั้นตอนที่ 3: Setup with Nginx (Reverse Proxy)
```nginx
# /etc/nginx/sites-available/ai-grader
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8502;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/ai-grader /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

### ขั้นตอนที่ 4: SSL Certificate (with Let's Encrypt)
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## Environment Variables Configuration

สำหรับ production environment ให้ตั้งค่า:

```bash
# API Configuration
GOOGLE_API_KEY=your_google_api_key

# Database
DATABASE_FILE=analysis.db

# Email (optional)
EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-app-specific-password
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587

# Application
APP_TITLE=ระบบตรวจโครงงาน AI
DEBUG_MODE=False
```

---

## Performance Tips

1. **Database Optimization**
   ```bash
   # Use SQLite for small deployments
   # Migrate to PostgreSQL for larger scale
   ```

2. **Caching**
   - Enable Redis for session caching
   - Cache API responses

3. **Load Balancing**
   - Use Heroku Dynos
   - AWS Load Balancer
   - Google Cloud Load Balancing

4. **Monitoring**
   ```bash
   # Heroku
   heroku logs --tail

   # AWS CloudWatch
   aws logs tail /aws/ec2/ai-grader --follow

   # Google Cloud
   gcloud logs read --limit 50
   ```

---

## Backup & Recovery

### Database Backup
```bash
# Local backup
cp analysis.db analysis.db.backup

# Heroku backup
heroku pg:backups:capture

# Google Cloud Storage
gsutil cp analysis.db gs://ai-grader-db/backups/
```

### Recovery
```bash
# From local backup
cp analysis.db.backup analysis.db

# From Heroku
heroku pg:backups:restore DATABASE_URL <backup-id>

# From Cloud Storage
gsutil cp gs://ai-grader-db/backups/analysis.db .
```

---

## Troubleshooting

### Heroku Logs
```bash
heroku logs --tail --app your-app-name
heroku logs -n 100  # Last 100 lines
```

### Check App Status
```bash
heroku ps --app your-app-name
heroku config --app your-app-name
```

### Scale Dynos
```bash
heroku ps:scale web=1
heroku ps:scale web=3  # Scale up
```

### Restart App
```bash
heroku restart --app your-app-name
```

---

## Support & Documentation

- [Streamlit Deployment](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
- [Heroku Documentation](https://devcenter.heroku.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Google Cloud Documentation](https://cloud.google.com/docs)
- [AWS Documentation](https://docs.aws.amazon.com/)

---

**Last Updated**: December 14, 2025
**Version**: 1.0.0
