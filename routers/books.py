from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from models.Book import BookData

router = APIRouter(prefix='/api/books')
templates = Jinja2Templates(directory='templates')


@router.get('/{work_id}')
async def get_book(work_id, req: Request):
    book = BookData.from_work_id(work_id)
    return templates.TemplateResponse('login.html', {'request': req, 'book': book.__dict__})
