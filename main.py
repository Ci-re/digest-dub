from fastapi import FastAPI
from pydantic import BaseModel
from app.service.coldstart import predict

app = FastAPI()

class UserPreferences(BaseModel):
    course: str
    allergy: str
    intolerance: str

@app.post("/users/")
async def read_user(user: UserPreferences):
    user_dict = user.dict()
    result = predict(entries = user_dict).reset_index()
    result = result.head(10).to_dict()
    return result


@app.get("/items/{item_id}")
async def read_items(item_id : int):
    return {"item_id": item_id+45}
