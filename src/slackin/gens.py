import random

def losuj_imie():
    imiona = [
        'Jan',
        'Anita',
        'Marek',
        'Ola',
        "Andrzej"

    ]
    return imiona[random.randint(0,len(imiona)-1)]

def losuj_nazwisko():
    nazwiska =[
        'Kowalski',
        'Skrzyniarski',
        "Adwokat",
        "Kowalczyk",
        'Literacki'
    ]
    return nazwiska[random.randint(0,len(nazwiska)-1)]

def get_users(maxzad):
    users = []
    for u in range(random.randint(5,10)):
        users.append(
            {
                'imie': losuj_imie(),
                'nazwisko': losuj_nazwisko(),
                'zadania': random.randint(1,maxzad)
            }
        )
    print("wyg tyle:", len(users))
    return users

