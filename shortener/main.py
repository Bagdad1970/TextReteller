from src.entity_finder import EntityFinder
from src.text_parser import TextParser
import src.entities_by_proportion as entities_by_proportion
from src.text_shortener import TextShortener
import src.semantic_processing as semantics


def short_text(text: str, correlation: float) -> str:
    text_parser = TextParser(text)
    parsed_text = text_parser.get_parsed_text()

    entity_finder = EntityFinder(parsed_text)
    entity_dict = entity_finder.find_simple_entities()

    semantic_analyzer = semantics.SemanticAnalyzer(parsed_text, entity_dict)
    semantic_analyzer.importance_of_entities()
    couples_of_vertex = semantic_analyzer.relation_of_entities()

    graph = semantics.RelationGraph(couples_of_vertex)
    graph.traverse_and_update_coherence()
    weighted_vertexes = graph.get_weighted_vertexes()

    entity_dict.attach_entity_mains(weighted_vertexes)

    _week_entities = entities_by_proportion.get_weak_entities(entity_dict, correlation)
    _strong_entities = entities_by_proportion.get_strong_entities(entity_dict, correlation)

    text_shortener = TextShortener(
        parsed_text=parsed_text,
        entity_dict=entity_dict,
        weak_entity_dict=_week_entities
    )

    return text_shortener.short_text()



SHORT_SERVICE_ADDRESS = "0.0.0.0"
SHORT_SERVICE_PORT = 8001

from aiohttp import web
import json
routes = web.RouteTableDef()


@routes.post('/short')
async def shorten(request: web.Request) -> web.Response:
    try:
        data = await request.json()
        text = data.get("text", "").strip()
        correlation = float(data.get("correlation", 0.5))

        if not text:
            return web.json_response(
                {"error": "Text cannot be empty"},
                status=400
            )

        if correlation > 1.0 or correlation < 0:
            return web.json_response(
                {"error": "Correlation must be in [0.0, 1.0]"},
                status=400
            )

        return web.json_response(
                                { "shortened_text" : short_text(text, correlation) },
                                 status=200)

    except json.JSONDecodeError:
        return web.json_response(
            {"error": "Invalid JSON data"},
            status=400
        )
    except Exception as error:
        return web.json_response(
            {"error": f"Error shortening text: {str(error)}"},
            status=500
        )

@routes.get('/')
async def root() -> web.Response:
    return web.json_response(
        {"message": "Shortener service is running"},
        status=200
    )

app = web.Application()
app.add_routes(routes)

if __name__ == "__main__":
    web.run_app(app, host=SHORT_SERVICE_ADDRESS, port=SHORT_SERVICE_PORT)