from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from sqlalchemy import create_engine, Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import random


# ================= تنظیمات امنیتی و JWT =================

SECRET_KEY = "super_secret_key_change_me"   # فقط برای دمو
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# برای JWT Bearer در Swagger و /auth/me
bearer_scheme = HTTPBearer()


# ================= تنظیمات دیتابیس (SQLite) =================

SQLALCHEMY_DATABASE_URL = "sqlite:///./iam.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # مخصوص SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String, nullable=True)  # 👈 کد تأیید
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


# ================= مدل‌های Pydantic =================


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserVerify(BaseModel):
    email: EmailStr
    code: str   # کدی که کاربر وارد می‌کند


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Message(BaseModel):
    message: str
    verification_code: Optional[str] = None   # برای نمایش کد تأیید در دمو


# ================= توابع کمکی =================


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    این تابع از HTTPBearer استفاده می‌کند.
    یعنی در هدر باید این‌طوری بفرستی:

        Authorization: Bearer <access_token>
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="توکن نامعتبر است.",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="توکن نامعتبر یا منقضی شده است.",
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="کاربر یافت نشد.",
        )

    return user


# ================= اپ اصلی FastAPI =================

app = FastAPI(title="IAM Service - FastAPI")


@app.get("/", response_model=Message)
def root():
    return {"message": "IAM Service is running"}


# ----------- ثبت‌نام کاربر جدید -----------
@app.post("/auth/register", response_model=Message, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="این ایمیل قبلاً ثبت شده است.",
        )

    password_hash = get_password_hash(user_in.password)

    # 👈 تولید کد تأیید ۶ رقمی
    verification_code = str(random.randint(100000, 999999))

    new_user = User(
        email=user_in.email,
        password_hash=password_hash,
        is_verified=False,
        verification_code=verification_code,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # برای دمو: چاپ در ترمینال
    print(f"Verification code for {new_user.email} -> {verification_code}")

    # برای دمو: برگرداندن کد در پاسخ (در عمل واقعی این کار رو نمی‌کنیم)
    return {
        "message": "ثبت‌نام انجام شد. لطفاً کد تأیید ارسال‌شده را وارد کنید.",
        "verification_code": verification_code,
    }


# ----------- تأیید حساب کاربر -----------
@app.post("/auth/verify", response_model=Message)
def verify(user_verify: UserVerify, db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_verify.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="کاربر یافت نشد.",
        )

    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="این حساب قبلاً تأیید شده است.",
        )

    if not user.verification_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="برای این حساب کد تأیید ثبت نشده است.",
        )

    # 👈 این‌جا واقعا کد رو چک می‌کنیم
    if user_verify.code != user.verification_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="کد تأیید اشتباه است.",
        )

    user.is_verified = True
    user.verification_code = None  # بعد از تأیید، کد را پاک می‌کنیم
    db.commit()

    return {"message": "حساب شما با موفقیت تأیید شد."}


# ----------- ورود کاربر و دریافت JWT -----------
@app.post("/auth/login", response_model=Token)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_login.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ایمیل یا رمز عبور نادرست است.",
        )

    if not verify_password(user_login.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ایمیل یا رمز عبور نادرست است.",
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="حساب شما هنوز تأیید نشده است.",
        )

    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )

    return {"access_token": access_token, "token_type": "bearer"}


# ----------- دریافت اطلاعات کاربر فعلی -----------
@app.get("/auth/me")
def read_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "is_verified": current_user.is_verified,
        "created_at": current_user.created_at,
    }
