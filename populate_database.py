from datetime import datetime
from app import app
from models import setup_db, Movie, Actor

setup_db(app)
Sakka = Actor('Ahmed El Sakka', 48, 'M')
Mostafa = Actor('Mustafa Sha3ban', 51, 'M')
Mona = Actor('Mona Zaki', 44, 'F')
Mafia = Movie('Mafia', datetime.strptime('01 01 2000', '%d %m %Y').date())

Sakka.insert()
Mostafa.insert()
Mona.insert()
Mafia.insert()
Mafia.assign([Sakka, Mostafa, Mona])

Helmy = Actor('Ahmed Helmy', 51, 'M')
Ghada = Actor('Ghada Adel', 46, 'F')
Reham = Actor('Reham 3bd el 8afour', 43, 'F')
Mogrem = Movie('She turned me into a criminal', datetime.strptime('26 07 2006', '%d %m %Y').date())

Helmy.insert()
Ghada.insert()
Reham.insert()
Mogrem.insert()
Mogrem.assign([Helmy, Ghada, Reham])