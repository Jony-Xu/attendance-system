import pytest
from fastapi.testclient import TestClient
import models


class TestEmployeeAPI:
    """员工 API 测试"""
    
    def test_create_employee(self, client):
        """测试创建员工"""
        response = client.post(
            "/api/employees/",
            json={
                "employee_id": "EMP001",
                "name": "张三",
                "email": "zhangsan@example.com",
                "role": "employee"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["employee_id"] == "EMP001"
        assert data["name"] == "张三"
        assert data["email"] == "zhangsan@example.com"
        assert data["role"] == "employee"
        assert data["is_active"] is True
    
    def test_create_employee_duplicate_employee_id(self, client):
        """测试创建重复员工编号"""
        # 创建第一个员工
        client.post(
            "/api/employees/",
            json={
                "employee_id": "EMP001",
                "name": "张三",
                "email": "zhangsan@example.com",
                "role": "employee"
            }
        )
        
        # 尝试创建相同员工编号
        response = client.post(
            "/api/employees/",
            json={
                "employee_id": "EMP001",
                "name": "李四",
                "email": "lisi@example.com",
                "role": "employee"
            }
        )
        assert response.status_code == 400
        assert "Employee ID already registered" in response.json()["detail"]
    
    def test_create_employee_duplicate_email(self, client):
        """测试创建重复邮箱"""
        # 创建第一个员工
        client.post(
            "/api/employees/",
            json={
                "employee_id": "EMP001",
                "name": "张三",
                "email": "test@example.com",
                "role": "employee"
            }
        )
        
        # 尝试创建相同邮箱
        response = client.post(
            "/api/employees/",
            json={
                "employee_id": "EMP002",
                "name": "李四",
                "email": "test@example.com",
                "role": "employee"
            }
        )
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]
    
    def test_get_employees(self, client):
        """测试获取员工列表"""
        # 创建几个员工
        for i in range(3):
            client.post(
                "/api/employees/",
                json={
                    "employee_id": f"EMP00{i+1}",
                    "name": f"员工{i+1}",
                    "email": f"employee{i+1}@example.com",
                    "role": "employee"
                }
            )
        
        response = client.get("/api/employees/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
    
    def test_get_employee(self, client):
        """测试获取单个员工"""
        # 创建员工
        create_response = client.post(
            "/api/employees/",
            json={
                "employee_id": "EMP001",
                "name": "张三",
                "email": "zhangsan@example.com",
                "role": "employee"
            }
        )
        employee_id = create_response.json()["id"]
        
        # 获取员工
        response = client.get(f"/api/employees/{employee_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["employee_id"] == "EMP001"
    
    def test_get_employee_not_found(self, client):
        """测试获取不存在的员工"""
        response = client.get("/api/employees/9999")
        assert response.status_code == 404
    
    def test_update_employee(self, client):
        """测试更新员工"""
        # 创建员工
        create_response = client.post(
            "/api/employees/",
            json={
                "employee_id": "EMP001",
                "name": "张三",
                "email": "zhangsan@example.com",
                "role": "employee"
            }
        )
        employee_id = create_response.json()["id"]
        
        # 更新员工
        response = client.put(
            f"/api/employees/{employee_id}",
            json={"name": "张三三", "role": "supervisor"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "张三三"
        assert data["role"] == "supervisor"
    
    def test_create_supervisor(self, client):
        """测试创建主管"""
        response = client.post(
            "/api/employees/",
            json={
                "employee_id": "SUP001",
                "name": "王经理",
                "email": "wang@example.com",
                "role": "supervisor"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["role"] == "supervisor"
