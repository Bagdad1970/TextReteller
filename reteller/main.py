from aiohttp.web_exceptions import HTTPBadRequest, HTTPInternalServerError
import src.reteller_models as retellers
from aiohttp import web
import json


RETELL_SERVICE_ADDRESS = "127.0.0.1"
RETELL_SERVICE_PORT = 8002

routes = web.RouteTableDef()

#model = retellers.RuT5Reteller()

@routes.post('/retell')
async def retell(request: web.Request) -> web.Response:
    try:
        data = await request.json()
        text = data.get("text", "").strip()
        max_length = int(data.get("correlation", 100))

        if not text:
            raise HTTPBadRequest(text='Text cannot be empty')

        if max_length < 0:
            raise HTTPBadRequest(text="Text length cannot be negative")

        #retelled_text = model.summarize(text, max_length)
        return web.json_response(
                            { "retelled_text" : 'Заглушка' },
                                 status=200)

    except json.JSONDecodeError:
        raise HTTPBadRequest(text='Invalid JSON data')
    except Exception as error:
        HTTPInternalServerError(text=f"Error shortening text: {str(error)}")

@routes.get('/')
async def root() -> web.Response:
    return web.json_response(
        {"message": "Reteller service is running"},
        status=200
    )

app = web.Application()
app.add_routes(routes)

if __name__ == "__main__":
    web.run_app(app, host=RETELL_SERVICE_ADDRESS, port=RETELL_SERVICE_PORT)