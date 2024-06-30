import os

# Substitua 'NBA.db' pelo nome do seu banco de dados, se for diferente
db_name = 'NBA.db'
db_path = os.path.abspath(db_name)

print(f'O caminho absoluto do seu banco de dados é: {db_path}')
