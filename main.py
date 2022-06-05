import time
from fastapi import Depends, FastAPI,Request
from routers import (cities, companies, expenses, payments, products, purchases,
                     states, summary, suppliers, tickets, token, company_accounts,
                     roles, users)
from database import *
from starlette.middleware.cors import CORSMiddleware

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

async def reset_db_state():
    conn._state._state.set(db_state_default.copy())
    conn._state.reset()
    
def get_db(db_state=Depends(reset_db_state)):
    try:
        conn.connect()
        yield
    finally:
        if not conn.is_closed():
            conn.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}
app.include_router(token.router_token,dependencies=[Depends(get_db)])
app.include_router(products.router_productos,dependencies=[Depends(get_db)])
app.include_router(payments.router_pagos,dependencies=[Depends(get_db)])
app.include_router(tickets.router_tickets,dependencies=[Depends(get_db)])
app.include_router(purchases.router_compras,dependencies=[Depends(get_db)])
app.include_router(suppliers.router_proveedores,dependencies=[Depends(get_db)])
app.include_router(expenses.router_gastos,dependencies=[Depends(get_db)])
app.include_router(summary.router_summary,dependencies=[Depends(get_db)])
app.include_router(cities.router_cities,dependencies=[Depends(get_db)])
app.include_router(states.router_states,dependencies=[Depends(get_db)])
app.include_router(companies.router_companies,dependencies=[Depends(get_db)])
app.include_router(company_accounts.router_companies_accounts,dependencies=[Depends(get_db)])
app.include_router(roles.router_roles,dependencies=[Depends(get_db)])
app.include_router(users.router_users,dependencies=[Depends(get_db)])
