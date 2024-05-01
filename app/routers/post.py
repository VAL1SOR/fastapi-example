from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

router = APIRouter(prefix = "/posts", tags = ['Posts'])

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
async def create(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    post.owner_id = current_user.id
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/", response_model = List[schemas.PostOut])
async def get(db: Session = Depends(get_db), limit: int = 100, skip: int = 0, search: Optional[str] = ""):
  results = db.query(models.Post, func.count(models.Vote.user_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
  return results # db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

@router.get("/{id}", response_model = schemas.PostOut)
async def get(id: int, db: Session = Depends(get_db)):
  post = db.query(models.Post, func.count(models.Vote.user_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
  if not post:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {str(id)} not found")
  return post

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
  post = db.query(models.Post).filter(models.Post.id == id)
  if post.first() == None:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "post not found")
  if current_user.id != post.first().owner_id:
    raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Access denied")
  post.delete(synchronize_session = False)
  db.commit()
  return Response(status_code = status.HTTP_204_NO_CONTENT)
  
@router.put("/{id}", response_model = schemas.Post)
async def update(update: schemas.UpdatePost, id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
  post_query = db.query(models.UpdatePost).filter(models.Post.id == id)
  post = post_query.first()
  if post is None:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "post not found")
  if post.owner_id != current_user.id:
    raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "the auth can't be empty or diferent from the original post")
  if (update.title == None) or (update.content == None):
    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "the title and the content can't be empty")
  post_query.update({'title': update.title, 'content': update.content}, synchronize_session = False)
  db.commit()
  return post_query.first()