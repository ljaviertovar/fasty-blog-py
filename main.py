from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

posts: list[dict] = [
    {
        "id": 1,
        "author": "John Doe",
        "title": "First Post",
        "content": "This is the first post.",
        "date_posted": "April 1, 2023",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Second Post",
        "content": "This is the second post.",
        "date_posted": "April 2, 2023",
    },
    {
        "id": 3,
        "author": "Alice Smith",
        "title": "Third Post",
        "content": "This is the third post.",
        "date_posted": "April 3, 2023",
    },
]


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", include_in_schema=False)
@app.get("/posts", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", {"title": "Home", "posts": posts})


@app.get("/api/posts")
def get_posts():
    return {"posts": posts}