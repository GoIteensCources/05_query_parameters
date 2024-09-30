from datetime import datetime
from typing import Optional

import uvicorn
from fastapi import FastAPI, Path, Query, Body, Header, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from pydantic import BaseModel

app = FastAPI()

items = [
    {"id": 1,
     "title": "Lorem ipsum",
     "descr": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
              "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
              " Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
              "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
     "time": "12.09.2024"
     },
]


class Item(BaseModel):
    title: str
    descr: Optional[str] = None
    time_create: datetime = datetime.now()
    type: bool = True
    age: int


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")


# Path parameters
@app.get("/item/{id_}/")
def get_item_by_id(id_: int = Path(description="id item")):
    return items[id_]


# Query parameters
@app.get("/item/")
def get_items_or_item_by_id(id_:  Optional[int] = Query(None, description="mult for title")):
    return items[id_] if id_ else items


#body parameter
@app.post("/item/{id_}/")
def add_item(id_: int = Path(description="id item"),
             item: Item = Body(description="body parameters")):
    item_dict = item.model_dump()
    if id_ not in [i["id"] for i in items]:
        item_dict["id"] = id_
    else:
        item_dict["id"] = len(items) + 1
    items.append(item_dict)
    return item


# header
@app.get("/head")
def get_headers(user_agent: str = Header(None),
                x_token: str = Header()):
    if x_token == "secret":
        return {"user_agent": user_agent,
                "x_token": x_token}
    raise HTTPException(400, detail="x_token not correct")


@app.get("/info")
def info(accept: str = Header("application/json")):
    if "application/json" in accept:
        return JSONResponse({"message": "its JSon", "accept": accept})

    elif "text/html" in accept:
        return HTMLResponse(f"<html> <body> <h1>HTML</h1> <p>{accept}</p> </body> <!html>")

    else:
        raise HTTPException(400)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
