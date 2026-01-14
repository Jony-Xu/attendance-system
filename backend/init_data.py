"""
初始化脚本 - 创建测试数据
"""
import asyncio
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
import models
import crud
import schemas
from datetime import time


def create_test_data():
    """创建测试数据"""
    print("初始化数据库...")
    init_db()
    
    db = SessionLocal()
    
    try:
        print("\n创建员工...")
        # 创建主管
        supervisor = schemas.EmployeeCreate(
            employee_id="SUP001",
            name="王经理",
            email="wang@example.com",
            role=models.RoleEnum.SUPERVISOR
        )
        db_supervisor = crud.create_employee(db, supervisor)
        print(f"✓ 创建主管: {db_supervisor.name}")
        
        # 创建员工
        employees_data = [
            ("EMP001", "张三", "zhangsan@example.com"),
            ("EMP002", "李四", "lisi@example.com"),
            ("EMP003", "王五", "wangwu@example.com"),
        ]
        
        for emp_id, name, email in employees_data:
            employee = schemas.EmployeeCreate(
                employee_id=emp_id,
                name=name,
                email=email,
                role=models.RoleEnum.EMPLOYEE
            )
            db_emp = crud.create_employee(db, employee)
            print(f"✓ 创建员工: {db_emp.name}")
        
        print("\n创建工作时间...")
        # 创建工作时间
        schedules_data = [
            ("标准工作时间", "09:00:00", "18:00:00", True),
            ("早班", "08:00:00", "16:00:00", False),
            ("晚班", "14:00:00", "22:00:00", False),
        ]
        
        for name, check_in, check_out, is_active in schedules_data:
            schedule = schemas.WorkScheduleCreate(
                name=name,
                check_in_time=time.fromisoformat(check_in),
                check_out_time=time.fromisoformat(check_out)
            )
            db_schedule = crud.create_work_schedule(db, schedule)
            if not is_active:
                db_schedule.is_active = False
                db.commit()
            print(f"✓ 创建工作时间: {db_schedule.name}")
        
        print("\n✅ 测试数据创建完成！")
        print("\n登录信息:")
        print("主管: 王经理 (SUP001)")
        print("员工: 张三 (EMP001), 李四 (EMP002), 王五 (EMP003)")
        print("\n工作时间: 标准工作时间 (09:00-18:00) [已激活]")
        
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_test_data()
