## Planned Page structure

HTML Routes:
```
/login
/signup
/update:    update username, bio, password
/:          currently reading books, wishlist and friends updates (preview)
            recommended books based on author and genre (preview)
/my-books:    currently reading, wishlist and past books
    
/friends:   add and manage friends
            see friend updates (started new book, finished reading, etc)
    /friend/$id:    detailed friend view
/books:     search and browse books (algorithm will recommend books for you)
    /books/$id: detailed book view
```

API Routes:
```
/api
    /auth
        /login
        /signup
```

[Palette](https://colorhunt.co/palette/025464e57c23e8aa42f8f1f1)
