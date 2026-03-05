# main.py

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.user import router as auth_router  # adjust path/name if different


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("🚀 Auth Server starting up...")
    yield

    # Shutdown logic
    print("🛑 Auth Server shutting down...")
    # e.g., close any global resources here


app = FastAPI(
    title="Auth Server",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS: allow your frontend(s) to call this auth service
# In dev you can just use ["*"], later lock it down to your domains.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # e.g. ["https://your-frontend.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# ROUTES
# -------------------------

@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Microservice routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
