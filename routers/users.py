import logging
from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.security import OAuth2PasswordBearer
from models.user import User, UserLoginRequest, UserLoginResponse, UserRequest, UserResponse
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from utils import create_access_token, hash_password, verify_password 
from typing import List
from utils import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    logging.info(f"Token received: {token}")
    try:
        logging.info("Decoding access token")
        payload = decode_access_token(token)
        logging.info(f"Payload decoded: {payload}")
        username: str = payload.get("sub")

        logging.info(f"Decoded username: {username}")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def create_user(user_req: UserRequest, db: Session = Depends(get_db)):
    print("Endpoint called")
    # Check if username exists
    existing_user = db.query(User).filter(User.username == user_req.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    print(f"Great! {user_req.username} is not taken")
    # Create and save user
    new_user = User(
        username=user_req.username,
        fullname=user_req.fullname,
        email=user_req.email,
        hashed_password=hash_password(user_req.password)
    )
    print(new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    response = UserResponse(username=new_user.username, email=new_user.email)
    return response

@router.post("/login", response_model=UserLoginResponse)
def login(user_req: UserLoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_req.username).first()
    
    if not user or not verify_password(user_req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": user.username})
    return UserLoginResponse(
        message="Login successful",
        username=user.username,
        access_token=access_token,
        access_token_type="bearer"
        )

## Protected route to get all users
@router.get("/all", response_model=List[UserResponse])
def get_all_users(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [UserResponse(username=user.username, email=user.email) for user in users]