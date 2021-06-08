import os
from dotenv import dotenv_values

config = {
    **dotenv_values(os.path.join(os.path.dirname(__file__), '..', '.env')),
    **os.environ,
}

if __name__ == '__main__':
    print(config)
