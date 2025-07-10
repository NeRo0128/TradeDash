from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .routes import auth, users, products, orders, reports
from .database import engine, Base
from .utils.error_handlers import (
    database_error_handler,
    validation_error_handler,
    general_error_handler
)
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    Base.metadata.create_all(bind=engine)
    yield
    # Clean up resources on shutdown
    # You can add cleanup code here if needed

app = FastAPI(
    title="TradeDash API",
    description="Backend API for TradeDash restaurant management system",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register error handlers
app.add_exception_handler(SQLAlchemyError, database_error_handler)
app.add_exception_handler(HTTPException, validation_error_handler)
app.add_exception_handler(Exception, general_error_handler)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(reports.router)

@app.get("/")
async def root():
    return {"message": "Welcome to TradeDash API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)