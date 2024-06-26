from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix = "/users", tags = ['Users'])

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
  if user.password is not None:

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
  else:
    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "the password can't be empty")

@router.get("/me", response_model = schemas.UserOut)
async def get_user(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
  return db.query(models.User).filter(models.User.id == current_user.id).first()

@router.get("/{id}", response_model = schemas.UserOut)
async def get_user(id: int, db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == id).first()
  if not user:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "user not found")
  else:
    return user