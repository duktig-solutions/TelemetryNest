from fastapi import Depends, FastAPI

from .dependencies import get_token_header
from .internal import admin
from .routers import auth, items, profile, kpis, predicted_alarms

app = FastAPI()
# dependencies=[Depends(get_query_token)]

app.include_router(items.router)
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(kpis.router)
app.include_router(predicted_alarms.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
