from datetime import datetime, timezone
import fastf1 as f1
import pandas as pd


def get_params() -> tuple:
    year = datetime.now().year
    try:
        gp = int(input("Grand Prix week no. : "))
        event_code = input("Session code        : ").upper()

    except Exception as e:
        print(f"Failure: {e}")

    decode = {"SQ": "Sprint Qualifying", "Q": "Qualifying", "S": "Sprint", "R": "Race"}

    session = decode.get(event_code, "Qualifying")
    return year, gp, session


def latest_occured_weekend(year: int, gp: int, event: str) -> tuple:
    year_schedule = f1.get_event_schedule(year)
    session_num = year_schedule[:].iloc[gp][year_schedule[:].iloc[gp] == event].index(0)
    if year_schedule["EventDate"][0] > datetime.now(timezone.utc):
        # season does not seem to have started. fallback to last year
        year -= 1
        year_schedule = f1.get_event_schedule(year)
        round = year_schedule["RoundNumber"].iloc[-1]
        event = year_schedule[:].iloc[round]["Session5"]

    elif year_schedule[:].iloc[gp][f"{session_num}Date"] > datetime.now(timezone.utc):
        # this weekend is in future, find last occured non-practice round

        # TODO : handle fallback
        pass

    else:
        # weekend has occured this year
        # thus, year, gp and event are valid
        round = gp

    return year, round, event
