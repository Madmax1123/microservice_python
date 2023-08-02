"""

"""

from yoyo import step

__depends__ = {}

steps = [
    step("CREATE TABLE user (id SERIAL PRIMARY KEY, nome VARCHAR(100) NOT NULL, email VARCHAR(100) UNIQUE NOT NULL, senha VARCHAR(50) NOT NULL")
]
