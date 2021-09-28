from datetime import datetime
from api import app
from models import setup_db, Movie, Actor


# Mafia movie and its actors
Sakka = Actor('Ahmed El Sakka', 48, 'M')
Mostafa = Actor('Mustafa Sha3ban', 51, 'M')
Mona = Actor('Mona Zaki', 44, 'F')
Mafia = Movie('Mafia', datetime.strptime('01 01 2000', '%d %m %Y').date())

# ga3alatny mogreman movie with its actors
Helmy = Actor('Ahmed Helmy', 51, 'M')
Ghada = Actor('Ghada Adel', 46, 'F')
Reham = Actor('Reham 3bd el 8afour', 43, 'F')
Mogrem = Movie('She turned me into a criminal',
               datetime.strptime('26 07 2006', '%d %m %Y').date())


def init_database(args):
    # setup the database
    setup_db(**args)


def insert_all():
    '''
    insert all the above data into the database
    '''
    print('adding test data ...')
    Sakka.insert()
    Mostafa.insert()
    Mona.insert()
    Mafia.insert()
    Mafia.assign([Sakka, Mostafa, Mona])
    Helmy.insert()
    Ghada.insert()
    Reham.insert()
    Mogrem.insert()
    Mogrem.assign([Helmy, Ghada, Reham])


if __name__ == '__main__':
    init_database({'app': app})
    insert_all()
