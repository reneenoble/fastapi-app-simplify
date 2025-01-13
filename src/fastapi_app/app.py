import sys, os
import pathlib
from typing import Annotated
import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()
parent_path = pathlib.Path(__file__).parent.parent
app.mount("/mount", StaticFiles(directory=parent_path / "static"), name="static")
templates = Jinja2Templates(directory=parent_path / "templates")
templates.env.globals["prod"] = os.environ.get("RUNNING_IN_PRODUCTION", False)
# Use relative path for url_for, so that it works behind a proxy like Codespaces
templates.env.globals["url_for"] = app.url_path_for


@app.get("/", response_class=PlainTextResponse)
def index(request: Request):
    version = sys.version_info
    return PlainTextResponse(content=f"Hello World, I am Python {version.major}.{version.minor}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)