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

**06-06-23**
- added dummy buttons on `/books/{work_id}`
- added basic javascript code

**07-06-23**
- implemented working book action buttons
- organised html with Jinja layouts
- added bulma css

**todos:**
  - add books list on home page
  - make it look decent