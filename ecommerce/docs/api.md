# API 文檔

## API 概覽

### 基礎信息

- **基礎 URL**: `http://localhost:8000/api/v1/`
- **認證方式**: Token Authentication
- **響應格式**: JSON
- **字符編碼**: UTF-8

### 響應格式標準

```json
{
    "success": true,
    "data": {},
    "message": "操作成功",
    "error_code": null,
    "timestamp": "2024-12-28T10:00:00Z"
}
```

### 錯誤響應格式

```json
{
    "success": false,
    "data": null,
    "message": "錯誤描述",
    "error_code": "ERROR_CODE",
    "errors": {
        "field_name": ["具體錯誤信息"]
    },
    "timestamp": "2024-12-28T10:00:00Z"
}
```

### HTTP 狀態碼

- `200 OK`: 請求成功
- `201 Created`: 資源創建成功
- `400 Bad Request`: 請求參數錯誤
- `401 Unauthorized`: 未認證
- `403 Forbidden`: 無權限
- `404 Not Found`: 資源不存在
- `500 Internal Server Error`: 服務器錯誤

## 認證 API

### 1. 用戶註冊

```sh
POST /api/v1/auth/register/
```

**請求參數**:

```json
{
    "username": "string",
    "email": "string",
    "password": "string",
    "password_confirm": "string"
}
```

**響應示例**:

```json
{
    "success": true,
    "data": {
        "user": {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com"
        },
        "token": "abc123..."
    },
    "message": "註冊成功"
}
```

### 2. 用戶登入

```sh
POST /api/v1/auth/login/
```

**請求參數**:

```json
{
    "username": "string",
    "password": "string"
}
```

**響應示例**:

```json
{
    "success": true,
    "data": {
        "user": {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com"
        },
        "token": "abc123..."
    },
    "message": "登入成功"
}
```

### 3. 用戶登出

```sh
POST /api/v1/auth/logout/
```

**請求頭**:

```sh
Authorization: Token abc123...
```

**響應示例**:

```json
{
    "success": true,
    "data": null,
    "message": "登出成功"
}
```

## 用戶管理 API

### 1. 獲取用戶個人資料

```sh
GET /api/v1/users/profile/
```

**請求頭**:

```sh
Authorization: Token abc123...
```

**響應示例**:

```json
{
    "success": true,
    "data": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "profile": {
            "phone": "+1234567890",
            "address": "123 Main St"
        }
    },
    "message": "獲取成功"
}
```

### 2. 更新用戶個人資料

```sh
PUT /api/v1/users/profile/
```

**請求頭**:

```sh
Authorization: Token abc123...
```

**請求參數**:

```json
{
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "profile": {
        "phone": "string",
        "address": "string"
    }
}
```

**響應示例**:

```json
{
    "success": true,
    "data": {
        "id": 1,
        "username": "testuser",
        "email": "new@example.com",
        "first_name": "New",
        "last_name": "Name"
    },
    "message": "更新成功"
}
```

## 商品管理 API (待實現)

### 1. 獲取商品列表

```sh
GET /api/v1/products/
```

**查詢參數**:

- `page`: 頁碼 (默認: 1)
- `page_size`: 每頁數量 (默認: 20)
- `category`: 分類 ID
- `search`: 搜索關鍵字
- `ordering`: 排序字段 (price, -price, created_at, -created_at)

**響應示例**:

```json
{
    "success": true,
    "data": {
        "count": 100,
        "next": "http://localhost:8000/api/v1/products/?page=2",
        "previous": null,
        "results": [
            {
                "id": 1,
                "name": "商品名稱",
                "description": "商品描述",
                "price": "99.99",
                "stock_quantity": 10,
                "category": {
                    "id": 1,
                    "name": "分類名稱"
                },
                "images": [
                    {
                        "id": 1,
                        "image": "/media/products/image1.jpg",
                        "is_primary": true
                    }
                ]
            }
        ]
    },
    "message": "獲取成功"
}
```

### 2. 獲取商品詳情

```sh
GET /api/v1/products/{id}/
```

### 3. 創建商品 (管理員)

```sh
POST /api/v1/products/
```

### 4. 更新商品 (管理員)

```sh
PUT /api/v1/products/{id}/
```

### 5. 刪除商品 (管理員)

```sh
DELETE /api/v1/products/{id}/
```

## 購物車 API (待實現)

### 1. 獲取購物車

```sh
GET /api/v1/cart/
```

### 2. 添加商品到購物車

```sh
POST /api/v1/cart/items/
```

### 3. 更新購物車商品數量

```sh
PUT /api/v1/cart/items/{id}/
```

### 4. 刪除購物車商品

```sh
DELETE /api/v1/cart/items/{id}/
```

### 5. 清空購物車

```sh
DELETE /api/v1/cart/
```

## 訂單管理 API (待實現)

### 1. 創建訂單

```sh
POST /api/v1/orders/
```

### 2. 獲取訂單列表

```sh
GET /api/v1/orders/
```

### 3. 獲取訂單詳情

```sh
GET /api/v1/orders/{id}/
```

### 4. 更新訂單狀態 (管理員)

```sh
PUT /api/v1/orders/{id}/status/
```

## 支付 API (待實現)

### 1. 創建支付

```sh
POST /api/v1/payments/
```

### 2. 查詢支付狀態

```sh
GET /api/v1/payments/{id}/
```

### 3. 支付回調處理

```sh
POST /api/v1/payments/webhook/
```

## API 測試示例

### 使用 curl 測試

#### 1. 註冊用戶

```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'
```

#### 2. 登入用戶

```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

#### 3. 獲取用戶資料

```bash
curl -X GET http://localhost:8000/api/v1/users/profile/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### 使用 Python requests 測試

```python
import requests

# 基礎 URL
BASE_URL = "http://localhost:8000/api/v1"

# 註冊
response = requests.post(f"{BASE_URL}/auth/register/", json={
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123"
})
print(response.json())

# 登入
response = requests.post(f"{BASE_URL}/auth/login/", json={
    "username": "testuser",
    "password": "testpass123"
})
token = response.json()['data']['token']

# 獲取用戶資料
headers = {"Authorization": f"Token {token}"}
response = requests.get(f"{BASE_URL}/users/profile/", headers=headers)
print(response.json())
```

## 錯誤代碼對照表

| 錯誤代碼 | 描述 | HTTP 狀態碼 |
|---------|-----|------------|
| USER_NOT_FOUND | 用戶不存在 | 404 |
| INVALID_CREDENTIALS | 認證失敗 | 401 |
| EMAIL_EXISTS | 郵箱已存在 | 400 |
| USERNAME_EXISTS | 用戶名已存在 | 400 |
| INVALID_TOKEN | 無效的 Token | 401 |
| PERMISSION_DENIED | 權限不足 | 403 |
| PRODUCT_NOT_FOUND | 商品不存在 | 404 |
| INSUFFICIENT_STOCK | 庫存不足 | 400 |
| ORDER_NOT_FOUND | 訂單不存在 | 404 |
| PAYMENT_FAILED | 支付失敗 | 400 |

## 更新記錄

- 2024-12-28: 創建 API 文檔初版，包含認證和用戶管理 API
