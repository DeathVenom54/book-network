from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from models.Book import BookData, UserBook, search_books
from routers.api.auth import CurrentUserDep

router = APIRouter(prefix='/books')
templates = Jinja2Templates(directory='templates')

@router.get('/search')
async def get_book(req: Request, user: CurrentUserDep, q: str = ''):
    books = search_books(q)
    return templates.TemplateResponse('book_search.html', {'request': req, 'query': q, 'books': books})

@router.get('/{work_id}')
async def get_book(work_id, req: Request, user: CurrentUserDep):
    book = BookData.from_work_id(work_id)
    user_book = UserBook.get_books_for_user(user.username, work_id)
    if user_book:
        return templates.TemplateResponse('book_details.html', {'request': req, 'book': book.__dict__, 'user_book': user_book.to_dict()})
    else:
        return templates.TemplateResponse('book_details.html', {'request': req, 'book': book.__dict__, 'user_book': None})
