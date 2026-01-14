import pytest
from fastapi.testclient import TestClient
from datetime import datetime


class TestAttendanceAPI:
    """考勤 API 测试"""
    
    @pytest.fixture
    def employee_id(self, client):
        """创建测试员工"""
        response = client.post(
            "/api/employees/",
            json={
                "employee_id": "EMP001",
                "name": "张三",
                "email": "zhangsan@example.com",
                "role": "employee"
            }
        )
        return response.json()["id"]
    
    def test_check_in(self, client, employee_id):
        """测试签到"""
        response = client.post(
            "/api/attendance/check-in",
            params={
                "employee_id": employee_id,
                "notes": "正常签到"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["employee_id"] == employee_id
        assert data["attendance_type"] == "check_in"
        assert data["notes"] == "正常签到"
    
    def test_check_in_with_location(self, client, employee_id):
        """测试带地理位置的签到"""
        response = client.post(
            "/api/attendance/check-in",
            params={
                "employee_id": employee_id,
                "latitude": "39.9042",
                "longitude": "116.4074"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["latitude"] == "39.9042"
        assert data["longitude"] == "116.4074"
    
    def test_check_in_not_found_employee(self, client):
        """测试不存在的员工签到"""
        response = client.post(
            "/api/attendance/check-in",
            params={"employee_id": 9999}
        )
        assert response.status_code == 404
        assert "Employee not found" in response.json()["detail"]
    
    def test_double_check_in(self, client, employee_id):
        """测试重复签到"""
        # 第一次签到
        client.post(
            "/api/attendance/check-in",
            params={"employee_id": employee_id}
        )
        
        # 第二次签到（应该失败）
        response = client.post(
            "/api/attendance/check-in",
            params={"employee_id": employee_id}
        )
        assert response.status_code == 400
        assert "Already checked in" in response.json()["detail"]
    
    def test_check_out(self, client, employee_id):
        """测试签退"""
        # 先签到
        client.post(
            "/api/attendance/check-in",
            params={"employee_id": employee_id}
        )
        
        # 签退
        response = client.post(
            "/api/attendance/check-out",
            params={
                "employee_id": employee_id,
                "notes": "正常签退"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["employee_id"] == employee_id
        assert data["attendance_type"] == "check_out"
        assert data["notes"] == "正常签退"
    
    def test_check_out_without_check_in(self, client, employee_id):
        """测试未签到就签退"""
        response = client.post(
            "/api/attendance/check-out",
            params={"employee_id": employee_id}
        )
        assert response.status_code == 400
        assert "Please check in first" in response.json()["detail"]
    
    def test_get_attendance_records(self, client, employee_id):
        """测试获取考勤记录"""
        # 创建几条记录
        client.post("/api/attendance/check-in", params={"employee_id": employee_id})
        client.post("/api/attendance/check-out", params={"employee_id": employee_id})
        
        # 获取记录
        response = client.get("/api/attendance/records")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
    
    def test_get_attendance_records_by_employee(self, client, employee_id):
        """测试获取指定员工的考勤记录"""
        # 创建记录
        client.post("/api/attendance/check-in", params={"employee_id": employee_id})
        
        # 获取指定员工的记录
        response = client.get(f"/api/attendance/records?employee_id={employee_id}")
        assert response.status_code == 200
        data = response.json()
        assert all(record["employee_id"] == employee_id for record in data)
    
    def test_get_monthly_attendance(self, client, employee_id):
        """测试获取月度考勤统计"""
        # 创建记录
        client.post("/api/attendance/check-in", params={"employee_id": employee_id})
        client.post("/api/attendance/check-out", params={"employee_id": employee_id})
        
        # 获取当前月份统计
        now = datetime.now()
        response = client.get(f"/api/attendance/monthly/{now.year}/{now.month}")
        assert response.status_code == 200
        data = response.json()
        assert "total_records" in data
        assert "check_in_count" in data
        assert "check_out_count" in data
        assert data["check_in_count"] >= 1
        assert data["check_out_count"] >= 1
    
    def test_get_attendance_status_not_checked_in(self, client, employee_id):
        """测试获取未签到状态"""
        response = client.get(f"/api/attendance/status/{employee_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "not_checked_in"
    
    def test_get_attendance_status_checked_in(self, client, employee_id):
        """测试获取已签到状态"""
        client.post("/api/attendance/check-in", params={"employee_id": employee_id})
        
        response = client.get(f"/api/attendance/status/{employee_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "checked_in"
        assert data["last_action"] == "check_in"
    
    def test_get_attendance_status_checked_out(self, client, employee_id):
        """测试获取已签退状态"""
        client.post("/api/attendance/check-in", params={"employee_id": employee_id})
        client.post("/api/attendance/check-out", params={"employee_id": employee_id})
        
        response = client.get(f"/api/attendance/status/{employee_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "checked_out"
        assert data["last_action"] == "check_out"
    
    def test_inactive_employee_check_in(self, client, employee_id):
        """测试非激活员工签到"""
        # 停用员工
        client.put(f"/api/employees/{employee_id}", json={"is_active": False})
        
        # 尝试签到
        response = client.post(
            "/api/attendance/check-in",
            params={"employee_id": employee_id}
        )
        assert response.status_code == 400
        assert "not active" in response.json()["detail"]
