from aiohttp import web
from aiohttp.web_urldispatcher import StaticResource
from yarl import URL

from aiohttp_apispec import setup_aiohttp_apispec


def test_app_swagger_url(aiohttp_app):
    def safe_url_for(route):
        if isinstance(route._resource, StaticResource):
            # url_for on StaticResource requires filename arg
            return None
        try:
            return route.url_for()
        except KeyError:
            return None

    urls = [safe_url_for(route) for route in aiohttp_app.app.router.routes()]
    assert URL("/v1/api/docs/api-docs") in urls


async def test_app_swagger_json(aiohttp_app, example_for_request_schema):
    resp = await aiohttp_app.get("/v1/api/docs/api-docs")
    docs = await resp.json()
    assert docs["info"]["title"] == "API documentation"
    assert docs["info"]["version"] == "0.0.1"
    operation = docs["paths"]["/v1/test"]["get"]
    parameters = {parameter["name"]: parameter for parameter in operation["parameters"]}
    assert parameters["bool_field"]["schema"] == {"type": "boolean"}
    assert parameters["id"]["schema"] == {"type": "integer"}
    assert parameters["list_field"] == {
        "explode": True,
        "in": "query",
        "name": "list_field",
        "required": False,
        "schema": {"items": {"type": "integer"}, "type": "array"},
        "style": "form",
    }
    assert parameters["name"]["schema"] == {"type": "string"}
    assert parameters["name"]["description"] == "name"
    assert parameters["nested_field"]["schema"] == {
        "$ref": "#/components/schemas/MyNested"
    }
    assert operation["responses"]["200"] == {
        "content": {
            "application/json": {
                "schema": {"$ref": "#/components/schemas/Response"},
            }
        },
        "description": "Success response",
    }
    assert operation["responses"]["404"] == {"description": "Not Found"}

    class_operation = docs["paths"]["/v1/class_echo"]["get"]
    class_parameters = {
        parameter["name"]: parameter for parameter in class_operation["parameters"]
    }
    assert class_parameters["nested_field"]["schema"] == {
        "$ref": "#/components/schemas/MyNested"
    }
    assert class_operation["responses"] == {}
    assert class_operation["summary"] == "View method summary"

    example_operation = docs["paths"]["/v1/example_endpoint"]["post"]
    assert example_operation["parameters"] == []
    assert example_operation["requestBody"] == {
        "required": False,
        "content": {
            "application/json": {
                "schema": {
                    "allOf": [{"$ref": "#/components/schemas/Request"}],
                    "example": example_for_request_schema,
                }
            }
        },
    }

    schemas = docs["components"]["schemas"]
    assert set(schemas) == {"MyNested", "Request", "Partial-Request", "Response"}
    assert schemas["MyNested"]["properties"] == {"i": {"type": "integer"}}
    assert schemas["Request"]["example"] == example_for_request_schema
    assert schemas["Request"]["properties"] == schemas["Partial-Request"]["properties"]
    assert schemas["Request"]["properties"]["nested_field"] == {
        "$ref": "#/components/schemas/MyNested"
    }
    assert schemas["Response"]["properties"]["msg"] == {"type": "string"}
    assert schemas["Response"]["properties"]["data"]["type"] == "object"


async def test_not_register_route_for_none_url():
    app = web.Application()
    routes_count = len(app.router.routes())
    setup_aiohttp_apispec(app=app, url=None)
    routes_count_after_setup_apispec = len(app.router.routes())
    assert routes_count == routes_count_after_setup_apispec


async def test_register_route_for_relative_url():
    app = web.Application()
    routes_count = len(app.router.routes())
    assert routes_count == 0
    setup_aiohttp_apispec(app=app, url="api/swagger")
    # new route should be registered according to AiohttpApispec.register() method?
    routes_count_after_setup_apispec = len(app.router.routes())
    # not sure why there was a comparison between the old rount_count vs new_route_count
    assert routes_count_after_setup_apispec == 1
