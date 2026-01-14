from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, time
from typing import Optional, List
from models import RoleEnum, AttendanceTypeEnum


# Employee Schemas
class EmployeeBase(BaseModel):
    employee_id: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    role: RoleEnum = RoleEnum.EMPLOYEE


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None


class Employee(EmployeeBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Attendance Record Schemas
class AttendanceRecordBase(BaseModel):
    attendance_type: AttendanceTypeEnum
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    notes: Optional[str] = Field(None, max_length=500)


class AttendanceRecordCreate(AttendanceRecordBase):
    employee_id: int


class AttendanceRecord(AttendanceRecordBase):
    id: int
    employee_id: int
    timestamp: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class AttendanceRecordWithEmployee(AttendanceRecord):
    employee: Employee


# Work Schedule Schemas
class WorkScheduleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    check_in_time: time
    check_out_time: time


class WorkScheduleCreate(WorkScheduleBase):
    pass


class WorkScheduleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    check_in_time: Optional[time] = None
    check_out_time: Optional[time] = None
    is_active: Optional[bool] = None


class WorkSchedule(WorkScheduleBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Response Schemas
class MessageResponse(BaseModel):
    message: str


class AttendanceStatsResponse(BaseModel):
    total_records: int
    check_in_count: int
    check_out_count: int
    records: List[AttendanceRecordWithEmployee]
