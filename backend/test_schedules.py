import pytest
from fastapi.testclient import TestClient
from datetime import time


class TestWorkScheduleAPI:
    """工作时间 API 测试"""
    
    def test_create_work_schedule(self, client):
        """测试创建工作时间"""
        response = client.post(
            "/api/schedules/",
            json={
                "name": "标准工作时间",
                "check_in_time": "09:00:00",
                "check_out_time": "18:00:00"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "标准工作时间"
        assert data["check_in_time"] == "09:00:00"
        assert data["check_out_time"] == "18:00:00"
        assert data["is_active"] is True
    
    def test_get_work_schedules(self, client):
        """测试获取工作时间列表"""
        # 创建几个工作时间
        client.post(
            "/api/schedules/",
            json={
                "name": "早班",
                "check_in_time": "08:00:00",
                "check_out_time": "17:00:00"
            }
        )
        client.post(
            "/api/schedules/",
            json={
                "name": "晚班",
                "check_in_time": "14:00:00",
                "check_out_time": "22:00:00"
            }
        )
        
        response = client.get("/api/schedules/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
    
    def test_get_work_schedule(self, client):
        """测试获取单个工作时间"""
        # 创建工作时间
        create_response = client.post(
            "/api/schedules/",
            json={
                "name": "标准工作时间",
                "check_in_time": "09:00:00",
                "check_out_time": "18:00:00"
            }
        )
        schedule_id = create_response.json()["id"]
        
        # 获取工作时间
        response = client.get(f"/api/schedules/{schedule_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "标准工作时间"
    
    def test_get_work_schedule_not_found(self, client):
        """测试获取不存在的工作时间"""
        response = client.get("/api/schedules/9999")
        assert response.status_code == 404
    
    def test_update_work_schedule(self, client):
        """测试更新工作时间"""
        # 创建工作时间
        create_response = client.post(
            "/api/schedules/",
            json={
                "name": "标准工作时间",
                "check_in_time": "09:00:00",
                "check_out_time": "18:00:00"
            }
        )
        schedule_id = create_response.json()["id"]
        
        # 更新工作时间
        response = client.put(
            f"/api/schedules/{schedule_id}",
            json={
                "name": "调整后的工作时间",
                "check_in_time": "08:30:00",
                "check_out_time": "17:30:00"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "调整后的工作时间"
        assert data["check_in_time"] == "08:30:00"
        assert data["check_out_time"] == "17:30:00"
    
    def test_activate_work_schedule(self, client):
        """测试激活工作时间"""
        # 创建两个工作时间
        create_response1 = client.post(
            "/api/schedules/",
            json={
                "name": "工作时间1",
                "check_in_time": "09:00:00",
                "check_out_time": "18:00:00"
            }
        )
        schedule_id1 = create_response1.json()["id"]
        
        create_response2 = client.post(
            "/api/schedules/",
            json={
                "name": "工作时间2",
                "check_in_time": "08:00:00",
                "check_out_time": "17:00:00"
            }
        )
        schedule_id2 = create_response2.json()["id"]
        
        # 激活第二个工作时间
        response = client.post(f"/api/schedules/{schedule_id2}/activate")
        assert response.status_code == 200
        
        # 验证只有第二个是激活的
        schedules = client.get("/api/schedules/?active_only=false").json()
        active_schedules = [s for s in schedules if s["is_active"]]
        assert len(active_schedules) == 1
        assert active_schedules[0]["id"] == schedule_id2
    
    def test_get_active_work_schedule(self, client):
        """测试获取当前激活的工作时间"""
        # 创建并激活一个工作时间
        create_response = client.post(
            "/api/schedules/",
            json={
                "name": "当前工作时间",
                "check_in_time": "09:00:00",
                "check_out_time": "18:00:00"
            }
        )
        schedule_id = create_response.json()["id"]
        client.post(f"/api/schedules/{schedule_id}/activate")
        
        # 获取激活的工作时间
        response = client.get("/api/schedules/active")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "当前工作时间"
    
    def test_get_active_work_schedule_not_found(self, client):
        """测试获取激活的工作时间（无激活时间）"""
        response = client.get("/api/schedules/active")
        assert response.status_code == 404
    
    def test_deactivate_schedule(self, client):
        """测试停用工作时间"""
        # 创建工作时间
        create_response = client.post(
            "/api/schedules/",
            json={
                "name": "测试工作时间",
                "check_in_time": "09:00:00",
                "check_out_time": "18:00:00"
            }
        )
        schedule_id = create_response.json()["id"]
        
        # 停用
        response = client.put(
            f"/api/schedules/{schedule_id}",
            json={"is_active": False}
        )
        assert response.status_code == 200
        assert response.json()["is_active"] is False
