# Project Development History

---

## Setting Up and Deploying a MySQL Container

### MySQL Container Deployment

**Step 1:** Deploy MySQL/MariaDB using `docker-compose.yml`

```yml
---
networks:
  development_network:

services:
  mariadb:
    image: lscr.io/linuxserver/mariadb:latest
    container_name: mariadb
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/New_York
      - MYSQL_ROOT_PASSWORD=password
      - MYSQL_DATABASE=ecomme_db #database name
      - MYSQL_USER=admin #user name
      - MYSQL_PASSWORD=password #optional

    volumes:
      - /docker/mariadb/config:/config
    ports:
      - 3306:3306
    restart: unless-stopped
    networks:
      - development_network
```

**Step 2:** Verify and access the MariaDB container

- Confirm that MariaDB is running and accessible.

**Method 1: Access from within the container**

```sh
# 1. Enter the container shell
joh@sponge:~$ docker exec -it mariadb bash
root@88031c1c5c3a:/#

# 2. Log in to the database as the admin user
root@88031c1c5c3a:/# mariadb -u admin -p
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
MariaDB [(none)]>

# 3. Check available databases and tables
MariaDB [(none)]> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| ecomme_db          |
+--------------------+

MariaDB [(none)]> USE ecomme_db;
Database changed
MariaDB [ecomme_db]> SHOW TABLES;
+-----------------------------+
| Tables_in_ecomme_db         |
+-----------------------------+
| auth_group                  |
| auth_group_permissions      |
| auth_permission             |
| django_admin_log            |
| django_content_type         |
| django_migrations           |
| django_session              |
| users_user                  |
| users_user_groups           |
| users_user_user_permissions |
+-----------------------------+
10 rows in set (0.000 sec)

MariaDB [ecomme_db]>
```

**Method 2: Remote login via local IP address**

- If you're on the same network, you can connect to the database using its private IP.

```sh
# different devices on the same local network
joh@narwhal:~$ mariadb -h 192.168.17.79 -P 3306 -u admin -p
Enter password:
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
MariaDB [(none)]>

# in the host sponge which is hosting the database
joh@sponge:~$ mariadb -h 127.0.0.1 -P 3306 -u admin -p
Enter password:
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
MariaDB [(none)]>
```

**Method 3: Create and manipulate a test database and table**

```sql
-- 1. Create a Database
MariaDB [(none)]> CREATE DATABASE test_database;
Query OK, 1 row affected (0.003 sec)
-- 2. Use the database
MariaDB [(none)]> USE test_database;
Database changed
-- 3. Create a table in the database
MariaDB [test_database]> CREATE TABLE test_table_25 (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100));
Query OK, 0 rows affected (0.037 sec)
-- 4. Insert a data
MariaDB [test_database]> INSERT INTO test_table_25 (name) VALUES ('test1');
Query OK, 1 row affected (0.014 sec)
-- 5. Select the table to show data
MariaDB [test_database]> SELECT * FROM test_table_25;
+----+-------+
| id | name  |
+----+-------+
|  1 | test1 |
+----+-------+
1 row in set (0.000 sec)
```

- After verifying access and executing these steps, the database setup is ready for further development.

---
---

## Setting Up a Python and Django Project Structure

Following a standard full-stack development workflow, the next steps should be documented accordingly:

### Creating and initializing a Django project

- The project is initialized through the terminal (CLI), rather than via an IDE. Project creation with an IDE may offer a simpler experience.
創建項目是通過Terminal命令行來實現的， 也就是非IDE創建項目， IDE創建項目框架步驟應該會更簡單些。

**Step 1. Create the project directory structure**

```sh
# Create the project in Terminal
mkdir ecommerce && cd ecommerce
```

---

**Step 2. Set up a Python virtual environment**

```sh
python3 -m venv venv
source venv/bin/activate
```

---

**Step 3. Initialize the Django project**

```sh
# 3.1 Install Django and related dependencies
pip install django djangorestframework

# Or install all dependencies via a requirements.txt file
pip install -r requirements.txt

# Check installed packages
pip list
```

> **Note:**
> For how to configure packages like `djangorestframework` in `settings.py`, refer to Step 5.3 below.

```sh
# 3.2 Create a Django project named ecommerce_backend
cd ecommerce
django-admin startproject ecommerce_backend
# The project structure will be:
# ecommerce_backend/          # Project root
# ├── ecommerce_backend/      # Configuration directory (not an app) – acts as the "brain" of the project
# │   ├── settings.py
# │   ├── urls.py
# │   ├── wsgi.py
# │   └── asgi.py
# └── manage.py               # Django management script
```

> **NOTICE:**
> > Running `startproject ecommerce_backend` will generate a two-level folder structure:
> >
> > - The outer `ecommerce_backend/` is the project root.
> > - The inner `ecommerce_backend/` is the **Django configuration directory**, not an app. It serves as the project's "brain."
> >
> > It contains the global configuration files (e.g., `settings.py`), the central URL router (`urls.py`), and the app entry points (`wsgi.py`, `asgi.py`).

> **NOTICE：**
> > 當 `startproject ecommerce_backend`被執行時，Django 會建立兩層資料夾結構。
> >
> > - 第一層 `ecommerce_backend/` 是你的專案根目錄。
> > - 第二層 `ecommerce_backend/` 是 Django 的**項目設定目錄**，不是應用（app），而是整個專案的「大腦」。
> >
> > 它負責定義專案級別的設定檔（如 `settings.py`）、路由總入口（`urls.py`）、以及應用啟動方式（`wsgi.py`, `asgi.py`）。

---

**Step 4. Create a Django app called `users`**

```sh
# 4.1 Enter the project directory
cd ecommerce_backend  # Required to run manage.py commands

# 4.2 Verify project structure
ls -la
# Expected output:
# drwxr-xr-x  ecommerce_backend/
# -rwxr-xr-x  manage.py

# 4.3 Create the first app: users
python manage.py startapp users

# 4.4 Confirm app creation
ls -la
# Expected output:
# drwxr-xr-x  ecommerce_backend/
# drwxr-xr-x  users/
# -rwxr-xr-x  manage.py
```

> **NOTICE:**
> > The `users/` directory is created by running `python manage.py startapp users`.
> > It defines a new Django app responsible for user-related logic such as registration, authentication, and profile management.
> > This app functions as a **self-contained business module**, making it easier to test and scale independently.
> > After creating the app, make sure to register it in the `INSTALLED_APPS` list in `settings.py`.

> **NOTICE：**
> > `users/` 是透過 `python manage.py startapp users` 指令建立的 Django 應用（app），負責處理與「用戶功能」相關的邏輯，
> > 如註冊、登入、個人資料等。它是專案中一個**獨立的業務模組**，日後可獨立擴充與測試。
> > 使用 `python manage.py startapp users` 創建應用後，必須在 INSTALLED_APPS 中註冊

---

**Step 5. Basic Project Configuration 基礎配置設置**

**5.1 Project Directory Verification 項目結構檢查**

After completing the previous steps, confirm that the directory structure is as follows:
執行完前面的命令後，確認目錄結構：

```sh
/home/joh/Workspace/python_projects/ecommerce/
├── docs/                          # Project documentation (manually created)
├── venv/                          # Python virtual environment
├── requirements.txt               # Dependency list
└── ecommerce_backend/             # Django project root
    ├── manage.py                  # Django management tool
    ├── ecommerce_backend/         # Project configuration directory (auto-generated)
    │   ├── __init__.py
    │   ├── settings.py            # Project settings
    │   ├── urls.py               # Main URL router
    │   ├── wsgi.py               # 🚀 WSGI server entry point Web服務器接口
    │   └── asgi.py               # 🚀 ASGI server entry point 異步服務器接口
    └── users/                     # 📁 User app directory (manually created)
        ├── __init__.py
        ├── admin.py              # 👤 Admin interface configuration
        ├── apps.py               # 📱 App configuration
        ├── models.py             # 🗃️ Database models
        ├── views.py              # 👁️ View logic
        ├── tests.py              # 🧪 Unit tests
        └── migrations/           # 📁 Database migration files
```

**5.2 Django Core Concepts (Recap)**

- **Project**: `ecommerce_backend` – the overarching container for your Django application.
項目 (Project): `ecommerce_backend` - 整個Django項目的容器

- **App**: `users` – a modular component responsible for user-related features.
應用 (App): `users` - 項目中的功能模組

- Django follows a modular design; each app handles specific business logic independently.
Django採用模組化設計，每個應用負責特定的業務功能

**5.3 Configuring `settings.py` – Registering Apps**
配置 `settings.py` - 添加應用

After creating an app using `python manage.py startapp app_name`, you must manually register it in `INSTALLED_APPS` inside `settings.py`.
前提 使用`python manage.py startapp apps` 創建應用後需要在INSTALLED_APPS中註冊

**Why register apps in `INSTALLED_APPS`?**
為什麼要在 INSTALLED_APPS 中添加應用？

- **Application discovery**: Django needs to know which apps are part of the project.
**Django 應用發現機制**：Django 需要知道哪些應用是項目的一部分

- **Model recognition**: Only registered apps will have their `models.py` recognized and corresponding database tables created.
**模型註冊**：只有註冊的應用，其 `models.py` 中的模型才會被 Django 識別和創建數據表

- **URL routing**: App-level URL configurations can only be included if the app is registered.
**URL 路由**：應用的 URL 配置才能被包含到項目中

- **Static files and templates**: Django can discover static assets and templates in registered apps.
**靜態文件和模板**：Django 才能找到應用中的靜態文件和模板

- **Admin interface**: Models must be registered to appear in the Django admin dashboard.
**管理後台**：models 才能在 Django admin 中顯示

**5.3 Verifying the `INSTALLED_APPS` Configuration** {#step5-3-installed-apps}
5.3 檢查當前配置狀態

```sh
# Check current INSTALLED_APPS configuration
grep -A 15 "INSTALLED_APPS" ecommerce_backend/ecommerce_backend/settings.py
```

**Current Configuration Example**
當前實際配置:

```python
INSTALLED_APPS = [
    # Django built-in apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps (❗️ must be manually added)
    'rest_framework', # From requirements.txt
    'rest_framework_simplejwt',
    'corsheaders',

    # Local apps
    'users',  # Manually added
]
```

**🔧 Key Takeaways**
重要學習點

1. **`pip install` ≠ auto-configuration**: Installing a package via `pip` does not automatically register it with Django.
**pip 安裝 ≠ 自動配置**: 用 `pip install` 安裝的包不會自動添加到 `INSTALLED_APPS`

2. **Manual registration is required**: All Django-style third-party apps must be added to `INSTALLED_APPS`.
**手動註冊必要**: Django 應用型的第三方包需要手動添加到 `INSTALLED_APPS`

3. **Pure Python utility libraries are excluded**: Packages like `requests` or `numpy` do not need to be registered—they don’t contain Django app components.
**純工具包除外**: 像 `requests`、`numpy` 這類純 Python 工具包不需要添加

---
---

**Step 6. Database Configuration and Connection Verification** {#step6-database}
數據庫配置與連接驗證

**Learning Objectives**
學習目標

- Confirm that the Django project can successfully connect to the database
確認 Django 項目能正常連接數據庫

- Apply database migrations for Django’s built-in applications
執行 Django 內置應用的數據庫遷移

- Verify that the database connection and operations are functioning properly
驗證數據庫操作功能正常

**Prerequisites** 前提條件：

- MariaDB/MySQL container is running
MariaDB/MySQL 容器已運行

- The database `ecomme_db` has been created
數據庫 `ecomme_db` 已創建

- The user `admin` has the necessary privileges
用戶 `admin` 有相應權限

**6.1 Verify Database Configuration**
檢查數據庫配置

```sh
# Navigate to the Django project directory
cd ecommerce_backend

# Check if the database configuration exists in settings.py
grep -A 12 "DATABASES" ecommerce_backend/settings.py
```

**Expected configuration:** 預期配置內容

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecomme_db',
        'USER': 'admin',
        'PASSWORD': 'tyghbn',
        'HOST': '172.21.0.2',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

> If `settings.py` does not already contain a database configuration block, use the structure above to define it.
如果`settings.py`沒有相關數據庫配置信息， 那麼就按照以上的`DATABASES`中的內容來配置

**6.2 Test Database Connection** 測試數據庫連接

```sh
# Run system checks (includes database validation)
python manage.py check

# Expected output:
# System check identified no issues (0 silenced).

# A more specific test:
python manage.py check --database default

# Alternatively, open a raw database shell
python manage.py dbshell
# If the shell opens successfully, the connection is valid.
# Type `exit;` to quit the shell.
```

**If you encounter errors:** 如果遇到錯誤

- Start debugging from the MySQL container: `docker ps`
排錯先從 `MySQL` 容器開始：`docker ps`

- Verify the database exists using MariaDB shell commands
確認數據庫存在：使用之前學過的 MariaDB 命令檢查

- Confirm network connectivity: `ping 172.21.0.2`
檢查網絡連接：`ping 172.21.0.2`

**6.3 Apply Migrations for Django Built-in Apps** 執行 Django 內置應用遷移

**Why is this necessary?**
Even if you haven’t defined custom models yet, Django’s core apps (such as `admin`, `auth`, `sessions`, etc.) require migration in order to create the necessary tables.
**為什麼需要這步？** 即使沒有自定義 `models`，Django 內置應用（`admin`, `auth`, `sessions` 等）也需要創建數據表。

```sh
# View pending migrations for all apps 查看當前遷移狀態（會顯示內置應用的遷移）
python manage.py showmigrations

# Apply all initial migrations 執行 Django 內置應用的數據庫遷移
python manage.py migrate

# Verify tables were created successfully 驗證數據庫表創建成功
# Use MariaDB shell commands to inspect database tables 使用之前學過的 MariaDB 命令檢查表
```

**Completion Criteria for Step 6** Step 6 完成標誌

- `python manage.py check` runs without errors
- `python manage.py dbshell` connects successfully
- Core tables (e.g. `auth_user`, `django_admin_log`) are present
Django 內置表已創建（`auth_user`, `django_admin_log` 等）
- The project is now capable of performing basic database operations
項目具備基本的數據庫操作能力

---
---

**Step 7. 用戶數據模型設計** {#step7-users-model}

**學習目標**：

- 分析電商項目的用戶需求
- 設計用戶數據模型
- 理解 Django 用戶系統擴展

> Django 应用开发流程： models.py (数据模型) → 迁移 → admin.py → views.py → urls.py → templates
> > 为什么从 models.py 开始？
数据是核心：没有数据结构，就没有业务逻辑
Django 的 MVT 模式：Model → View → Template
依赖关系：Views 需要 Models，Admin 需要 Models

> `Django` 应用开发流程是否一致？ 是的，但有细微差异：

|应用类型 |开发流程| 重点差异|
|-|-|-|
|数据驱动型| models.py → 迁移 → admin.py → views.py → urls.py| 以数据模型为核心|
|API 服务型| models.py → 迁移 → serializers.py → views.py → urls.py| 重点在API设计|
|功能工具型| views.py → urls.py → utils.py| 可能不需要数据模型|

> 但核心流程基本一致：数据 → 逻辑 → 接口 → 展示

**前提條件**：

- 數據庫連接已配置並測試成功
- `users` 應用已創建並添加到 `INSTALLED_APPS`

**7.1 確認需求文檔**

✅ **需求分析已完成**：詳見 `docs/requirements.md`

- [x] 用戶角色定義
- 字段需求分析
- 設計決策說明

**當前開發目標**：基於需求分析，實現用戶模型

**7.2 用戶角色模型設計討論** {#step7-2-role-design}

**🎯 設計原則**：在編寫 models.py 之前，詳細分析和討論用戶角色體系

**用戶角色分類體系**：

**主類別 → 子角色設計**：

| 主類別 | 子角色 | 代碼 | 主要功能 | 特殊需求 |
|--------|--------|------|----------|----------|
| **C端（消費者）** | 普通用戶 | `customer` | 購買商品、管理訂單 | 生日字段 |
| **C端（消費者）** | VIP用戶 | `vip` | 享受折扣、專屬服務 | VIP等級、積分 |
| **C端（消費者）** | 批發用戶 | `wholesale` | 大量採購、批發價格 | 信用額度、公司信息 |
| **B端（商業）** | 商家 | `vendor` | 銷售商品、店鋪管理 | 營業執照、稅號 |
| **B端（商業）** | 供貨商 | `supplier` | 供貨、庫存管理 | 供貨協議、質控 |
| **平台（內部）** | 管理員 | `admin` | 平台管理、系統配置 | 員工編號、部門 |
| **平台（內部）** | 員工 | `staff` | 客服、運營支持 | 員工編號、部門 |

**字段需求分析**：

**1. 統一字段（所有角色都需要）**：

```python
# Django 內置字段
username, email, password, first_name, last_name, is_active, date_joined, last_login

# 自定義必需字段
phone          # 手機號（所有用戶必需）
user_type      # 用戶角色類型
```

**2. 條件字段（特定角色需要）**：

```python
# 個人信息（C端用戶）
birth_date = models.DateField(null=True, blank=True)    # 生日
gender = models.CharField(max_length=1, null=True, blank=True)  # 性別

# VIP信息（VIP用戶）
vip_level = models.IntegerField(null=True, blank=True)   # VIP等級
vip_points = models.IntegerField(default=0)             # VIP積分

# 商業信息（B端用戶）
company_name = models.CharField(max_length=200, null=True, blank=True)      # 公司名稱
business_license = models.CharField(max_length=100, null=True, blank=True)  # 營業執照
tax_number = models.CharField(max_length=50, null=True, blank=True)         # 稅號

# 信用信息（批發用戶）
credit_limit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # 信用額度

# 員工信息（平台用戶）
employee_id = models.CharField(max_length=20, null=True, blank=True)  # 員工編號
department = models.CharField(max_length=50, null=True, blank=True)   # 部門

# 驗證狀態
is_verified = models.BooleanField(default=False)  # 是否通過驗證
```

**3. 角色選擇設計**：
```python
USER_TYPE_CHOICES = [
    # C端用戶
    ('customer', '普通客戶'),
    ('vip', 'VIP客戶'), 
    ('wholesale', '批發客戶'),
    
    # B端用戶
    ('vendor', '商家'),
    ('supplier', '供應商'),
    
    # 平台用戶
    ('admin', '管理員'),
    ('staff', '員工'),
]
```

**設計決策**：
- ✅ 採用 **單一模型 + 角色區分** 方案
- ✅ 大部分字段設為可選（`null=True, blank=True`）
- ✅ 通過角色類型控制字段的使用
- ✅ 為未來擴展預留靈活性

**討論問題**：
1. 您是否同意這個角色分類？
2. 是否需要調整某些字段設計？
3. 是否需要保留現有的 `guest` 角色？

**7.2.1 當前 models.py 狀態分析** {#step7-2-1-current-analysis}

**✅ 檢查了當前的 `users/models.py`**，發現你已經編寫了一個基礎版本：

**當前實現的優點**：

- ✅ 正確使用 `AbstractUser`
- ✅ 添加了性別字段（`gender`）
- ✅ 添加了生日字段（`dob`）  
- ✅ 有基本的角色系統（`role`）
- ✅ 正確處理了 `groups` 和 `user_permissions` 的衝突

**需要改進的地方**：

- ❌ 角色選擇不夠全面（只有 admin, customer, staff, guest）
- ❌ 缺少電商關鍵字段（手機號、公司信息、VIP等級等）
- ❌ 字段命名可以更規範（`dob` → `birth_date`）

**7.2.2 電商角色設計討論** {#step7-2-2-ecommerce-roles}

**當前角色 vs 電商需求對比**：

| 當前角色 | 電商擴展建議 | 說明 |
|----------|--------------|------|
| `customer` | ✅ 保留 | 普通客戶 |
| `admin` | ✅ 保留 | 管理員 |
| `staff` | ✅ 保留 | 員工 |
| `guest` | ❓ 討論 | 訪客（可能不需要存儲） |
| **新增** | `vip` | VIP客戶 |
| **新增** | `wholesale` | 批發客戶 |
| **新增** | `vendor` | 商家/賣家 |
| **新增** | `supplier` | 供應商 |

**建議的完整角色設計**：
```python
USER_TYPE_CHOICES = [
    # C端用戶
    ('customer', '普通客戶'),
    ('vip', 'VIP客戶'), 
    ('wholesale', '批發客戶'),
    
    # B端用戶
    ('vendor', '商家'),
    ('supplier', '供應商'),
    
    # 平台用戶
    ('admin', '管理員'),
    ('staff', '員工'),
    
    # 特殊（可選）
    ('guest', '訪客'),  # 討論是否需要
]
```

**7.2.3 電商字段需求討論** {#step7-2-3-field-requirements}

**當前缺少的重要字段**：

```python
# 1. 基礎聯絡信息（所有用戶必需）
phone = models.CharField(max_length=20, blank=True)  # 手機號

# 2. 商業信息（B端用戶需要）
company_name = models.CharField(max_length=200, null=True, blank=True)
business_license = models.CharField(max_length=100, null=True, blank=True)
tax_number = models.CharField(max_length=50, null=True, blank=True)

# 3. VIP 信息（VIP用戶需要）  
vip_level = models.IntegerField(null=True, blank=True)
vip_points = models.IntegerField(default=0)

# 4. 信用信息（批發用戶需要）
credit_limit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

# 5. 員工信息（平台用戶需要）
employee_id = models.CharField(max_length=20, null=True, blank=True)
department = models.CharField(max_length=50, null=True, blank=True)

# 6. 驗證狀態
is_verified = models.BooleanField(default=False)
```

**討論要點**：

1. **是否保留 `guest` 角色？**
   - 訪客通常不需要註冊，用 session 即可
   - 如果保留，是為了什麼業務場景？

2. **字段命名規範**：
   - `dob` → `birth_date`（更清晰）
   - `role` → `user_type`（更準確）

3. **必需字段 vs 可選字段**：
   - `phone` 是否對所有用戶必需？
   - `email` 是否可以作為主要聯絡方式？

**請回答以下問題，我們再完善 models.py**：

1. 你認為需要保留 `guest` 角色嗎？如果需要，用於什麼場景？
2. 手機號對於你的電商網站是否必需？（影響 `blank=False` 的設置）
3. 你是否同意添加上述的商業字段和VIP字段？
4. 是否有其他特殊的業務需求需要考慮？

---

**⚠️ 請逐項確認，確認後我們立即開始重寫 models.py！**

**7.5 用戶建模與角色設計最終確認** {#step7-5-user-modeling-final}

**✅ 用戶經過一天思考，提出具體用戶類型需求**

**用戶提出的原始需求**：

- Customer # 顧客（普通+VIP+會員+批發）
- Vendor   # 商家（如自營、合作供應商）
- Store Associate  # 實體門市的店員
- Delivery Driver  # 自營物流或合作配送人員
- Supplier  # 原始供應商（貨源端）
- Support   # 客服人員
- Administrator  # 系統超管
- Staff  # 內部管理或支援人員（含採購、營運）

**最終確定的 8 個主要用戶類型**：

```python
MAIN_USER_TYPES = [
    ('customer', 'Customer'),                    # 顧客（普通+VIP+會員+批發）
    ('vendor', 'Vendor'),                        # 商家（如自營、合作供應商）
    ('store_associate', 'Store Associate'),      # 實體門市的店員
    ('delivery_driver', 'Delivery Driver'),      # 自營物流或合作配送人員
    ('supplier', 'Supplier'),                    # 原始供應商（貨源端）
    ('support', 'Customer Support'),             # 客服人員
    ('admin', 'Administrator'),                  # 系統超管
    ('staff', 'Staff'),                          # 內部管理或支援人員（含採購、營運）
]
```

**✅ 已更新 requirements.md 文檔**：

- 詳細定義了每個用戶類型的功能和子角色
- 建立了完整的字段需求矩陣
- 明確了主次分類設計原理

**下一步確認事項**：

1. **你是否同意這 6 個主要用戶類型？**
2. **你是否理解主次分類的設計邏輯？**（如：customer + sub_role="vip_gold"）
3. **字段設計是否符合你的預期？**（如：VIP積分、商業信息等）
4. **是否有需要補充或修改的地方？**

**⚠️ 請確認以上設計，然後我們開始設計具體的字段並編寫 models.py！**

---

**7.6 用戶業務背景深入分析與角色重新設計** {#step7-6-business-context}

**✅ 用戶業務背景說明**：

**真實業務場景**：

- 🏪 **實體亞洲超市經營者**：有實體店鋪，實際商品庫存
- 🌐 **實體+線上混合經營**：將實體店商品搬到線上銷售
- 👤 **小生意主**：可能親自參與送貨、客服、訂單處理等多個環節
- 📦 **內部配送**：可能自己送貨，不依賴第三方配送

**重要認知**：這不是純粹的電商項目，而是「實體店數位化轉型」項目

---

**7.6.1 重新分析「Guest Shopper」角色** {#step7-6-1-guest-analysis}

**用戶質疑**：「Guest Shopper 為什麼不是用戶類型？」

**✅ 專業分析修正**：

**在實體+線上混合的場景下，Guest Shopper 確實是重要的用戶類型！**

**為什麼之前判斷有誤**：

- ❌ 純線上電商思維：訪客只是瀏覽，不需要記錄
- ✅ 實體+線上混合：訪客可能是實體店老客戶，需要特殊處理

**實體+線上混合場景下的 Guest Shopper 特點**：

1. **既是用戶狀態，也是用戶類型**：

   ```text
   用戶狀態：未登錄狀態下瀏覽商品
   用戶類型：選擇不註冊但有購買意願的客戶群體
   ```

3. **業務需求**：
   - 🛒 **快速購買**：實體店熟客不想註冊，直接下單
   - 📞 **電話聯絡**：提供手機號，方便確認訂單
   - 🚗 **到店取貨**：選擇到實體店自取
   - 💰 **現金支付**：到店付款取貨

4. **技術實現**：

   ```python
   # Guest 用戶需要最基本的信息記錄
   guest_phone = models.CharField(max_length=20, null=True, blank=True)  # 聯絡電話
   guest_name = models.CharField(max_length=100, null=True, blank=True)   # 聯絡姓名
   pickup_preference = models.CharField(max_length=20, null=True, blank=True)  # 取貨偏好
   ```

**結論**：Guest Shopper 在您的業務模式下是必要的用戶類型

---

**7.6.2 重新分析「Store Associate」和「Delivery Driver」** {#step7-6-2-staff-analysis}

**用戶說明**：
- Store Associate = 實體店員工，處理線上+線下訂單
- Delivery Driver = 內部員工，老闆可能親自送貨

**✅ 專業分析修正**：

**Store Associate（店員）的實際職責**：

1. **線上線下訂單處理**：
   ```
   - 線下：實體店收銀、商品諮詢
   - 線上：處理網上訂單、打包商品
   - 混合：協助客戶線上下單、到店取貨
   ```

2. **權限需求**：
   ```python
   store_position = models.CharField(max_length=50, null=True, blank=True)  # 店內職位
   can_process_orders = models.BooleanField(default=False)     # 能否處理訂單
   can_manage_inventory = models.BooleanField(default=False)   # 能否管理庫存
   work_schedule = models.TextField(null=True, blank=True)     # 工作時間
   ```

**Delivery Driver（配送員）的實際需求**：

1. **內部員工特性**：
   ```
   - 老闆自己送貨
   - 員工兼職送貨
   - 需要訂單管理權限
   - 需要客戶聯絡權限
   ```

2. **字段需求**：
   ```python
   vehicle_type = models.CharField(max_length=50, null=True, blank=True)    # 配送工具
   delivery_area = models.TextField(null=True, blank=True)                  # 配送區域
   contact_number = models.CharField(max_length=20, null=True, blank=True)  # 配送聯絡號碼
   ```

---

**7.6.3 針對實體+線上混合經營的最終角色設計** {#step7-6-3-final-role-design}

**基於真實業務場景的完整用戶類型**：

| 用戶類型 | 代碼 | 主要場景 | 特殊需求 | 業務價值 |
|----------|------|----------|----------|----------|
| **Guest Shopper** | `guest` | 不註冊快速購買 | 手機號、取貨方式 | 降低購買門檻 |
| **Customer** | `customer` | 註冊會員購買 | 積分、偏好記錄 | 客戶忠誠度 |
| **VIP Customer** | `vip` | 高價值客戶 | VIP等級、專屬服務 | 提升客單價 |
| **Store Associate** | `store_associate` | 實體店員工 | 職位、權限管理 | 線上線下整合 |
| **Delivery Driver** | `delivery_driver` | 內部配送員 | 配送工具、區域 | 配送效率 |
| **Supplier** | `supplier` | 商品供應商 | 公司信息、供貨協議 | 採購管理 |
| **Support** | `support` | 客服人員 | 服務權限、響應時間 | 客戶滿意度 |
| **Admin** | `admin` | 系統管理員 | 全部權限 | 系統管理 |

**權限層次設計**：
```
Admin > Support > Store Associate > Delivery Driver
Customer = VIP (不同服務等級)
Guest (最基本權限)
Supplier (B端權限)
```

**關鍵字段設計**：

```python
# 通用字段
user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
phone = models.CharField(max_length=20, blank=True)  # 必要聯絡方式

# Guest 專用字段
guest_phone = models.CharField(max_length=20, null=True, blank=True)
guest_name = models.CharField(max_length=100, null=True, blank=True)
pickup_preference = models.CharField(max_length=20, null=True, blank=True)

# Store Associate 專用字段
store_position = models.CharField(max_length=50, null=True, blank=True)
can_process_orders = models.BooleanField(default=False)
can_manage_inventory = models.BooleanField(default=False)

# Delivery Driver 專用字段
vehicle_type = models.CharField(max_length=50, null=True, blank=True)
delivery_area = models.TextField(null=True, blank=True)

# VIP 專用字段
vip_level = models.IntegerField(null=True, blank=True)
vip_points = models.IntegerField(default=0)

# Supplier 專用字段
company_name = models.CharField(max_length=200, null=True, blank=True)
business_license = models.CharField(max_length=100, null=True, blank=True)
```

---

**7.6.4 設計決策總結** {#step7-6-4-design-summary}

**✅ 修正了之前的專業判斷**：

1. **Guest Shopper 是必要用戶類型**：
   - 實體+線上混合場景下，快速購買是重要需求
   - 需要記錄基本聯絡信息和取貨偏好

2. **Store Associate 是核心員工角色**：
   - 處理線上線下訂單的關鍵人員
   - 需要細分權限管理

3. **Delivery Driver 是內部配送資源**：
   - 不是第三方，是內部員工或老闆
   - 需要配送管理相關字段

**最終確認事項**：

1. **您是否同意這個重新分析的結果？**
2. **Guest Shopper 的字段設計是否符合您的業務需求？**
3. **Store Associate 的權限設計是否合理？**
4. **Delivery Driver 的字段是否足夠？**
5. **是否還有其他業務場景需要考慮？**

**⚠️ 請確認以上分析，我們立即開始編寫 models.py！**

---

**7.7 用戶角色最終確認與設計決策** {#step7-7-final-confirmation}

**✅ 基於用戶詳細反饋的最終設計**

**用戶明確的業務需求**：

1. ❌ **Guest Shopper 不作為主用戶角色**：用 Django Sessions 處理未登錄狀態
2. ✅ **Store Associate 確定為主用戶角色**：實體店員工需要處理線上業務
3. ✅ **Delivery Driver 確定為主用戶角色**：Local 配送，可能是老闆本人
4. ✅ **必須有會員積分/批發折扣系統**：這是核心業務需求
5. ✅ **支持到店取貨**：實體+線上混合經營的關鍵功能

**最終確定的 7 個主用戶角色**：

```python
MAIN_USER_TYPES = [
    ('customer', 'Customer'),                    # 客戶（普通+會員+批發）
    ('store_associate', 'Store Associate'),      # 店員  
    ('delivery_driver', 'Delivery Driver'),      # 配送員
    ('supplier', 'Supplier'),                    # 供應商
    ('support', 'Customer Support'),             # 客服
    ('admin', 'Administrator'),                  # 管理員
    ('staff', 'Staff'),                         # 其他員工
]
```

**關鍵設計決策**：

1. **Customer 角色設計**：
   - 普通客戶 + 會員等級（銅銀金）+ 批發客戶
   - 會員積分系統
   - 批發折扣系統

2. **Store Associate 權限**：
   - 處理線上訂單
   - 管理到店取貨
   - 客戶服務
   - 庫存管理（根據子角色）

3. **Delivery Driver 功能**：
   - Local 配送範圍
   - 配送狀態更新
   - 可能是老闆本人

4. **業務流程支持**：
   - 到店取貨流程
   - Local 配送流程
   - 會員積分累積
   - 批發折扣計算

**待用戶最終確認的要點**：

1. 7個主用戶角色是否完整？
2. Customer 的子角色分類（會員+批發）是否合理？
3. Store Associate 的4個子角色是否涵蓋實際工作？
4. 字段設計矩陣是否有遺漏？
5. 取貨和配送業務流程是否正確？

**下一步**：等待用戶確認後，開始設計具體的 models.py 結構

---

**7.8 用戶建模專業流程確認與執行計劃** {#step7-8-modeling-process}

**✅ 用戶對建模流程的深度思考**

**用戶重要觀點**：
- ✅ **主用戶角色已確定**：7個主角色可以確定下來
- ✅ **認識到建模流程的重要性**：不應該直接跳到字段定義
- ✅ **提出遵循專業步驟**：按 requirements.md 中的 6 步驟流程執行
- ✅ **强調用戶故事的重要性**：應該先做「撰寫角色任務與使用者故事」

**專業分析**：用戶的認知是完全正確的！

---

**7.8.1 建模流程深度分析** {#step7-8-1-process-analysis}

**為什麼用戶的建議是專業的？**

1. **避免「資料驅動設計」的陷阱**：
   - ❌ 錯誤做法：直接定義字段 → 建立 models → 發現業務邏輯不通
   - ✅ 正確做法：業務故事 → 功能需求 → 字段需求 → models

2. **符合軟體工程最佳實踐**：
   - 📋 **需求分析**：用戶故事 (User Stories)
   - 🎯 **功能設計**：功能模塊梳理
   - 🗃️ **資料設計**：基於功能的字段設計
   - 💻 **實作**：models.py 實現

3. **降低重構風險**：
   - 提前發現業務邏輯衝突
   - 避免後期大幅度修改資料庫結構
   - 確保每個字段都有明確的業務意義

---

**7.8.2 當前進度確認** {#step7-8-2-current-progress}

**✅ 已完成的步驟**：

| 步驟 | 狀態 | 說明 |
|------|------|------|
| **步驟1** | ✅ 完成 | 7個主用戶角色已確定 |
| **步驟2** | ⏳ 進行中 | 撰寫角色任務與使用者故事 |
| **步驟3** | ⏳ 待開始 | 梳理主要流程與功能模塊 |
| **步驟4** | ⏳ 待開始 | 對每個角色抽出必要欄位 |
| **步驟5** | ⏳ 待開始 | 定義資料模型架構（models） |
| **步驟6** | ⏳ 待開始 | 繪製 ER 圖（可選） |

**下一步執行計劃**：立即開始步驟2 - 撰寫角色任務與使用者故事

---

**7.8.3 步驟2執行方案** {#step7-8-3-user-stories}

**角色任務與使用者故事模板**：

```
作為 [角色類型]，
我希望能夠 [具體功能]，
以便 [業務目標/價值]。

接受標準：
- [ ] 條件1
- [ ] 條件2
- [ ] 條件3
```

**需要為7個主角色分別撰寫**：
1. **Customer** - 購買、會員、批發相關故事
2. **Store Associate** - 店員工作相關故事
3. **Delivery Driver** - 配送相關故事
4. **Supplier** - 供貨相關故事
5. **Support** - 客服相關故事
6. **Admin** - 管理相關故事
7. **Staff** - 其他員工相關故事

**建議執行方式**：
- 每個角色寫 3-5 個核心用戶故事
- 專注於實體+線上混合經營的特殊場景
- 確保涵蓋會員積分、批發折扣、到店取貨等關鍵業務

**問題確認**：
1. **是否立即開始撰寫用戶故事？**
2. **每個角色大概需要幾個核心故事？**
3. **是否要我先示範 Customer 角色的用戶故事？**

**⚠️ 確認後立即開始專業的用戶建模流程步驟2！**
