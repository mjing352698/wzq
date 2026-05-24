from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
# 定义五子棋游戏逻辑
class WZQ :
    def __init__(self):
        self.board = [[0 for _ in range(15)] for _ in range(15)]
        self.current_player = 'black'
        self.winner = None
    def make_move(self, row, col):
        if self.board[row][col] == 0 and not self.winner:
            self.board[row][col] = 1 if self.current_player == 'black' else 2
        if self.check_win(row, col):
            self.winner = self.current_player
        else:
            self.current_player = 'white' if self.current_player == 'black' else 'black'
    def check_win(self,row,col):
        target = self.board[row][col]
        if target == 0:
            return False
        directions = [(1,0),(0,1),(1,1),(1,-1)]
        for dr,dc in directions:
            count = 1
            r,c = row+dr,col+dc
            while 0<=r<15 and 0<=c<15 and self.board[r][c] == target:
                count += 1
                r += dr
                c += dc
            r,c = row-dr,col-dc
            while 0<=r<15 and 0<=c<15 and self.board[r][c] == target:
                count += 1
                r -= dr
                c -= dc
            if count >= 5:
                return True
        return False
    def reset(self):
        self.board = [[0 for _ in range(15)] for _ in range(15)]
        self.current_player = 'black'
        self.winner = None
game = WZQ()
class LoginData(BaseModel):
    username: str
    password: str
# 数据库配置
DATABASE_URL = "sqlite:///./user.db"
Base = declarative_base()
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(100),nullable=False)
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
# 创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# 密码加密配置
pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')
def hash_password(password: str):
    return pwd_context.hash(password)
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
# 初始化数据库，创建默认用户
def init_db():
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            default_user = User(username="admin", hashed_password=hash_password("123456"))
            db.add(default_user)
            db.commit()
        else:
            print("默认用户已存在")
    finally:
        db.close()