from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import *
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify


router_task = APIRouter(prefix="/task", tags = ["task"])

@router_task.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks_all = db.scalars(select(Task)).all()
    return tasks_all

@router_task.get("/task_id")
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    id_task = db.scalars(select(Task).where(Task.id == task_id))
    if id_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found"
        )
    else:
        return id_task
@router_task.post("/create")
async def create_task(db: Annotated[Session, Depends(get_db)], create: CreateTask, user_id: int):
    user_create = db.scalar(select(User).where(User.id == user_id))
    if user_create is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )
    else:
        db.execute(insert(Task).values(title=create.title,
                                       content=create.content,
                                       priority=create.priority,
                                       user_id=user_id,
                                       slug=slugify(create.title)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
           }
@router_task.put("/update")
async def update_task(db: Annotated[Session, Depends(get_db)], updateTask: UpdateTask, task_id: int):
    task_update = db.scalar(select(Task).where(Task.id == task_id))
    if task_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found"
        )
    else:
        db.execute(update(Task).where(Task.id == task_id).values(title=updateTask.title,
                                                                 content=updateTask.content,
                                                                 priority=updateTask.priority))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task update is successful!'
    }
@router_task.delete("/delete")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task_delete = db.scalar(select(Task).where(Task.id == task_id))
    if task_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found"
        )
    else:
        db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task delete is successful!'
    }