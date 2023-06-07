from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from models.Book import BookData, UserBook
from routers.api.auth import CurrentUserDep

router = APIRouter(prefix='/api/books')

@router.post('/{work_id}/{action}')
async def get_book(work_id, action, user: CurrentUserDep):
    try:
        if action not in ['wtr', 'rng', 'rd']:
            return {'error': 'Invalid action'}
        UserBook.upsert_user_book(user.username, work_id, action)
        return {'success': True, 'error': None}
    except Exception as e:
        print(e)
        return None