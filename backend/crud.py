from sqlalchemy.orm import Session
from sqlalchemy import and_, extract
from datetime import datetime, date
from typing import List, Optional
import models
import schemas


# Employee CRUD
def get_employee(db: Session, employee_id: int) -> Optional[models.Employee]:
    """根据ID获取员工"""
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()


def get_employee_by_employee_id(db: Session, employee_id: str) -> Optional[models.Employee]:
    """根据员工编号获取员工"""
    return db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()


def get_employee_by_email(db: Session, email: str) -> Optional[models.Employee]:
    """根据邮箱获取员工"""
    return db.query(models.Employee).filter(models.Employee.email == email).first()


def get_employees(db: Session, skip: int = 0, limit: int = 100) -> List[models.Employee]:
    """获取员工列表"""
    return db.query(models.Employee).offset(skip).limit(limit).all()


def create_employee(db: Session, employee: schemas.EmployeeCreate) -> models.Employee:
    """创建员工"""
    db_employee = models.Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def update_employee(db: Session, employee_id: int, employee: schemas.EmployeeUpdate) -> Optional[models.Employee]:
    """更新员工信息"""
    db_employee = get_employee(db, employee_id)
    if db_employee is None:
        return None
    
    update_data = employee.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_employee, field, value)
    
    db_employee.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_employee)
    return db_employee


# Attendance Record CRUD
def create_attendance_record(db: Session, record: schemas.AttendanceRecordCreate) -> models.AttendanceRecord:
    """创建考勤记录"""
    db_record = models.AttendanceRecord(**record.model_dump(), timestamp=datetime.utcnow())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def get_attendance_records(
    db: Session,
    employee_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[models.AttendanceRecord]:
    """获取考勤记录"""
    query = db.query(models.AttendanceRecord)
    if employee_id:
        query = query.filter(models.AttendanceRecord.employee_id == employee_id)
    return query.order_by(models.AttendanceRecord.timestamp.desc()).offset(skip).limit(limit).all()


def get_monthly_attendance_records(
    db: Session,
    year: int,
    month: int,
    employee_id: Optional[int] = None
) -> List[models.AttendanceRecord]:
    """获取月度考勤记录"""
    query = db.query(models.AttendanceRecord).filter(
        and_(
            extract('year', models.AttendanceRecord.timestamp) == year,
            extract('month', models.AttendanceRecord.timestamp) == month
        )
    )
    if employee_id:
        query = query.filter(models.AttendanceRecord.employee_id == employee_id)
    return query.order_by(models.AttendanceRecord.timestamp.desc()).all()


def get_today_last_record(db: Session, employee_id: int) -> Optional[models.AttendanceRecord]:
    """获取今天最后一条考勤记录"""
    today = date.today()
    return db.query(models.AttendanceRecord).filter(
        and_(
            models.AttendanceRecord.employee_id == employee_id,
            extract('year', models.AttendanceRecord.timestamp) == today.year,
            extract('month', models.AttendanceRecord.timestamp) == today.month,
            extract('day', models.AttendanceRecord.timestamp) == today.day
        )
    ).order_by(models.AttendanceRecord.timestamp.desc()).first()


# Work Schedule CRUD
def create_work_schedule(db: Session, schedule: schemas.WorkScheduleCreate) -> models.WorkSchedule:
    """创建工作时间"""
    db_schedule = models.WorkSchedule(**schedule.model_dump())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


def get_work_schedule(db: Session, schedule_id: int) -> Optional[models.WorkSchedule]:
    """根据ID获取工作时间"""
    return db.query(models.WorkSchedule).filter(models.WorkSchedule.id == schedule_id).first()


def get_work_schedules(db: Session, active_only: bool = True) -> List[models.WorkSchedule]:
    """获取工作时间列表"""
    query = db.query(models.WorkSchedule)
    if active_only:
        query = query.filter(models.WorkSchedule.is_active == True)
    return query.order_by(models.WorkSchedule.created_at.desc()).all()


def get_active_work_schedule(db: Session) -> Optional[models.WorkSchedule]:
    """获取当前激活的工作时间"""
    return db.query(models.WorkSchedule).filter(
        models.WorkSchedule.is_active == True
    ).first()


def update_work_schedule(
    db: Session,
    schedule_id: int,
    schedule: schemas.WorkScheduleUpdate
) -> Optional[models.WorkSchedule]:
    """更新工作时间"""
    db_schedule = get_work_schedule(db, schedule_id)
    if db_schedule is None:
        return None
    
    update_data = schedule.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_schedule, field, value)
    
    db_schedule.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


def deactivate_all_schedules(db: Session):
    """停用所有工作时间"""
    db.query(models.WorkSchedule).update({"is_active": False})
    db.commit()
