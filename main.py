from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

users = [
    {"id": 1,
     "username": "Fenix",
     "first_name": "Sardor",
     "last_name": "Safaraliyev",
     "job_title": "Programmer",
     "location": "Tashkent",
     "email": "hello@gmail.com",
     "phone_number": "990708605",
     "birthday": "05/07/2005"
     },
    {"id": 2,
     "username": "Pendi",
     "first_name": "Diyor",
     "last_name": "Turgunboyev",
     "job_title": "Trader",
     "location": "Tashkent",
     "email": "tatata@gmail.com",
     "phone_number": "943644401",
     "birthday": "03/08/2005"
     },
    {"id": 3,
     "username": "Shustr",
     "first_name": "Otabek",
     "last_name": "Rahimberdiyev",
     "job_title": "Businessman",
     "location": "Tashkent",
     "email": "momomo@gmail.com",
     "phone_number": "971290904",
     "birthday": "23/01/2006"
     }

]


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    context = {
        "users": users
    }
    return templates.TemplateResponse(request, 'user-list.html', context)


@app.get("/user/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: int):
    _user = None
    for user in users:
        if user['id'] == id:
            _user = user

    context = {
        'user': _user
    }

    return templates.TemplateResponse(request, 'user-detail.html', context)
