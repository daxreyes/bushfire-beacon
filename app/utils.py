from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional, Union
from uuid import UUID

from passlib.context import CryptContext
import emails
from emails.template import JinjaTemplate
from jose import jwt
from loguru import logger

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["ssl"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    if settings.EMAILS_ENABLED:
        response = message.send(to=email_to, render=environment, smtp=smtp_options)
        logger.info(f"send email result: {response}")
    else:
        logger.info("Email sending currently disabled")
        logger.info(f"send email: {email_to}, {message.html.render(**environment)}")


def send_test_email(email_to: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": settings.PROJECT_NAME, "email": email_to},
    )


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    server_host = settings.SERVER_HOST
    link = f"{server_host}/#/reset-password/{token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def send_new_account_email(email_to: str, username: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account verification for user {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template_str = f.read()
    link = f"{settings.SERVER_HOST}/#/confirm-registration/{token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "email": email_to,
            "link": link,
            "valid_hours": settings.ACCOUNT_VERIFY_EXPIRE_HOURS,
        },
    )


def send_new_account_info(email_to: str, username: str, full_name: str, about: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account created for {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account_info.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "email": email_to,
            "full_name": full_name,
            "about": about,
        },
    )


def send_welcome_email(email_to: str, username: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Welcome {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "welcome_confirmed.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
        },
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return {"access_token": encoded_jwt, "token_type": "bearer", "expires_in": expire}


def generate_verification_token(user_id: UUID) -> str:
    """token for registration token"""
    delta = timedelta(hours=settings.ACCOUNT_VERIFY_EXPIRE_HOURS)
    now = datetime.utcnow()
    encoded_jwt = jwt.encode(
        {"exp": now + delta, "nbf": now, "sub": str(user_id), "aud": "account:verification"},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def decode_verification_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            audience="account:verification",
        )
        return decoded_token
    except jwt.JWTError:
        logger.exception(f"Unable to decode token {token}")
        return None


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    encoded_jwt = jwt.encode(
        {"exp": expires, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        logger.info(f"decoded token:{decoded_token}")
        return decoded_token["sub"]
    except jwt.JWTError as err:
        logger.error(f"ERROR: {err}")
        return None
