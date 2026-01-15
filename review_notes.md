## Nazewnictwo 
ListUsersQuery(user_repo(db)).run(limit, offset, email_like) - Kazda ta klasa ma funkcje run(). Metody sa ok ale 
jesli chodzi o nazwy lepiej dawac cos bardziej opisowego w stylu get_users() to jest bardziej DDD/CQRS

## Czystośc kodu 

dodalem ci taka metode  zeby nie duplikowac tego co  w return    

@classmethod
    def from_entity(cls, user):
        return cls(id=user.id, email=user.email, name=user.name)

## Logika i działanie 
Transakcje nie do konca spełniały reguły ACID. To znaczy mialas komit na baze nawet jesli lecial wyjatek. Czy ktos
dodaje usera leci 500 uzytkownik mysli ze sie nie dodalo ale w bazie cos zostalo zapisane bo commit(). dlatego potrzebne 
jest rolowanie transakcji jesli cos jest nie tak wtedy baza ma spojne dane. 
Tu numer commita gdzi mozesz zobaczyc szczegolowe zmiany: [Commit: 13f3078]
