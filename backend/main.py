from fastapi import FastAPI, HTTPException
import httpx
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

SHORT_SERVICE_ADDRESS = RETELL_SERVICE_ADDRESS = '0.0.0.0'
SHORT_SERVICE_PORT, RETELL_SERVICE_PORT = 8001, 8002

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080",
                   "http://text-reteller.k-lab.su"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RetellerInput(BaseModel):
    text: str
    max_length: int

class ShortenerInput(BaseModel):
    text: str
    correlation: float = 0.5

class Input(BaseModel):
    text: str
    max_length: int
    correlation: float = 0.5


@app.post('/short')
async def short(shortener_input: ShortenerInput):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f'http://{SHORT_SERVICE_ADDRESS}:{SHORT_SERVICE_PORT}/short',
                headers={'Content-Type': 'application/json'},
                json=shortener_input.model_dump(),
            )
            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Error from shortening service: {e.response.text}"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Could not connect to reteller service: {str(e)}"
        )


@app.post('/retell')
async def retell(reteller_input: RetellerInput):
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            print(reteller_input)
            response = await client.post(
                f'http://{RETELL_SERVICE_ADDRESS}:{RETELL_SERVICE_PORT}/retell',
                headers={'Content-Type': 'application/json'},
                json=reteller_input.model_dump(),
            )
            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Error from reteller service: {e.response.text}"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Could not connect to reteller service: {str(e)}"
        )


@app.post('/api/summarize')
async def summarize(input: Input):
    try:
        async with httpx.AsyncClient(timeout=25) as client:

            shortener_input = ShortenerInput(text=input.text, correlation=input.correlation)
            shortener_response = await client.post(
                f'http://localhost:{SHORT_SERVICE_PORT}/short',
                headers={'Content-Type' : 'application/json'},
                json=shortener_input.model_dump(),
            )
            shortener_response.raise_for_status()
            shortener_data = shortener_response.json()

            reteller_input = RetellerInput(text=shortener_data.get('shortened_text'), max_length=input.max_length)
            reteller_response = await client.post(
                f'http://localhost:{RETELL_SERVICE_PORT}/retell',
                headers={'Content-Type': 'application/json'},
                json=reteller_input.model_dump(),
            )
            reteller_response.raise_for_status()

            return { **reteller_response.json(), **shortener_response.json() }

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Error from service: {e.response.text}"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Could not connect to service: {str(e)}"
        )