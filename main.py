from fastapi import FastAPI
from contextlib import asynccontextmanager

# If you have routers
# from routers import auth_router, user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("🚀 Server starting up...")

    yield

    # Shutdown logic
    print("🛑 Server shutting down...")


app = FastAPI(
    title="Auth Server",
    version="0.1.0",
    lifespan=lifespan
)


# -------------------------
# ROUTES
# -------------------------

@app.get("/health")
async def health_check():
    return {"status": "ok"}


# If using routers:
# app.include_router(auth_router, prefix="/auth", tags=["auth"])
# app.include_router(user_router, prefix="/users", tags=["users"])