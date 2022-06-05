from datetime import datetime
import os
from core.generate_password import generate_pass
from core.hashing import Hasher
from core.send_email import send_email_async
import crud.token
from fastapi import HTTPException, status
from core.is_email import is_email
from database import *
from models.client_credential import Client_credential
from models.company import Company
from models.company_account import Company_account
from models.role import Role
from models.status import Status
from models.user import User


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


    for user in users:
        password = generate_pass()
        password_hash = Hasher.get_password_hash(password+hexsalt)
        print(password_hash, hexsalt)
        now = datetime.datetime.utcnow()

        if not(is_email(user.email)):
            return "Email not valid"

        if user.firstName == "" or user.lastName == "":
            return "First name or last name empty"

        email_exists = User.get_or_none(User.email == user.email)
        company_id = Company.get_or_none(
            Company.uuid == user.uuid)

        role_result =Role.get_or_none(Role.roleName == user.role)

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

        user_result = User.insert(email=user.email,
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


    return "User saved"


def change_password(form, current_user):


    salt = os.urandom(10)
    hexsalt = salt.hex()
    user = crud.token.auth_user(current_user.email, form.password)
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
    query = User.update(passwordHash=password_hash, passwordSalt=hexsalt).where(
        User.email == current_user.email)
    result = query.execute()



    if result > 0:
        return 'Password changed'


def get_users(current_user):



    data = []

    company_account_by_user = Company_account.get_or_none(
        Company_account.userId == current_user.id)

    company = Company.get_by_id(
        company_account_by_user.companyId)

    company_accounts = list(Company_account.select().where(
        Company_account.companyId == company_account_by_user.companyId))

    for account in company_accounts:
        if account.userId is not None:
            user_result = User.get_by_id(account.userId)
            role_result =Role.get_or_none(
               Role.id == user_result.roleId)
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



    return data


def get_app_credentials(current_user):



    data = {}
    company_account_by_user = Company_account.get_or_none(
        Company_account.userId == current_user.id)

    company = Company.get_by_id(
        company_account_by_user.companyId)

    company_accounts = list(Company_account.select().where(
        Company_account.companyId == company_account_by_user.companyId))

    for account in company_accounts:
        if account.appId is not None:
            credentials = Client_credential.get_or_none(
                Client_credential.app_id == account.appId
            )
            data = {
                "appId": credentials.app_id,
                "appKey": credentials.app_key
            }



    return data


def in_same_company(user, current_user):



    user_result = User.get_or_none(User.email == user.email)
    user_accounts = Company_account.select().where(
        Company_account.userId == user_result.id)
    current_user_accounts = Company_account.select().where(
        Company_account.userId == current_user.id)



    if user_accounts is not None and current_user_accounts is not None:
        for user_account in user_accounts:
            for current_user_account in current_user_accounts:
                if user_account.companyId == current_user_account.companyId:
                    return True
        return False


def can_perform_action(user, current_user, action=None):



    user_in_db = User.get_or_none(User.email == user.email)
    if current_user.email != user.email:
        if current_user.roleId >= user_in_db.roleId:
            raise HTTPException(
                status_code=404, detail="Not able to perform action")

    role_result =Role.get_or_none(Role.roleName == user.role)



    if current_user.email == user.email:
        if action == 'delete':
            raise HTTPException(
                status_code=404, detail="Not able to perform action")
        if current_user.roleId > role_result.id:
            raise HTTPException(
                status_code=404, detail="Not able to perform action")


def modify_users(users, current_user):



    for user in users:

        can_perform_action(user, current_user)

        role_result =Role.get_or_none(Role.roleName == user.role)

        status_result = Status.get_or_none(Status.name == user.statusEn)

        if status_result is None:
            return "Status not valid"

        if status_result.name == "active" or status_result.name == "inactive":

            users_related = in_same_company(user, current_user)

            if users_related:
                query = User.update(firstName=user.firstName,
                                     lastName=user.lastName,
                                     status=user.statusEn,
                                     roleId=role_result.id).where(
                    User.email == user.email
                )
                result = query.execute()
            else:
                result = "Not able to update user"

    return result


def delete_users(users, current_user):



    for user in users:

        can_perform_action(user, current_user, 'delete')

        users_related = in_same_company(user, current_user)

        if users_related:
            # query = Users.delete().where(Users.email == user.email)
            user_in_db = User.get_or_none(User.email == user.email)
            user_in_db.delete_instance()

            user_accounts = Company_account.select().where(
                Company_account.userId == user_in_db.id)

            for user_account in user_accounts:
                company_in_db = Company_account.get_or_none(
                    Company_account.userId == user_account.userId)
                company_in_db.delete_instance()
                # Company_account.delete().where(Company_account.userId == user_account.userId)
        result = 'Users deleted'

    return result
