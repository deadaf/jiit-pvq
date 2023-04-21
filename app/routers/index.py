from fastapi import APIRouter, Request, Query
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def hello_sexy(request: Request):
    # Render the homepage template with the contents of the data directory
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/subjects")
async def get_subjects(
    dept: str = Query(...), year: str = Query(...), sem: str = Query(...)
):
    # get list of subjects for the selected department and semester
    return ["DBMS", "ABCD"]
