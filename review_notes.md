## Nazewnictwo 
ListUsersQuery(user_repo(db)).run(limit, offset, email_like) - Kazda ta klasa ma funkcje run(). Metody sa ok ale 
jesli chodzi o nazwy lepiej dawac cos bardziej opisowego w stylu get_users() to jest bardziej DDD/CQRS

## Czystoś kodu 

dodalem ci taka metode  zeby nie duplikowac tego co  w return    

@classmethod
    def from_entity(cls, user):
        return cls(id=user.id, email=user.email, name=user.name)
