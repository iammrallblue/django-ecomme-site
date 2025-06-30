# 部署文檔

## 部署環境概覽

### 環境分類

1. **開發環境** (Development)
   - 本地開發機器
   - Django 開發服務器
   - SQLite 數據庫

2. **測試環境** (Staging) - 計劃中
   - 模擬生產環境
   - 用於功能測試和集成測試

3. **生產環境** (Production) - 計劃中
   - 實際服務環境
   - 高可用性和性能要求

## 開發環境部署

### 1. 系統要求

- **操作系統**: Linux/macOS/Windows
- **Python 版本**: 3.8+
- **Node.js**: 16+ (前端開發時需要)
- **Git**: 最新版本

### 2. 環境配置步驟

#### 2.1 克隆項目

```bash
git clone <repository-url>
cd ecommerce_backend
```

#### 2.2 創建虛擬環境

```bash
# Linux/macOS
python3 -m venv ecommerce_env
source ecommerce_env/bin/activate

# Windows
python -m venv ecommerce_env
ecommerce_env\Scripts\activate
```

#### 2.3 安裝依賴

```bash
pip install -r requirements.txt
```

#### 2.4 環境變量配置

創建 `.env` 文件:

```bash
# .env 文件 (開發環境)
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

#### 2.5 數據庫初始化

```bash
cd ecommerce_backend
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

#### 2.6 啟動開發服務器

```bash
python manage.py runserver
```

### 3. 開發環境驗證

訪問以下端點驗證部署成功:

- `http://localhost:8000/admin/` - 管理界面
- `http://localhost:8000/api/v1/` - API 根端點

## 測試環境部署 (計劃)

### 1. Docker 容器化

#### 1.1 Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ecommerce_backend.wsgi:application"]
```

#### 1.2 docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://user:password@db:5432/ecommerce
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: ecommerce
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### 2. 測試環境配置

```bash
# 環境變量 (測試環境)
DEBUG=False
SECRET_KEY=test-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/ecommerce_test
REDIS_URL=redis://localhost:6379/0
ALLOWED_HOSTS=test.example.com
```

## 生產環境部署 (計劃)

### 1. 服務器要求

- **CPU**: 2+ 核心
- **內存**: 4GB+
- **存儲**: 50GB+ SSD
- **網絡**: 公網 IP 和域名

### 2. 技術棧

- **Web 服務器**: Nginx
- **WSGI 服務器**: Gunicorn
- **數據庫**: PostgreSQL
- **緩存**: Redis
- **容器化**: Docker + Docker Compose
- **反向代理**: Nginx
- **SSL**: Let's Encrypt

### 3. 部署架構

```
Internet
    ↓
Nginx (反向代理 + SSL)
    ↓
Gunicorn (Django 應用)
    ↓
PostgreSQL (主數據庫)
    ↓
Redis (緩存)
```

### 4. Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /app/staticfiles/;
    }

    location /media/ {
        alias /app/media/;
    }
}
```

### 5. 生產環境配置

```bash
# 環境變量 (生產環境)
DEBUG=False
SECRET_KEY=super-secure-production-key
DATABASE_URL=postgresql://prod_user:prod_password@localhost:5432/ecommerce_prod
REDIS_URL=redis://localhost:6379/0
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
```

## 部署清單

### 開發環境部署清單

- [ ] Python 虛擬環境創建
- [ ] 依賴包安裝
- [ ] 環境變量配置
- [ ] 數據庫遷移
- [ ] 超級用戶創建
- [ ] 開發服務器啟動
- [ ] API 端點測試

### 生產環境部署清單 (計劃)

- [ ] 服務器環境準備
- [ ] Docker 和 Docker Compose 安裝
- [ ] PostgreSQL 配置
- [ ] Redis 配置
- [ ] Nginx 配置
- [ ] SSL 證書配置
- [ ] 環境變量設置
- [ ] 靜態文件收集
- [ ] 數據庫遷移
- [ ] 服務啟動
- [ ] 監控配置
- [ ] 備份策略實施

## 監控和維護

### 1. 日誌管理

- **應用日誌**: Django 日誌配置
- **訪問日誌**: Nginx 訪問日誌
- **錯誤日誌**: 應用和服務器錯誤日誌
- **日誌輪轉**: logrotate 配置

### 2. 監控指標

- **服務可用性**: uptime 監控
- **響應時間**: API 響應時間監控
- **資源使用**: CPU、內存、磁盤使用率
- **數據庫性能**: 查詢時間、連接數

### 3. 備份策略

- **數據庫備份**: 每日自動備份
- **文件備份**: 用戶上傳文件備份
- **配置備份**: 服務器配置文件備份
- **代碼備份**: Git 倉庫備份

### 4. 安全措施

- **防火牆配置**: 只開放必要端口
- **SSL/TLS**: HTTPS 強制使用
- **數據庫安全**: 限制數據庫訪問權限
- **定期更新**: 系統和依賴包更新

## 故障排除

### 常見問題

1. **數據庫連接失敗**
   - 檢查數據庫服務狀態
   - 驗證連接字符串
   - 檢查網絡連接

2. **靜態文件載入失敗**
   - 檢查 STATIC_URL 配置
   - 執行 collectstatic 命令
   - 驗證 Nginx 配置

3. **API 響應慢**
   - 檢查數據庫查詢性能
   - 監控服務器資源使用
   - 優化代碼邏輯

## 持續集成/持續部署 (CI/CD) - 計劃

### GitHub Actions 配置示例

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          python manage.py test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to server
        run: |
          # 部署腳本
```

## 更新記錄

- 2024-12-28: 創建部署文檔初版
