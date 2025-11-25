from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Infrastructure.Data.database import init_db
from API.Controllers import customer_controller, item_controller, order_controller

app = FastAPI(title="Sales Order Management API", version="1.0.0")

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(customer_controller.router)
app.include_router(item_controller.router)
app.include_router(order_controller.router)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def home():
    return {"status": "running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
