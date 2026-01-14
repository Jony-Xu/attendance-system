from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import crud
import schemas
import models
from database import get_db

router = APIRouter(prefix="/api/attendance", tags=["attendance"])


@router.post("/check-in", response_model=schemas.AttendanceRecord, status_code=status.HTTP_201_CREATED)
def check_in(
    employee_id: int,
    latitude: Optional[str] = None,
    longitude: Optional[str] = None,
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """员工签到"""
    # 检查员工是否存在
    employee = crud.get_employee(db, employee_id=employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    if not employee.is_active:
        raise HTTPException(status_code=400, detail="Employee is not active")
    
    # 检查今天是否已经签到
    last_record = crud.get_today_last_record(db, employee_id=employee_id)
    if last_record and last_record.attendance_type == models.AttendanceTypeEnum.CHECK_IN:
        raise HTTPException(
            status_code=400,
            detail="Already checked in today. Please check out first."
        )
    
    # 创建签到记录
    record = schemas.AttendanceRecordCreate(
        employee_id=employee_id,
        attendance_type=models.AttendanceTypeEnum.CHECK_IN,
        latitude=latitude,
        longitude=longitude,
        notes=notes
    )
    return crud.create_attendance_record(db=db, record=record)


@router.post("/check-out", response_model=schemas.AttendanceRecord, status_code=status.HTTP_201_CREATED)
def check_out(
    employee_id: int,
    latitude: Optional[str] = None,
    longitude: Optional[str] = None,
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """员工签退"""
    # 检查员工是否存在
    employee = crud.get_employee(db, employee_id=employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    if not employee.is_active:
        raise HTTPException(status_code=400, detail="Employee is not active")
    
    # 检查今天是否已经签到
    last_record = crud.get_today_last_record(db, employee_id=employee_id)
    if not last_record or last_record.attendance_type == models.AttendanceTypeEnum.CHECK_OUT:
        raise HTTPException(
            status_code=400,
            detail="Please check in first before checking out."
        )
    
    # 创建签退记录
    record = schemas.AttendanceRecordCreate(
        employee_id=employee_id,
        attendance_type=models.AttendanceTypeEnum.CHECK_OUT,
        latitude=latitude,
        longitude=longitude,
        notes=notes
    )
    return crud.create_attendance_record(db=db, record=record)


@router.get("/records", response_model=List[schemas.AttendanceRecord])
def get_attendance_records(
    employee_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取考勤记录"""
    records = crud.get_attendance_records(db, employee_id=employee_id, skip=skip, limit=limit)
    return records


@router.get("/monthly/{year}/{month}", response_model=schemas.AttendanceStatsResponse)
def get_monthly_attendance(
    year: int,
    month: int,
    employee_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """获取月度考勤统计"""
    records = crud.get_monthly_attendance_records(db, year=year, month=month, employee_id=employee_id)
    
    check_in_count = sum(1 for r in records if r.attendance_type == models.AttendanceTypeEnum.CHECK_IN)
    check_out_count = sum(1 for r in records if r.attendance_type == models.AttendanceTypeEnum.CHECK_OUT)
    
    # 加载员工信息
    records_with_employee = []
    for record in records:
        employee = crud.get_employee(db, record.employee_id)
        record_dict = {
            "id": record.id,
            "employee_id": record.employee_id,
            "attendance_type": record.attendance_type,
            "timestamp": record.timestamp,
            "latitude": record.latitude,
            "longitude": record.longitude,
            "notes": record.notes,
            "created_at": record.created_at,
            "employee": employee
        }
        records_with_employee.append(schemas.AttendanceRecordWithEmployee(**record_dict))
    
    return schemas.AttendanceStatsResponse(
        total_records=len(records),
        check_in_count=check_in_count,
        check_out_count=check_out_count,
        records=records_with_employee
    )


@router.get("/status/{employee_id}")
def get_attendance_status(employee_id: int, db: Session = Depends(get_db)):
    """获取员工今日考勤状态"""
    employee = crud.get_employee(db, employee_id=employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    last_record = crud.get_today_last_record(db, employee_id=employee_id)
    
    if not last_record:
        return {
            "employee_id": employee_id,
            "status": "not_checked_in",
            "last_action": None,
            "last_timestamp": None
        }
    
    return {
        "employee_id": employee_id,
        "status": "checked_in" if last_record.attendance_type == models.AttendanceTypeEnum.CHECK_IN else "checked_out",
        "last_action": last_record.attendance_type,
        "last_timestamp": last_record.timestamp
    }
