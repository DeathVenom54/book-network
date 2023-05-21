## Planned Page structure

HTML Routes:
```
/login
/signup
/home:      currently reading
            friends reading
            past books (add a review)
            recommended books based on author and genre
    /home/my-books:    currently reading and past books
    
/friends:   add and manage friends
    /friends/add:   add a new friend
    /friend/$id:    detailed friend view
/books:     search and browse books
    /books/$id: detailed book view
```

API Routes:
```
/api
    /auth
        /login
        /signup
    /books
        /$id
        /recommend
```