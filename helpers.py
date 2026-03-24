from datetime import datetime, timezone
import fastf1 as f1
import pandas as pd


def get_params() -> tuple:
    year = datetime.now().year  # using current year for now by default
    try:
        gp = int(input("Grand Prix week no. : "))
        event_code = input("Session code        : ").upper()

    except Exception as e:  # gp might not be an int
        print(f"Failure: {e}")

    decode = {"SQ": "Sprint Qualifying", "Q": "Qualifying", "S": "Sprint", "R": "Race"}

    session = decode.get(event_code, "Qualifying")
    return year, gp, session


def last_complete_session(year: int, gp: int, event: str) -> tuple:
    """
    For now, we are assuming that user is trying to get sprint data from
    sprint events only.
    """

    year_schedule = f1.get_event_schedule(year, include_testing=False)
    remaining = f1.get_events_remaining()
    # event_format = year_schedule.query(f"RoundNumber == {gp}")["EventFormat"]
    gp = max(1, min(gp, remaining["RoundNumber"].iloc[-1]))  # clip round num
    session_num = year_schedule.iloc[gp-1][year_schedule.iloc[gp-1] == event].index[0]

    if year_schedule.iloc[0]["Session2Date"] > datetime.now(timezone.utc):
        # season does not seem to have started. fallback to last year

        year -= 1
        year_schedule = f1.get_event_schedule(year)
        round = year_schedule["RoundNumber"].iloc[-1]
        event = year_schedule.iloc[round]["Session5"]

    elif year_schedule.iloc[gp-1][f"{session_num}Date"] > datetime.now(timezone.utc):
        # this session is in future, find last occured non-practice round

        for S in range(1,int(session_num[-1])):
            if year_schedule.iloc[gp-1][f"Session{S}Date"] > datetime.now(timezone.utc):
                last_valid_session = S - 1
                break
            
        if last_valid_session == 0 or year_schedule.iloc[gp-1][f"Session{last_valid_session}"].startswith("Practice"):
            # go to previous race
            event = "Race"
            round = remaining.iloc[0]["RoundNumber"] - 1
            if round < 1:
                year -= 1
                round = f1.get_event_schedule(year)["RoundNumber"].iloc[-1]
                    
        else:
            event = year_schedule.iloc[gp-1][f"Session{last_valid_session}"]
            round = gp

    else:
        # weekend has occured this year
        # thus, year, gp and event are valid
        round = gp

    return year, int(round), event

