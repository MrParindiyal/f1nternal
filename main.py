import fastf1 as f1
from helpers import get_args, last_complete_session
import pandas as pd

def main() -> None:
    args = get_args()
    last_session = last_complete_session(*args)
    session = f1.get_session(*last_session)
    session._load_drivers_results()

    results = session.results[["Abbreviation", "Position"]]
    results_dict = {results.iloc[n].iloc[0] : n + 1 for n in range(len(results))}
    
    pred = pd.read_csv("predictions.csv")
    
    predictors = pred.columns[1:] # 1st col is Name/Position
    last = len(pred)
    pred.at[last, pred.columns[0]] = "Total"
    total_drivers = len(results["Abbreviation"])# .iloc[-1] could be None

    for player in predictors:
        sum = 0
        for i in range(len(results)):
            delta = abs(results_dict.get(pred[player][i], -999) - (i+1))
            sum += (total_drivers - delta) if delta < 24 else 0
        
        pred.at[last, player] = int(sum)
    
    pred.to_csv("results.csv", index=False)

    return

if __name__ == "__main__":
    main()