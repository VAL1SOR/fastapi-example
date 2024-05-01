from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2, database
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix = '/vote', tags = ['Vote'])

@router.post("/", status_code = status.HTTP_201_CREATED)
async def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: dict = Depends(oauth2.get_current_user)):
  vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
  found_vote = vote_query.first()
  post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
  if not post:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "post not found")
  if vote.dir == 1:
    if found_vote:
      raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "you have already liked this post")
    new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
    db.add(new_vote)
    db.commit()
    return {"message": "vote added successfully"}
  else:
    if not found_vote:
      raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "vote not found")
    vote_query.delete(synchronize_session = False)
    db.commit()
    return {"message": "vote removed successfully"}