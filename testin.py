from faker  import Faker

fkr=Faker()

def create_random(num:int):
    ''' add ramdon products '''
    for _ in range(num):

        print(fkr.pystr_format(), 
              fkr.pyfloat(min_value=100, max_value=900, right_digits=2),
              fkr.pyint(max_value=100))

create_random(5)