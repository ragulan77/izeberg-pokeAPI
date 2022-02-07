from operator import contains
from fastapi import FastAPI, HTTPException, Depends
from starlette.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN
import requests
from config import *
from auth.routes import app as router
from auth.auth import AuthHandler
from sql_app import schemas
from sql_app.crud import add_type_to_user, get_user_by_login
from sql_app.database import SessionLocal


app = FastAPI()
app.include_router(router)

auth_handler = AuthHandler()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/group/{type}/add")
async def add_group(type: str, db: SessionLocal = Depends(get_db), token=Depends(auth_handler.auth_wrapper)):
    get_test_url = f"{POKEAPI_TYPE_URL}/{type}"
    test_get_response = requests.get(get_test_url)

    # check if the pokeAPI returned an answer
    if test_get_response.status_code == 200 and test_get_response.json() is not None:
        type_to_add = schemas.TypeBase(name=type)
        add_type_to_user(db, type_to_add, "ragulan")
        return 
    else:
        return HTTPException(status_code=HTTP_404_NOT_FOUND)

@app.get("/api/pokemon")
async def get_pokemons(db: SessionLocal = Depends(get_db), token=Depends(auth_handler.auth_wrapper)):
    me = get_user_by_login(db, token['login'])
    pokemons = []
    for type in me.types:
        get_test_url = f"{POKEAPI_TYPE_URL}/{type.name}"
        test_get_response = requests.get(get_test_url)
        # check if the pokeAPI returned an answer
        if test_get_response.status_code == 200 and test_get_response.json() is not None:
            pokemons.append(test_get_response.json().get("pokemon"))
    return pokemons


@app.get("/api/pokemon/{pokemon_name}")
async def get_pokemon(pokemon_name: str, db: SessionLocal = Depends(get_db), token=Depends(auth_handler.auth_wrapper)):
    get_test_url = f"{POKEAPI_POKEMON_URL}/{pokemon_name}"
    test_get_response = requests.get(get_test_url)

    # check if the pokeAPI returned an answer
    if test_get_response.status_code == 200 and test_get_response.json() is not None:
        pokemon = test_get_response.json()
        me = get_user_by_login(db, token['login'])
        for pokemonType in pokemon["types"]:
            #TODO : check user's types
            for myType in me.types:
                if myType.name == pokemonType["type"]["name"]:
                    return pokemon
        return HTTPException(status_code=HTTP_403_FORBIDDEN)
    else:
        return HTTPException(status_code=HTTP_404_NOT_FOUND)

