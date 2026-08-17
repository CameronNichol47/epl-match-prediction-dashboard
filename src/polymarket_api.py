import json
import requests


def fetch_polymarket_probabilities(slug: str):
    url = f"https://gamma-api.polymarket.com/events/slug/{slug}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        event = response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching event: {e}")
        return None

    if not event:
        return None

    markets = event.get("markets", [])

    if not markets:
        return None

    probabilities = []

    for market in markets:

        raw_outcomes = market.get("outcomes", "[]")
        outcomes = (
            json.loads(raw_outcomes)
            if isinstance(raw_outcomes, str)
            else raw_outcomes
        )

        raw_prices = market.get("outcomePrices", "[]")
        prices = (
            json.loads(raw_prices)
            if isinstance(raw_prices, str)
            else raw_prices
        )

        for outcome, price_str in zip(outcomes, prices):

            if outcome != "Yes":
                continue

            try:
                probabilities.append(float(price_str))

            except ValueError:
                continue

    return probabilities

def load_slug(home, away, date):
    name = {"Manchester City": "mac",
            "Bournemouth": "bou",
            "Arsenal": "ars",
            "Coventry City": "cov",
            "Hull City": "hul",
            "Manchester Ußnited": "mun",
            "Everton": "eve",
            "Crystal Palace": "cry",
            "Ipswich Town": "ips",
            "Sundeland": "sun",
            "Nottingham Forest": "not",
            "Leeds United": "lee",
            "Brentford": "bre",
            "Tottenham Hotspur": "tot",
            "Brighton and Hove Albion": "bri",
            "Aston Villa": "ast",
            "Newcastle United": "new",
            "Liverpool": "liv",
            "Fulham": "ful",
            "Chelsea": "che"
            }
    
    home = name.get(home, home)
    away = name.get(away, away)

    slug = f"epl-{home}-{away}-{date}"
    print(slug)
    return fetch_polymarket_probabilities(slug)