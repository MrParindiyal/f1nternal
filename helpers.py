import fastf1 as f1
from datetime import datetime

def get_params() -> tuple:
    year = datetime.now().year
    gp = int(input("Grand Prix week no. : "))

    decode = {
        "SQ" : "Sprint Qualifying",
        "Q"  : "Qualifying",
        "S"  : "Sprint",
        "R"  : "Race"
    }

    session_code = input("Session code        : ")
    session = decode.get(session_code, 'Q')
    return year, gp, session

