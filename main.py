from fastapi import FastAPI, HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN
import requests
from config import *
from auth.routes import app as router

app = FastAPI()
app.include_router(router)

@app.get("/api/login")
async def login():
    return {"message": "LOGIN"}


@app.get("/api/group/{type}/add")
async def add_group(type: str):
    get_test_url = f"{POKEAPI_TYPE_URL}/{type}"
    test_get_response = requests.get(get_test_url)

    # check if the pokeAPI returned an answer
    if test_get_response.status_code == 200 and test_get_response.json() is not None:
        return test_get_response.json()
    else:
        return HTTPException(status_code=HTTP_404_NOT_FOUND)

#TODO : check user's type instead of type param
@app.get("/api/pokemon")
async def get_pokemons(type: str):
    get_test_url = f"{POKEAPI_TYPE_URL}/{type}"
    test_get_response = requests.get(get_test_url)

    # check if the pokeAPI returned an answer
    if test_get_response.status_code == 200 and test_get_response.json() is not None:
        return test_get_response.json().get("pokemon")
    else:
        return HTTPException(status_code=HTTP_404_NOT_FOUND)


@app.get("/api/pokemon/{pokemon_name}")
async def get_pokemon(pokemon_name: str):
    get_test_url = f"{POKEAPI_POKEMON_URL}/{pokemon_name}"
    test_get_response = requests.get(get_test_url)

    # check if the pokeAPI returned an answer
    if test_get_response.status_code == 200 and test_get_response.json() is not None:
        pokemon = test_get_response.json()
        for pokemonType in pokemon["types"]:
            #TODO : check user's types
            if pokemonType["type"]["name"] == "grass": 
                return pokemon
        else:
            return HTTPException(status_code=HTTP_403_FORBIDDEN)
    else:
        return HTTPException(status_code=HTTP_404_NOT_FOUND)

