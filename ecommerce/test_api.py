#!/usr/bin/env python3
"""
電商 API 測試腳本
用於測試用戶認證相關的 API 端點
"""

import requests
import json

# API 基礎 URL
BASE_URL = 'http://127.0.0.1:8000/api'


def test_api_root():
    """測試 API 根端點"""
    print("🔍 測試 API 根端點...")
    response = requests.get(f"{BASE_URL}/")
    print(f"狀態碼: {response.status_code}")
    print(f"響應: {response.json()}")
    print("-" * 50)


def test_user_registration():
    """測試用戶註冊"""
    print("📝 測試用戶註冊...")

    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpassword123",
        "password_confirm": "testpassword123",
        "gender": "M"
    }

    response = requests.post(
        f"{BASE_URL}/users/auth/register/", json=user_data)
    print(f"狀態碼: {response.status_code}")
    print(f"響應: {response.json()}")

    if response.status_code == 201:
        return response.json()['tokens']['access']
    print("-" * 50)
    return None


def test_user_login():
    """測試用戶登入"""
    print("🔐 測試用戶登入...")

    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }

    response = requests.post(f"{BASE_URL}/users/auth/login/", json=login_data)
    print(f"狀態碼: {response.status_code}")
    print(f"響應: {response.json()}")

    if response.status_code == 200:
        return response.json()['tokens']['access']
    print("-" * 50)
    return None


def test_user_profile(access_token):
    """測試用戶資料查看"""
    if not access_token:
        print("❌ 無法測試用戶資料 - 缺少 access token")
        return

    print("👤 測試用戶資料查看...")

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(f"{BASE_URL}/users/profile/", headers=headers)
    print(f"狀態碼: {response.status_code}")
    print(f"響應: {response.json()}")
    print("-" * 50)


def test_user_dashboard(access_token):
    """測試用戶儀表板"""
    if not access_token:
        print("❌ 無法測試用戶儀表板 - 缺少 access token")
        return

    print("📊 測試用戶儀表板...")

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(f"{BASE_URL}/users/dashboard/", headers=headers)
    print(f"狀態碼: {response.status_code}")
    print(f"響應: {response.json()}")
    print("-" * 50)


def main():
    """主測試函數"""
    print("🚀 開始 E-Commerce API 測試")
    print("=" * 50)

    # 測試 API 根端點
    test_api_root()

    # 測試用戶註冊
    access_token = test_user_registration()

    # 如果註冊失敗，嘗試登入
    if not access_token:
        access_token = test_user_login()

    # 測試需要認證的端點
    test_user_profile(access_token)
    test_user_dashboard(access_token)

    print("✅ API 測試完成!")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到服務器，請確保 Django 開發服務器正在運行")
        print("💡 請運行: python manage.py runserver")
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
