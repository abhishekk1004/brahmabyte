from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Room, Message, User
from schemas import RoomCreate, RoomOut, MessageCreate, MessageOut

router = APIRouter(prefix="/chat")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/room", response_model=RoomOut)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    existing = db.query(Room).filter(Room.name == room.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Room already exists")
    new_room = Room(name=room.name, description=room.description)
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

@router.post("/message", response_model=MessageOut)
def post_message(msg: MessageCreate, db: Session = Depends(get_db)):
    room = db.query(Room).get(msg.room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    new_msg = Message(content=msg.content, room_id=msg.room_id, user_id=1)  # Mocked user
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    return new_msg

@router.get("/room/{room_id}/messages", response_model=list[MessageOut])
def get_messages(room_id: int, db: Session = Depends(get_db)):
    return db.query(Message).filter(Message.room_id == room_id).order_by(Message.timestamp).all()
