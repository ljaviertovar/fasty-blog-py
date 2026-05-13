from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

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

@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", {"title": "Home", "posts": posts})


@app.get("/posts/{post_id}", include_in_schema=False, name="post_detail")
def post_detail(request: Request, post_id: int):
    post = next((post for post in posts if post["id"] == post_id), None)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return templates.TemplateResponse(request, "post.html", {"title": post["title"][:50], "post": post})


# API endpoints
@app.get("/api/posts")
def get_posts():
    return {"posts": posts}

@app.get("/api/posts/{post_id}")
def get_post(post_id: int):
    post = next((post for post in posts if post["id"] == post_id), None)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"post": post}


# Custom error handlers
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )