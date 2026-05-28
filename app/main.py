from pathlib import Path

from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import SessionLocal, engine, Base, DATABASE_URL
from . import crud, config

from app.config import APP_VERSION

from fastapi.middleware.trustedhost import TrustedHostMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

templates.env.globals["APP_VERSION"] = APP_VERSION

# Dependency


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    ads = crud.get_ads(db)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "ads": ads,
            "app_env": config.APP_ENV,
            "app_host": config.APP_HOST,
            "app_port": config.APP_PORT,
            "debug": config.DEBUG,
            "database_type": config.DATABASE_TYPE,
            "database_host": config.DATABASE_HOST,
            "database_port": config.DATABASE_PORT,
            "database_name": config.DATABASE_NAME,
            "database_user": config.DATABASE_USER,
            "database_password": config.DATABASE_PASSWORD,
            "database_path": config.DATABASE_PATH,
            "database_url": DATABASE_URL,
        },
    )


@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={
            "request": request,
            "app_env": config.APP_ENV,
            "app_host": config.APP_HOST,
            "app_port": config.APP_PORT,
            "debug": config.DEBUG,
            "database_type": config.DATABASE_TYPE,
            "database_host": config.DATABASE_HOST,
            "database_port": config.DATABASE_PORT,
            "database_name": config.DATABASE_NAME,
            "database_user": config.DATABASE_USER,
            "database_password": config.DATABASE_PASSWORD,
            "database_path": config.DATABASE_PATH,
            "database_url": DATABASE_URL,
        },
    )


@app.get("/create", response_class=HTMLResponse)
def create_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="create.html",
        context={
            "request": request,
        },
    )


@app.post("/create")
def create_ad(
    title: str = Form(...),
    description: str = Form(...),
    price: str = Form(...),
    db: Session = Depends(get_db),
):
    crud.create_ad(db, title, description, price)

    return RedirectResponse(url="/", status_code=303)


@app.get("/edit/{ad_id}", response_class=HTMLResponse)
def edit_page(
    ad_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    ad = crud.get_ad(db, ad_id)

    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={
            "request": request,
            "ad": ad,
        },
    )


@app.post("/edit/{ad_id}")
def edit_ad(
    ad_id: int,
    title: str = Form(...),
    description: str = Form(...),
    price: str = Form(...),
    db: Session = Depends(get_db),
):
    crud.update_ad(db, ad_id, title, description, price)

    return RedirectResponse(url="/", status_code=303)


@app.get("/delete/{ad_id}")
def delete_ad(
    ad_id: int,
    db: Session = Depends(get_db),
):
    crud.delete_ad(db, ad_id)

    return RedirectResponse(url="/", status_code=303)


@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)

    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=()"

    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains; preload"
    )

    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "img-src 'self' data:; "
        "style-src 'self' 'unsafe-inline'; "
        "script-src 'self' 'unsafe-inline'"
    )

    return response
