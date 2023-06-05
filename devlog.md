**03-06-23**
- fixed bugs in fetching book by id
- need to fix circular dependency in models

**04-06-23**
- fixed circular dependency bug
- moved `get_books` to `UserBook` class
- added `constants.py`
- made `Database` a singleton class

**05-06-23**
- fixed singleton errors
- tested `/books/{work_id}`, working
- added `upsert_user_book` to `UserBook` class
- **todos:**
    - add buttons to set book action
    - add books list on home page
    - Read up on Jinja templating and improve html