from sqlalchemy import Column, Integer, String, DateTime, Time, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base


class RoleEnum(str, enum.Enum):
    """用户角色枚举"""
    EMPLOYEE = "employee"
    SUPERVISOR = "supervisor"


class AttendanceTypeEnum(str, enum.Enum):
    """考勤类型枚举"""
    CHECK_IN = "check_in"
    CHECK_OUT = "check_out"


class Employee(Base):
    """员工表"""
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    role = Column(SQLEnum(RoleEnum), default=RoleEnum.EMPLOYEE, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    attendance_records = relationship("AttendanceRecord", back_populates="employee")


class AttendanceRecord(Base):
    """考勤记录表"""
    __tablename__ = "attendance_records"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    attendance_type = Column(SQLEnum(AttendanceTypeEnum), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    latitude = Column(String(50), nullable=True)  # 可选的地理位置
    longitude = Column(String(50), nullable=True)
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    employee = relationship("Employee", back_populates="attendance_records")


class WorkSchedule(Base):
    """工作时间表"""
    __tablename__ = "work_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # 例如: "标准工作时间"
    check_in_time = Column(Time, nullable=False)  # 上班时间
    check_out_time = Column(Time, nullable=False)  # 下班时间
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
