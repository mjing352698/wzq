from fastapi import APIRouter, WebSocket, WebSocketDisconnect,Depends,status,Query
from model import game, LoginData, User, get_db, hash_password, verify_password
import json
from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
from token_utils import generate_token,check_token
from jose import JWTError,jwt
wzq = APIRouter(prefix='/wzq')
@wzq.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket,token:str = Query(...)):
    print(token)
    if not check_token(token):
        print('token错误')
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            direct = json.loads(data)
            if direct['type'] == 'move':
                game.make_move(direct['row'], direct['col'])
            elif direct['type'] == 'reset':
                game.reset()
            await websocket.send_text(json.dumps({
                'board': game.board,
                'currentplayer': game.current_player,
                'winner': game.winner
            }))
    except WebSocketDisconnect:
        print("WebSocket disconnected")
        game.reset()
    except Exception as e:
        print(f"WebSocket error: {e}")
@wzq.post('/login')
def Login(input: LoginData, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == input.username).first()
    if not existing_user:
        return {"success": False, "message": "用户不存在"}
    if not verify_password(input.password, existing_user.hashed_password):
        return {"success": False, "message": "密码错误"}
    token = generate_token(input.username)
    return {"success": True, "message": "登录成功",'token':token}
@wzq.post('/create')
def Create(input: LoginData, db: Session = Depends(get_db)):
    existing_user =  db.query(User).filter(User.username == input.username).first()
    if existing_user:
        return {"success": False, "message": "用户名已存在"}
    hashed_password = hash_password(input.password)
    new_user = User(username=input.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"success": True, "message": "用户创建成功"}