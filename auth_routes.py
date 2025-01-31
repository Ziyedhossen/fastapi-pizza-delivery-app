from curses.ascii import alt
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from database import Session, engine
from schemas import SignUpModel, LoginModel
from models import User
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
import bcrypt


def generate_password_hash(password: str) -> str:
    # bcrypt automatically generates a salt and prefixes it to the hash
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')  # Store as a string

def check_password_hash(stored_hash: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))



auth_routes = APIRouter(prefix= '/auth', tags=['Auth'])



session = Session(bind=engine)

@auth_routes.get('/')
async def hello(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    return {'massage': 'Hello world!'}

@auth_routes.post('/signup', response_model=SignUpModel, status_code=status.HTTP_201_CREATED)
async def signup(user:SignUpModel):
    db_email=session.query(User).filter(User.email==user.email).first()

    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="User with the email already exists"                     
                             )
    
    db_username=session.query(User).filter(User.username==user.username).first()

    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="User with the username already exists"                     
                             )

    new_user = User(
        username = user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        # password=generate_password_hash(user.password.encode('utf-8'), salt),
        is_active = user.is_active,
        is_staff = user.is_staff
    )

    session.add(new_user)
    session.commit()

    return new_user

# login routes

@auth_routes.post('/login', status_code=200)
async def login(user:LoginModel, Authorize:AuthJWT=Depends()):
    db_user=session.query(User).filter(User.username==user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)

        response = {
            "access": access_token,
            "refresh": refresh_token
        }

        return jsonable_encoder(response)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                        detail="Invalid Username or Password"
                        )



# refreshing tokens

@auth_routes.get('/refresh')
async def refresh_token(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please provide a valid refresh token")
    
    current_user = Authorize._get_jwt_identifier()

    access_token = Authorize.create_access_token(subject=current_user)

    return jsonable_encoder({"access":access_token})
        