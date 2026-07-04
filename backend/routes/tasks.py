from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from database.models import Task
from backend.services.auth import get_current_user, get_current_user_id
from backend.services.auth import get_db

router = APIRouter(prefix="/api/tasks")

class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., max_length=1000)
    completed: bool = Field(default=False)

class TaskUpdateRequest(BaseModel):
    title: str = Field(None, min_length=1, max_length=255)
    description: str = Field(None, max_length=1000)
    completed: bool = Field(None)

class TaskResponse(BaseModel):
    id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: Optional[datetime] = None

@router.post("/", operation_id="create_task", response_model=TaskResponse)
async def create_task_endpoint(
    task_data: TaskCreateRequest,
    db: Session = Depends(get_db),
    current_user: UUID = Depends(get_current_user_id)
):
    try:
        task = Task(
            user_id=current_user,
            title=task_data.title,
            description=task_data.description,
            completed=task_data.completed,
            created_at=datetime.utcnow()
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/", operation_id="list_tasks", response_model=List[TaskResponse])
async def list_tasks_endpoint(
    db: Session = Depends(get_db),
    current_user: UUID = Depends(get_current_user_id)
):
    try:
        tasks = db.query(Task).filter(Task.user_id == current_user).all()
        return [
            TaskResponse(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                created_at=task.created_at
            )
            for task in tasks
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/{id}", operation_id="update_task", response_model=TaskResponse)
async def update_task_endpoint(
    id: UUID,
    task_data: TaskUpdateRequest,
    db: Session = Depends(get_db),
    current_user: UUID = Depends(get_current_user_id)
):
    try:
        task = db.query(Task).filter(Task.id == id, Task.user_id == current_user).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.completed is not None:
            task.completed = task_data.completed
        db.commit()
        db.refresh(task)
        return TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/{id}", operation_id="delete_task", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: UUID = Depends(get_current_user_id)
):
    try:
        task = db.query(Task).filter(Task.id == id, Task.user_id == current_user).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        db.delete(task)
        db.commit()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )