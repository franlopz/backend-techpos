import models.token
from fastapi import HTTPException, status
from sqlalchemy import true
from core.is_email import is_email
from models import role
import models.company
from core.generate_password import generate_pass
from core.send_email import send_email_async, send_email_background
from models.company_account import Company_account
from peewee import *
from .Base import BaseModel
from database import *
import os
from core.hashing import Hasher
import datetime


class Users(BaseModel):
    email = CharField(max_length=255)
    firstName = CharField(max_length=255)
    lastName = CharField(max_length=255)
    passwordSalt = CharField(max_length=255)
    passwordHash = CharField(max_length=255)
    createdDate = DateTimeField()
    status = CharField(max_length=255)
    loginTries = IntegerField()
    roleId = IntegerField()

    class Meta:
        db_table = 'users'


class Status(BaseModel):
    id = IntegerField()
    name = CharField(max_length=45)

    class Meta:
        db_table = 'status'


class App_credentials(BaseModel):
    id = IntegerField()
    app_id = CharField(max_length=255)
    app_key = CharField(max_length=255)

    class Meta:
        db_table = 'client_credential'


def generateFakePass():
    salt = os.urandom(10)
    hexsalt = salt.hex()
    password = generate_pass()
    password_hash = Hasher.get_password_hash(password+hexsalt)
    print(password, password_hash + ' xx ' + hexsalt)
    return


def create_users(users, current_user):

    salt = os.urandom(10)
    hexsalt = salt.hex()
    # try:
    if conn.is_closed():
        conn.connect()

    for user in users:
        password = generate_pass()
        password_hash = Hasher.get_password_hash(password+hexsalt)
        print(password_hash, hexsalt)
        now = datetime.datetime.utcnow()

        if not(is_email(user.email)):
            return "Email not valid"

        if user.firstName == "" or user.lastName == "":
            return "First name or last name empty"

        email_exists = Users.get_or_none(Users.email == user.email)
        company_id = models.company.Company.get_or_none(
            models.company.Company.uuid == user.uuid)

        role_result = role.Role.get_or_none(role.Role.roleName == user.role)

        if email_exists is not None:
            return "Email already registered."

        if company_id is None:
            return "Company not registered"

        if role_result is None:
            return "Invalid role"

        if current_user.roleId > role_result.id:
            return "Forbidden transaction"

        send_email_async('Cuenta creada',
                         user.email,
                         {'title': 'Bienvenid@',
                          'name': user.firstName,
                          'password': password})

        user_result = Users.insert(email=user.email,
                                   firstName=user.firstName,
                                   lastName=user.lastName,
                                   roleId=role_result.id,
                                   passwordSalt=hexsalt,
                                   passwordHash=password_hash,
                                   createdDate=now,
                                   status="active",
                                   loginTries=0).execute()
        if company_id is not None:
            company_account_result = Company_account.insert(
                userId=user_result,
                companyId=company_id).execute()

    if not conn.is_closed():
        conn.close()
    return "User saved"


def change_password(form, current_user):
    if conn.is_closed():
        conn.connect()

    salt = os.urandom(10)
    hexsalt = salt.hex()
    user = models.token.auth_user(current_user.email, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if form.newpassword != form.passwordconfirm:
        raise HTTPException(
            status_code=404, detail="New password not matches with password confirm")

    password_hash = Hasher.get_password_hash(form.newpassword+hexsalt)
    query = Users.update(passwordHash=password_hash, passwordSalt=hexsalt).where(
        Users.email == current_user.email)
    result = query.execute()

    if not conn.is_closed():
        conn.close()

    if result > 0:
        return 'Password changed'


def get_users(current_user):

    if conn.is_closed():
        conn.connect()

    data = []

    company_account_by_user = Company_account.get_or_none(
        Company_account.userId == current_user.id)

    company = models.company.Company.get_by_id(
        company_account_by_user.companyId)

    company_accounts = list(Company_account.select().where(
        Company_account.companyId == company_account_by_user.companyId))

    for account in company_accounts:
        if account.userId is not None:
            user_result = Users.get_by_id(account.userId)
            role_result = role.Role.get_or_none(
                role.Role.id == user_result.roleId)
            data.append(
                {
                    "email": user_result.email,
                    "role": role_result.roleName,
                    "firstName": user_result.firstName,
                    "lastName": user_result.lastName,
                    "business": company.name,
                    "state": company.state,
                    "city": company.city,
                    "address": company.address,
                    "status": user_result.status,
                    "statusEn": user_result.status}
            )

    if not conn.is_closed():
        conn.close()

    return data


def get_app_credentials(current_user):

    if conn.is_closed():
        conn.connect()

    data = {}
    company_account_by_user = Company_account.get_or_none(
        Company_account.userId == current_user.id)

    company = models.company.Company.get_by_id(
        company_account_by_user.companyId)

    company_accounts = list(Company_account.select().where(
        Company_account.companyId == company_account_by_user.companyId))

    for account in company_accounts:
        if account.appId is not None:
            credentials = App_credentials.get_or_none(
                App_credentials.app_id == account.appId
            )
            data = {
                "appId": credentials.app_id,
                "appKey": credentials.app_key
            }

    if not conn.is_closed():
        conn.close()

    return data


def in_same_company(user, current_user):

    if conn.is_closed():
        conn.connect()

    user_result = Users.get_or_none(Users.email == user.email)
    user_accounts = Company_account.select().where(
        Company_account.userId == user_result.id)
    current_user_accounts = Company_account.select().where(
        Company_account.userId == current_user.id)

    if not conn.is_closed():
        conn.close()

    if user_accounts is not None and current_user_accounts is not None:
        for user_account in user_accounts:
            for current_user_account in current_user_accounts:
                if user_account.companyId == current_user_account.companyId:
                    return True
        return False


def can_perform_action(user, current_user, action=None):

    if conn.is_closed():
        conn.connect()

    user_in_db = Users.get_or_none(Users.email == user.email)
    if current_user.email != user.email:
        if current_user.roleId >= user_in_db.roleId:
            raise HTTPException(
                status_code=404, detail="Not able to perform action")

    role_result = role.Role.get_or_none(role.Role.roleName == user.role)

    if not conn.is_closed():
        conn.close()

    if current_user.email == user.email:
        if action == 'delete':
            raise HTTPException(
                status_code=404, detail="Not able to perform action")
        if current_user.roleId > role_result.id:
            raise HTTPException(
                status_code=404, detail="Not able to perform action")


def modify_users(users, current_user):

    if conn.is_closed():
        conn.connect()

    for user in users:

        can_perform_action(user, current_user)

        role_result = role.Role.get_or_none(role.Role.roleName == user.role)

        status_result = Status.get_or_none(Status.name == user.statusEn)

        if status_result is None:
            return "Status not valid"

        if status_result.name == "active" or status_result.name == "inactive":

            users_related = in_same_company(user, current_user)

            if users_related:
                query = Users.update(firstName=user.firstName,
                                     lastName=user.lastName,
                                     status=user.statusEn,
                                     roleId=role_result.id).where(
                    Users.email == user.email
                )
                result = query.execute()
            else:
                result = "Not able to update user"
    if not conn.is_closed():
        conn.close()
    return result


def delete_users(users, current_user):

    if conn.is_closed():
        conn.connect()

    for user in users:

        can_perform_action(user, current_user, 'delete')

        users_related = in_same_company(user, current_user)

        if users_related:
            # query = Users.delete().where(Users.email == user.email)
            user_in_db = Users.get_or_none(Users.email == user.email)
            user_in_db.delete_instance()

            user_accounts = Company_account.select().where(
                Company_account.userId == user_in_db.id)

            for user_account in user_accounts:
                company_in_db = Company_account.get_or_none(
                    Company_account.userId == user_account.userId)
                company_in_db.delete_instance()
                # Company_account.delete().where(Company_account.userId == user_account.userId)
        result = 'Users deleted'
    if not conn.is_closed():
        conn.close()
    return result
