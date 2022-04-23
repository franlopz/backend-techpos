from fastapi import Depends, FastAPI, HTTPException, status
from datetime import datetime, timedelta
from routers import (cities, companies, pagos, productos,
                     states, summary, tickets, proveedores,
                     compras, gastos, token, company_accounts,
                     roles, users)
from database import *
from starlette.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional
from pydantic import BaseModel

app = FastAPI(title='Contact.ly',
              description='APIs for contact Apis',
              version='0.1'
              )

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(token.router_token)
app.include_router(productos.router_productos)
app.include_router(pagos.router_pagos)
app.include_router(tickets.router_tickets)
app.include_router(compras.router_compras)
app.include_router(proveedores.router_proveedores)
app.include_router(gastos.router_gastos)
app.include_router(summary.router_summary)
app.include_router(cities.router_cities)

app.include_router(states.router_states)

app.include_router(companies.router_companies)

app.include_router(company_accounts.router_companies_accounts)

app.include_router(roles.router_roles)

app.include_router(users.router_users)
