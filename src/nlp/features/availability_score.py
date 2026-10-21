AVAILABILITY_SCORES = {
    "AVAILABLE": 0.0,
    "DOUBTFUL": 0.75,
    "QUESTIONABLE": 0.5,
    "OUT": 1.0,
    "SUSPENDED": 1.0,
    "UNKNOWN": None
}

def get_availability_score(status):
    return AVAILABILITY_SCORES.get(status.upper())

