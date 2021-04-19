from fastapi import  Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from configparser import ConfigParser

security_scheme = HTTPBasic()


def check_credentials(credentials: HTTPBasicCredentials = Depends(security_scheme)):
    valid_login = False

    login_information = ConfigParser()
    login_information.read('config.ini')
    login_information = login_information['CREDENTIALS']
    if credentials.username in login_information:
        if login_information[credentials.username] == credentials.password:
            valid_login = True

    if not valid_login:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    else:
        return credentials.username