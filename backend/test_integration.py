import pytest
from fastapi.testclient import TestClient
from datetime import datetime


class TestIntegration:
    """集成测试 - 测试完整的业务流程"""
    
    def test_complete_attendance_flow(self, client):
        """测试完整的考勤流程"""
        # 1. 创建主管
        supervisor_response = client.post(
            "/api/employees/",
            json={
                "employee_id": "SUP001",
                "name": "王经理",
                "email": "wang@example.com",
                "role": "supervisor"
            }
        )
        assert supervisor_response.status_code == 201
        
        # 2. 创建员工
        employee_response = client.post(
            "/api/employees/",
            json={
                "employee_id": "EMP001",
                "name": "张三",
                "email": "zhangsan@example.com",
                "role": "employee"
            }
        )
        assert employee_response.status_code == 201
        employee_id = employee_response.json()["id"]
        
        # 3. 主管设置工作时间
        schedule_response = client.post(
            "/api/schedules/",
            json={
                "name": "标准工作时间",
                "check_in_time": "09:00:00",
                "check_out_time": "18:00:00"
            }
        )
        assert schedule_response.status_code == 201
        schedule_id = schedule_response.json()["id"]
        
        # 4. 激活工作时间
        activate_response = client.post(f"/api/schedules/{schedule_id}/activate")
        assert activate_response.status_code == 200
        
        # 5. 获取当前激活的工作时间
        active_schedule = client.get("/api/schedules/active")
        assert active_schedule.status_code == 200
        assert active_schedule.json()["name"] == "标准工作时间"
        
        # 6. 员工签到
        checkin_response = client.post(
            "/api/attendance/check-in",
            params={
                "employee_id": employee_id,
                "latitude": "39.9042",
                "longitude": "116.4074",
                "notes": "准时到达"
            }
        )
        assert checkin_response.status_code == 201
        
        # 7. 查看员工状态
        status_response = client.get(f"/api/attendance/status/{employee_id}")
        assert status_response.status_code == 200
        assert status_response.json()["status"] == "checked_in"
        
        # 8. 员工签退
        checkout_response = client.post(
            "/api/attendance/check-out",
            params={
                "employee_id": employee_id,
                "notes": "正常下班"
            }
        )
        assert checkout_response.status_code == 201
        
        # 9. 主管查看月度考勤记录
        now = datetime.now()
        monthly_response = client.get(f"/api/attendance/monthly/{now.year}/{now.month}")
        assert monthly_response.status_code == 200
        monthly_data = monthly_response.json()
        assert monthly_data["total_records"] == 2
        assert monthly_data["check_in_count"] == 1
        assert monthly_data["check_out_count"] == 1
        
        # 10. 验证记录详情
        records = monthly_data["records"]
        assert len(records) == 2
        assert all(r["employee"]["name"] == "张三" for r in records)
    
    def test_multiple_employees_attendance(self, client):
        """测试多个员工的考勤管理"""
        # 创建多个员工
        employees = []
        for i in range(3):
            response = client.post(
                "/api/employees/",
                json={
                    "employee_id": f"EMP00{i+1}",
                    "name": f"员工{i+1}",
                    "email": f"employee{i+1}@example.com",
                    "role": "employee"
                }
            )
            employees.append(response.json())
        
        # 所有员工签到
        for emp in employees:
            response = client.post(
                "/api/attendance/check-in",
                params={"employee_id": emp["id"]}
            )
            assert response.status_code == 201
        
        # 获取所有考勤记录
        records_response = client.get("/api/attendance/records")
        assert records_response.status_code == 200
        assert len(records_response.json()) == 3
        
        # 获取特定员工的考勤记录
        emp1_records = client.get(f"/api/attendance/records?employee_id={employees[0]['id']}")
        assert emp1_records.status_code == 200
        assert len(emp1_records.json()) == 1
        assert emp1_records.json()[0]["employee_id"] == employees[0]["id"]
    
    def test_schedule_management(self, client):
        """测试工作时间管理"""
        # 创建多个工作时间
        schedules = []
        schedule_configs = [
            {"name": "早班", "check_in": "08:00:00", "check_out": "16:00:00"},
            {"name": "中班", "check_in": "12:00:00", "check_out": "20:00:00"},
            {"name": "晚班", "check_in": "16:00:00", "check_out": "24:00:00"}
        ]
        
        for config in schedule_configs:
            response = client.post(
                "/api/schedules/",
                json={
                    "name": config["name"],
                    "check_in_time": config["check_in"],
                    "check_out_time": config["check_out"]
                }
            )
            assert response.status_code == 201
            schedules.append(response.json())
        
        # 激活中班
        activate_response = client.post(f"/api/schedules/{schedules[1]['id']}/activate")
        assert activate_response.status_code == 200
        
        # 验证只有中班是激活的
        active_response = client.get("/api/schedules/active")
        assert active_response.status_code == 200
        assert active_response.json()["name"] == "中班"
        
        # 获取所有工作时间（包括非激活的）
        all_schedules = client.get("/api/schedules/?active_only=false")
        assert all_schedules.status_code == 200
        assert len(all_schedules.json()) == 3
        
        # 验证只有一个是激活的
        active_count = sum(1 for s in all_schedules.json() if s["is_active"])
        assert active_count == 1
    
    def test_employee_lifecycle(self, client):
        """测试员工生命周期管理"""
        # 1. 创建员工
        create_response = client.post(
            "/api/employees/",
            json={
                "employee_id": "EMP001",
                "name": "张三",
                "email": "zhangsan@example.com",
                "role": "employee"
            }
        )
        assert create_response.status_code == 201
        employee_id = create_response.json()["id"]
        
        # 2. 员工正常考勤
        client.post("/api/attendance/check-in", params={"employee_id": employee_id})
        client.post("/api/attendance/check-out", params={"employee_id": employee_id})
        
        # 3. 更新员工信息
        update_response = client.put(
            f"/api/employees/{employee_id}",
            json={"name": "张三三"}
        )
        assert update_response.status_code == 200
        assert update_response.json()["name"] == "张三三"
        
        # 4. 停用员工
        deactivate_response = client.put(
            f"/api/employees/{employee_id}",
            json={"is_active": False}
        )
        assert deactivate_response.status_code == 200
        
        # 5. 停用后无法考勤
        checkin_response = client.post(
            "/api/attendance/check-in",
            params={"employee_id": employee_id}
        )
        assert checkin_response.status_code == 400
        
        # 6. 但历史记录仍然存在
        records_response = client.get(f"/api/attendance/records?employee_id={employee_id}")
        assert records_response.status_code == 200
        assert len(records_response.json()) == 2
