import datetime

import fastapi
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError
from pydantic import EmailStr

import schemas
import database
import exceptions


# to get a random 32 bit encrypted key
# run openssl rand -hex 32
SECRET_KEY = "2d08be3f8eb7cb41b8419df4bfc757c9202836aa93e4146f8445c904cf0ba0ac"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pass_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# use OAuth2 scheme to get the token
oauth2scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password: str) -> str:
    """converts plain password into hash

    Args:
        password (str):

    Returns:
        str: the hash from the password
    """
    return pass_ctx.hash(password)


def verify_password(plain_password: str, hash_password: str) -> bool:
    """uses the passlib context to verify the password

    Args:
        plain_password (str): the plain password sent from the request
        hash_password (str): the hash found in the database

    Returns:
        bool: True if password matches or False if doesnt
    """
    return pass_ctx.verify(plain_password, hash_password)


def authenticate_user(username: EmailStr, password: str) -> schemas.User:
    """authenticates the user by looking up the username in the database and then verifying the password

    Args:
        username (str): the username to search
        password (str): the password to verify

    Raises:
        exceptions.AuthenticationError: if the username or password is incorrect
        LookupError: if no user found

    Returns:
        schemas.User: the user object
    """
    user = get_user(username)
    if not user or not verify_password(password, user.password):
        raise exceptions.AuthenticationError("Incorrect username or password")
    return user


def get_user(username: EmailStr) -> schemas.UserInDB:
    """
    gets the user from the database

    Args:
        username (str): the username to search

    Raises:
        LookupError: if no user found

    Returns:
        schemas.UserInDB: the user object
    """
    db_response = database.base_users.fetch({"email": username})
    if db_response.count == 0:
        raise LookupError("No user found")
    # get the first item found in the database
    item = db_response.items[0]
    user = schemas.UserInDB(**item)
    return user


async def get_current_user(token: str = Depends(oauth2scheme)) -> schemas.UserInDB:
    """
    decodes the token string into a dict and returns UserInDB if validated

    Args:
        token (str, optional): _description_. token to be auth to Depends(oauth2scheme).

    Raises:
        credentials_exception: raises a 401 if the token is invalid, expired or if the user is not found

    Returns:
        schemas.UserInDB: the user object
    """
    credentials_exception = fastapi.HTTPException(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # decode the token str into dict from secret key and the algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # get the username from decoded string
        username = payload.get("sub")
        if username is None:
            # if no user found in the token then raise a 401
            raise credentials_exception
        # validate the username from the token
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    # lookup the user from the database
    try:
        user = get_user(username=token_data.username)
    except LookupError:
        raise credentials_exception
    else:
        return user


async def get_current_active_user(
    current_user: schemas.User = Depends(get_current_user),
) -> schemas.User:
    """checks if the user is active or not

    Args:
        current_user (schemas.User, optional): _description_. Defaults to Depends(get_current_user).

    Raises:
        fastapi.HTTPException: raise a 400 Bad Request if user is inactive

    Returns:
        schemas.User:
    """
    if current_user.disabled:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


async def get_current_active_admin(
    current_user: schemas.User = Depends(get_current_user),
) -> schemas.User:
    """validates that this user is a admin and active

    Args:
        current_user (schemas.User, optional): _description_. Defaults to Depends(get_current_user).

    Raises:
        fastapi.HTTPException: 403 if checks fail

    Returns:
        schemas.User:
    """
    if current_user.disabled or not current_user.is_admin:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this request",
        )
    return current_user


def create_access_token(data: dict, expires_delta: datetime.timedelta) -> str:
    """
    generates an access token with an optional expiration
    time by encoding a dictionary using the JSON Web Token (JWT) format and a secret key.

    Args:
        data (dict): adds the expiration time to the data dictionary
        td (datetime.timedelta): expiration time

    Returns:
        str: the encoded JWT as the access token
    """
    # Make a copy of the data dictionary to prevent modifying the original data
    to_encode = data.copy()

    # Calculate the expiration time for the token based on the `expires_delta` parameter
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

    # Add the expiration time to the `to_encode` dictionary
    to_encode.update({"exp": expire})

    # Encode the `to_encode` dictionary as a JWT using the `SECRET_KEY` and `ALGORITHM`
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # Return the encoded JWT as the access token
    return encoded_jwt


router = fastapi.APIRouter(prefix="/users")


@router.post(
    "/token", response_model=schemas.Token, status_code=fastapi.status.HTTP_200_OK
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    """
    logs in the user and returns a JWT token

    Args:
        form_data (OAuth2PasswordRequestForm, optional): Defaults to Depends().

    Raises:
        fastapi.HTTPException: raises a 401 if the user could not be authenticated

    Returns:
        dict: access_token, token_type, user: User
    """
    try:
        user = authenticate_user(form_data.username, form_data.password)
    except (exceptions.AuthenticationError, LookupError):
        raise fastapi.HTTPException(
            fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # generate a JWT
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    try:
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
    except JWTError as err:
        raise fastapi.HTTPException(
            fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, err.__str__()
        )
    # remove the password when returning
    user = schemas.User(**user.dict())
    return_value = {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user,
    }
    return return_value


@router.get("/token")
async def generate_password_hash(
    plain_password: str, current_admin: schemas.User = Depends(get_current_active_admin)
):
    """for admin use only for testing

    Args:
        plain_password (str): _description_
        current_admin (schemas.User, optional): _description_. Defaults to Depends(get_current_active_admin).

    Returns:
        _type_: password: str, hash: str
    """
    hash = get_password_hash(plain_password)
    return {"password": plain_password, "hash": hash}


@router.get("/info")
async def get_user_info(current_user: schemas.User = Depends(get_current_active_user)):
    """get the currently active user information

    Raises:
        401 if not valid

    Args:
        current_user (schemas.User, optional): _description_. Defaults to Depends(get_current_active_user).
    """

    return current_user
