# 🛒 E-Commerce Django REST API

> **現代化電商後端系統** - 基於 Django REST Framework 與 MySQL

📅 **最後更新**: 2025 年 6 月 22 日  
🏗️ **專案狀態**: 開發中 (基礎架構階段)  
👨‍💻 **開發者**: joh

---

## 📊 專案概覽

### 🎯 專案目標

打造一個功能完整的電商平台後端 API 系統，支持用戶管理、商品管理、購物車、訂單處理等核心電商功能。

### 🏗️ 技術架構

- **後端框架**: Django 5.1.7 + Django REST Framework
- **資料庫**: MySQL 8.0
- **認證系統**: JWT (Simple JWT)
- **API 文檔**: 計劃使用 Swagger/OpenAPI
- **容器化**: Docker (計劃中)

---

## 📈 開發進度追蹤

### ✅ 已完成功能

- [x] **基礎架構搭建** (2025-06-22)
  - Django 專案初始化
  - MySQL 資料庫連接配置
  - 虛擬環境設置
- [x] **用戶系統基礎** (2025-06-22)
  - 自定義 User 模型 (擴展 AbstractUser)
  - 用戶角色系統 (Admin, Customer, Staff, Guest)
  - 性別、生日等額外欄位
  - JWT 認證配置

### 🔄 進行中

- [ ] **用戶認證 API**
  - [ ] 用戶註冊 API
  - [ ] 用戶登入 API
  - [ ] Token 刷新機制
  - [ ] 用戶資料更新 API

### 📋 待開發功能

#### 🏪 **核心業務模組**

- [ ] **商品管理系統**

  - [ ] Product 模型設計
  - [ ] 商品分類系統
  - [ ] 商品圖片上傳
  - [ ] 商品 CRUD API
  - [ ] 商品搜索與篩選

- [ ] **購物車系統**

  - [ ] Cart 模型設計
  - [ ] 購物車 API
  - [ ] 商品數量管理
  - [ ] 購物車同步機制

- [ ] **訂單管理系統**
  - [ ] Order 模型設計
  - [ ] 訂單狀態管理
  - [ ] 訂單歷史查詢
  - [ ] 訂單統計功能

#### 🔧 **系統功能**

- [ ] **支付集成**

  - [ ] 支付介面設計
  - [ ] 第三方支付集成
  - [ ] 支付狀態追蹤

- [ ] **權限與安全**

  - [ ] 基於角色的權限控制
  - [ ] API 限流機制
  - [ ] 資料驗證強化

- [ ] **系統優化**
  - [ ] 資料庫查詢優化
  - [ ] 快取機制
  - [ ] 日誌系統
  - [ ] 錯誤處理機制

---

## 🗂️ 專案結構

```text
ecommerce/
├── docs/                           # 專案文檔
│   ├── README.md                   # 本文件
│   └── temp.md                     # 臨時筆記
├── ecommerce_backend/              # Django 專案根目錄
│   ├── ecommerce_backend/          # 專案設定
│   │   ├── settings.py             # 專案配置 ⚙️
│   │   ├── urls.py                 # 主要路由
│   │   └── ...
│   ├── users/                      # 用戶管理應用 ✅
│   │   ├── models.py               # 自定義用戶模型
│   │   ├── views.py                # API 視圖 (待開發)
│   │   └── ...
│   └── manage.py                   # Django 管理腳本
└── venv/                           # Python 虛擬環境
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- MySQL 8.0+
- Git

### Environment Setup

1. **Activate Virtual Environment**

```bash
cd /home/joh/Workspace/python_projects/ecommerce
source venv/bin/activate
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Database Migration**

```bash
cd ecommerce_backend
python manage.py makemigrations
python manage.py migrate
```

4. **Create Superuser**

```bash
python manage.py createsuperuser
```

5. **Start Development Server**

```bash
python manage.py runserver
```

### Common Issues & Solutions

**Error: `ModuleNotFoundError: No module named 'django'`**

- Cause: Virtual environment not activated
- Solution: Run `source venv/bin/activate` first

**Error: `ModuleNotFoundError: No module named 'corsheaders'`**

- Cause: Missing dependencies
- Solution: Run `pip install -r requirements.txt`

### Development Tips

- Always activate virtual environment before development
- Update `requirements.txt` when adding new dependencies
- Server will be available at: `http://127.0.0.1:8000/`

---

## 🎯 當前開發計劃

### 🔥 **本週目標** (2025 年 6 月 22 日 - 6 月 29 日)

1. **完善用戶認證系統**

   - 實現註冊/登入 API
   - 創建用戶序列化器
   - 添加 API 文檔

2. **建立專案依賴管理**

   - 創建 requirements.txt
   - 設置開發環境文檔

3. **開始商品模型設計**
   - 設計 Product 模型
   - 規劃商品分類系統

### 📅 **下週計劃** (6 月 30 日 - 7 月 6 日)

- 實現商品管理 API
- 設計購物車系統
- 前端技術方案選擇

---

## 🔗 API 端點 (計劃中)

### 認證相關

- `POST /api/auth/register/` - 用戶註冊
- `POST /api/auth/login/` - 用戶登入
- `POST /api/auth/refresh/` - Token 刷新
- `POST /api/auth/logout/` - 用戶登出

### 用戶管理

- `GET /api/users/profile/` - 獲取用戶資料
- `PUT /api/users/profile/` - 更新用戶資料

### 商品管理 (待開發)

- `GET /api/products/` - 商品列表
- `POST /api/products/` - 創建商品 (管理員)
- `GET /api/products/{id}/` - 商品詳情
- `PUT /api/products/{id}/` - 更新商品
- `DELETE /api/products/{id}/` - 刪除商品

---

## 📝 Development Notes

### 2025-06-22

- ✅ Completed initial project structure analysis
- ✅ Refactored README.md into practical project documentation
- ✅ Created requirements.txt file
- ✅ **Successfully started Django development server**
  - Learned virtual environment activation process
  - Resolved dependency installation issues
  - Server running at http://127.0.0.1:8000/
- ✅ Implemented complete user authentication system
  - User registration API (with password validation & email uniqueness check)
  - User login API (supports username or email login)
  - User profile view & update API
  - Change password API
  - User logout API (with token blacklist support)
  - User dashboard API (reserved for statistics data)
- ✅ Configured JWT authentication system
- ✅ Set up CORS support (prepared for frontend)
- ✅ Created API testing script
- ✅ Completed URL routing configuration

### Completed API Endpoints

- `GET /api/` - API root endpoint
- `POST /api/users/auth/register/` - User registration
- `POST /api/users/auth/login/` - User login
- `POST /api/users/auth/logout/` - User logout
- `POST /api/users/auth/refresh/` - Token refresh
- `GET/PUT /api/users/profile/` - User profile
- `POST /api/users/change-password/` - Change password
- `GET /api/users/dashboard/` - User dashboard

### Known Issues

- [x] ~~Missing requirements.txt file~~ ✅ Resolved
- [x] ~~users/views.py mostly empty, need to implement API views~~ ✅ Resolved
- [x] ~~Missing URL routing configuration~~ ✅ Resolved
- [x] ~~No CORS support setup (frontend preparation)~~ ✅ Resolved
- [x] ~~Server startup issues~~ ✅ Resolved
- [ ] Need to test database connection and user models
- [ ] Need to create product management module

---

## 🤝 貢獻指南

這是個人學習專案，目前由單人開發。歡迎建議與反饋！

---

## 📞 聯絡資訊

如有問題或建議，請透過以下方式聯絡：

- 開發者: joh
- 專案位置: `/home/joh/Workspace/python_projects/ecommerce/`

---

_⚡ 讓我們一步步建構這個現代化的電商平台！_
