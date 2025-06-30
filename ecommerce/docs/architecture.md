# 電商網購網站架構設計文檔

## 系統架構概覽

### 1. 整體架構

```text
Frontend (Future)
     ↓
API Gateway/Load Balancer
     ↓
Django REST API Backend
     ↓
Database (SQLite/PostgreSQL)
```

### 2. 技術架構層次

- **表現層**: RESTful API 接口
- **業務邏輯層**: Django Views 和 Serializers
- **數據訪問層**: Django ORM
- **數據存儲層**: SQLite (開發) / PostgreSQL (生產)

## 應用模組設計

### 1. 核心應用 (Django Apps)

```text
ecommerce_backend/
├── ecommerce_backend/    # 主項目配置
├── users/               # 用戶管理應用
├── products/            # 商品管理應用 (待開發)
├── cart/               # 購物車應用 (待開發)
├── orders/             # 訂單管理應用 (待開發)
├── payments/           # 支付應用 (待開發)
└── common/             # 共用工具應用 (待開發)
```

### 2. 每個應用的責任

- **users**: 用戶註冊、認證、個人資料管理
- **products**: 商品 CRUD、分類管理、庫存管理
- **cart**: 購物車操作、會話管理
- **orders**: 訂單創建、狀態管理、歷史記錄
- **payments**: 支付處理、支付狀態管理
- **common**: 共用工具、中間件、裝飾器

## 數據庫設計

### 1. 數據庫選擇

- **開發環境**: SQLite (簡單、輕量)
- **生產環境**: PostgreSQL (性能、擴展性)

### 2. 主要數據表設計

#### 2.1 用戶相關表

```sql
-- 用戶表 (基於 Django User 擴展)
User (Django 內建)
├── id (主鍵)
├── username (用戶名)
├── email (郵箱)
├── password (密碼)
├── first_name (名)
├── last_name (姓)
├── is_active (是否激活)
├── is_staff (是否員工)
├── date_joined (註冊時間)
└── last_login (最後登入時間)

-- 用戶資料表 (一對一擴展)
UserProfile
├── id (主鍵)
├── user (外鍵 -> User)
├── phone (電話)
├── address (地址)
├── date_of_birth (生日)
└── avatar (頭像)
```

#### 2.2 商品相關表 (待實現)

```sql
-- 商品分類表
Category
├── id (主鍵)
├── name (分類名稱)
├── description (描述)
├── parent (外鍵 -> Category, 支持層級)
├── is_active (是否激活)
├── created_at (創建時間)
└── updated_at (更新時間)

-- 商品表
Product
├── id (主鍵)
├── name (商品名稱)
├── description (商品描述)
├── price (價格)
├── stock_quantity (庫存數量)
├── category (外鍵 -> Category)
├── sku (商品編號)
├── is_active (是否上架)
├── created_at (創建時間)
└── updated_at (更新時間)

-- 商品圖片表
ProductImage
├── id (主鍵)
├── product (外鍵 -> Product)
├── image (圖片路徑)
├── is_primary (是否主圖)
└── order (排序)
```

#### 2.3 購物車相關表 (待實現)

```sql
-- 購物車表
Cart
├── id (主鍵)
├── user (外鍵 -> User)
├── created_at (創建時間)
└── updated_at (更新時間)

-- 購物車商品表
CartItem
├── id (主鍵)
├── cart (外鍵 -> Cart)
├── product (外鍵 -> Product)
├── quantity (數量)
├── added_at (添加時間)
└── updated_at (更新時間)
```

#### 2.4 訂單相關表 (待實現)

```sql
-- 訂單表
Order
├── id (主鍵)
├── user (外鍵 -> User)
├── order_number (訂單號)
├── status (訂單狀態)
├── total_amount (總金額)
├── shipping_address (收貨地址)
├── created_at (創建時間)
└── updated_at (更新時間)

-- 訂單商品表
OrderItem
├── id (主鍵)
├── order (外鍵 -> Order)
├── product (外鍵 -> Product)
├── quantity (數量)
├── unit_price (單價)
└── subtotal (小計)
```

## API 設計架構

### 1. URL 結構設計

```text
/api/v1/
├── auth/              # 認證相關
│   ├── register/      # 用戶註冊
│   ├── login/         # 用戶登入
│   └── logout/        # 用戶登出
├── users/             # 用戶管理
│   ├── profile/       # 個人資料
│   └── {id}/          # 特定用戶
├── products/          # 商品管理
│   ├── categories/    # 分類管理
│   └── {id}/          # 特定商品
├── cart/              # 購物車
│   └── items/         # 購物車商品
├── orders/            # 訂單管理
│   └── {id}/          # 特定訂單
└── payments/          # 支付相關
```

### 2. 認證和授權架構

- **認證方式**: Token Authentication (可擴展到 JWT)
- **權限系統**: Django 內建權限 + 自定義權限
- **用戶角色**: 普通用戶、管理員

### 3. 響應格式標準

```json
{
    "success": true,
    "data": {},
    "message": "操作成功",
    "error_code": null,
    "timestamp": "2024-12-28T10:00:00Z"
}
```

## 安全架構

### 1. 認證安全

- 密碼加密 (Django 內建 PBKDF2)
- Token 過期機制
- 登入失敗次數限制

### 2. 數據安全

- 輸入驗證和清理
- SQL 注入防護 (Django ORM)
- XSS 防護
- CSRF 防護

### 3. API 安全

- HTTPS 強制 (生產環境)
- 請求頻率限制
- 敏感數據脫敏

## 性能優化架構

### 1. 數據庫優化

- 索引設計
- 查詢優化
- 連接池配置

### 2. 緩存策略

- Redis 緩存 (後期)
- 數據庫查詢緩存
- API 響應緩存

### 3. 擴展性設計

- 水平擴展支持
- 微服務準備
- 負載均衡考慮

## 部署架構

### 1. 開發環境

- Django 開發服務器
- SQLite 數據庫
- 本地文件存儲

### 2. 生產環境 (計劃)

- Gunicorn + Nginx
- PostgreSQL 數據庫
- Redis 緩存
- Docker 容器化

## 監控和日誌

### 1. 日誌設計

- 應用日誌
- 錯誤日誌
- 訪問日誌
- 安全日誌

### 2. 監控指標

- API 響應時間
- 錯誤率
- 併發用戶數
- 數據庫性能

## 更新記錄

- 2024-12-28: 創建架構設計文檔初版
