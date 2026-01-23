from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import crud
import schemas
from database import get_db

router = APIRouter(prefix="/api/schedules", tags=["work schedules"])


@router.post("/", response_model=schemas.WorkSchedule, status_code=status.HTTP_201_CREATED)
def create_work_schedule(schedule: schemas.WorkScheduleCreate, db: Session = Depends(get_db)):
    """创建工作时间安排"""
    return crud.create_work_schedule(db=db, schedule=schedule)


@router.get("/", response_model=List[schemas.WorkSchedule])
def read_work_schedules(active_only: bool = True, db: Session = Depends(get_db)):
    """获取工作时间列表"""
    schedules = crud.get_work_schedules(db, active_only=active_only)
    return schedules


@router.get("/active", response_model=schemas.WorkSchedule)
def read_active_schedule(db: Session = Depends(get_db)):
    """获取当前激活的工作时间"""
    schedule = crud.get_active_work_schedule(db)
    if schedule is None:
        raise HTTPException(status_code=404, detail="No active work schedule found")
    return schedule


@router.get("/{schedule_id}", response_model=schemas.WorkSchedule)
def read_work_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """获取单个工作时间安排"""
    db_schedule = crud.get_work_schedule(db, schedule_id=schedule_id)
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Work schedule not found")
    return db_schedule


@router.put("/{schedule_id}", response_model=schemas.WorkSchedule)
def update_work_schedule(
    schedule_id: int,
    schedule: schemas.WorkScheduleUpdate,
    db: Session = Depends(get_db)
):
    """更新工作时间安排"""
    db_schedule = crud.update_work_schedule(db, schedule_id=schedule_id, schedule=schedule)
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Work schedule not found")
    return db_schedule


@router.post("/{schedule_id}/activate", response_model=schemas.WorkSchedule)
def activate_work_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """激活工作时间安排（停用其他所有安排）"""
    # 先停用所有安排
    crud.deactivate_all_schedules(db)
    
    # 激活指定安排
    schedule_update = schemas.WorkScheduleUpdate(is_active=True)
    db_schedule = crud.update_work_schedule(db, schedule_id=schedule_id, schedule=schedule_update)
    
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Work schedule not found")
    
    return db_schedule


@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_work_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """删除工作时间安排"""
    success = crud.delete_work_schedule(db, schedule_id=schedule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Work schedule not found")
    return None
