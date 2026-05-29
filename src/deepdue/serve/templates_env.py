import json
import markdown as md
from pathlib import Path
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")

templates.env.filters["tojson"] = json.dumps
templates.env.filters["markdown"] = lambda text: md.markdown(text, extensions=["nl2br"])