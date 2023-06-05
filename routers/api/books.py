from fastapi import APIRouter

from models.Book import BookData

router = APIRouter(prefix='/books')

@router.get('/{work_id}')
async def get_book(work_id):
    book = BookData.from_work_id(work_id)
    return book.__dict__ if book else None