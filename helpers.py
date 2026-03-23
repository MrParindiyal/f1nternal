from datetime import datetime, timezone
import fastf1 as f1
import pandas as pd


def get_params() -> tuple:
    year = datetime.now().year # using current year for now by default 
    try:
        gp = int(input("Grand Prix week no. : "))
        event_code = input("Session code        : ").upper()

    except Exception as e: # gp might not be an int
        print(f"Failure: {e}")

    decode = {"SQ": "Sprint Qualifying", "Q": "Qualifying", "S": "Sprint", "R": "Race"}

    session = decode.get(event_code, "Qualifying")
    return year, gp, session


def latest_occured_weekend(year: int, gp: int, event: str) -> tuple:
    """
    For now, we are assuming that user is trying to get sprint data from
    sprint events only.
    """

    year_schedule = f1.get_event_schedule(year, include_testing=False)
    remaining = f1.get_events_remaining()
    event_format = year_schedule.query(f"RoundNumber == {gp}")["EventFormat"]
    session_num = year_schedule[:].iloc[gp][year_schedule[:].iloc[gp] == event].index(0)
    gp = max(1, min(gp, remaining["RoundNumber"].iloc[-1])) # clip round num   
    
    if year_schedule[:].iloc[0]["Session2Date"] > datetime.now(timezone.utc):
        # season does not seem to have started. fallback to last year

        year -= 1
        year_schedule = f1.get_event_schedule(year)
        round = year_schedule["RoundNumber"].iloc[-1]
        event = year_schedule[:].iloc[round]["Session5"]

    elif year_schedule[:].iloc[gp][f"{session_num}Date"] > datetime.now(timezone.utc):
        # this weekend is in future, find last occured non-practice round

        if datetime.now(timezone.utc) < remaining.iloc[0]["Session2Date"]:
            # this week's important stuff is yet to happen, 
            # falling to last event's race 
            event = "Race"
            round = gp - 1

            # TODO : can round < 1 be possible?
            # return

        if event_format == "sprint_qualifying":
            pass

        elif event_format == "conventional":
            pass

    else:
        # weekend has occured this year
        # thus, year, gp and event are valid
        round = gp

    return year, round, event
