import json
import requests


def fetch_polymarket_probabilities(slug, home, away):
    url = f"https://gamma-api.polymarket.com/events/slug/{slug}"

    headers = {
        "User-Agent": "Mozilla/5.0"
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

    home_prob = None
    draw_prob = None
    away_prob = None

    for market in markets:

        # Useful fields for figuring out what this market represents
        question = (market.get("question") or "").lower()
        title = (market.get("groupItemTitle") or "").lower()

        market_text = f"{question} {title}"

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

        # Find the YES probability for this market
        yes_price = None

        for outcome, price in zip(outcomes, prices):
            if outcome.lower() == "yes":
                yes_price = float(price)
                break

        if yes_price is None:
            continue

        # Determine what outcome this market represents
        if "draw" in market_text:
            draw_prob = yes_price

        elif home.lower() in market_text:
            home_prob = yes_price

        elif away.lower() in market_text:
            away_prob = yes_price

    print("HOME:", home_prob)
    print("DRAW:", draw_prob)
    print("AWAY:", away_prob)

    if (
        home_prob is None
        or draw_prob is None
        or away_prob is None
    ):
        return None

    return [away_prob, draw_prob, home_prob]

def load_slug(home, away, date):

    original_home = home
    original_away = away

    name = {
        "Manchester City": "mac",
        "Bournemouth": "bou",
        "Arsenal": "ars",
        "Coventry City": "cov",
        "Hull City": "hul",
        "Manchester United": "mun",
        "Everton": "eve",
        "Crystal Palace": "cry",
        "Ipswich Town": "ips",
        "Sunderland": "sun",
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

    home_slug = name.get(home, home)
    away_slug = name.get(away, away)

    slug = f"epl-{home_slug}-{away_slug}-{date}"

    return fetch_polymarket_probabilities(
        slug,
        original_home,
        original_away
    )