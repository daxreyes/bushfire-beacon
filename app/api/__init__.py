from fastapi import APIRouter
from app.api.v1 import login, users, items
from app import utils


from typing import Any, Callable

from fastapi import APIRouter as FastAPIRouter

# https://github.com/tiangolo/fastapi/issues/2060#issuecomment-834868906
# from fastapi.types import DecoratedCallable
# How to Prevent the 307 Temporary Redirect When There's a Missing Trailing Slash
# class APIRouter(FastAPIRouter):
#     def api_route(
#         self, path: str, *, include_in_schema: bool = True, **kwargs: Any
#     ) -> Callable[[DecoratedCallable], DecoratedCallable]:
#         if path.endswith("/"):
#             path = path[:-1]

#         add_path = super().api_route(path, include_in_schema=include_in_schema, **kwargs)

#         alternate_path = path + "/"
#         add_alternate_path = super().api_route(alternate_path, include_in_schema=False, **kwargs)

#         def decorator(func: DecoratedCallable) -> DecoratedCallable:
#             add_alternate_path(func)
#             return add_path(func)

#         return decorator


api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
