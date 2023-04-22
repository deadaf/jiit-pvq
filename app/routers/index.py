from fastapi import APIRouter, Request, Query
from fastapi.templating import Jinja2Templates
import json
import re
import os

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

    with open("app/static/data/subjects.json") as f:
        data = json.loads(f.read())
        return data[dept.upper()][year.upper()][sem.upper()]


@router.get("/get-files")
async def get_files(dept: str, year: str, sem: str, exam: str, subject: str):
    # [q/a]year-dept-clgyr-sem-t-sub.ext

    pattern = re.compile(
        r"^q-\d{4}-dept-year-sem-exam-sub\.pdf$".replace("dept", dept.upper())
        .replace("year", year.upper())
        .replace("sem", sem.upper())
        .replace("sub", subject.upper().replace(" ", "_"))
        .replace("exam", exam.upper())
    )

    matching_files = []
    for filename in os.listdir("app/resources"):
        print(filename)
        if pattern.match(filename):
            matching_files.append(filename)

    return matching_files
