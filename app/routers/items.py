from fastapi import APIRouter, Depends, HTTPException
from typing_extensions import Annotated
from ..dependencies import decode_jwt

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(decode_jwt)],
    responses={404: {"description": "Not found"}},
)

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}
tokenPayload = Annotated[dict, Depends(decode_jwt)]


@router.get("/test-payload")
async def read_items(payload: tokenPayload):

    data = {
        'item_data': 555,
        'user_email_from_token_payload': payload['email'],
        'total_token_payload': payload
    }

    return data


@router.get("/")
async def read_items():
    return fake_items_db


@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}
