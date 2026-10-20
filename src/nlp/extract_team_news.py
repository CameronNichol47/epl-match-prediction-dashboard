import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
from ddgs.exceptions import DDGSException
from datetime import datetime, timedelta
from extract_names import analyze_player_availability

def get_article_date(soup):

    # First try the publication metadata
    published = soup.find("meta", property="article:published_time")

    if published is not None:
        article_date = published.get("content")

    else:
        # Fallback to a time element
        published = soup.find("time")

        if published is None:
            return None

        article_date = published.get("datetime")

    if article_date is None:
        return None

    try:
        return datetime.fromisoformat(
            article_date.replace("Z", "+00:00")
        ).date()

    except ValueError:
        return None


def get_bbc_url(team, opponent, match_date):

    date = datetime.strptime(match_date, "%Y-%m-%d").date()
    start_date = date - timedelta(days=3)

    queries = [
        f"BBC Sport {team} {opponent} team news {date.strftime('%B %Y')}",
        f"BBC Sport {team} injury news {date.strftime('%B %Y')}",
        f"BBC Sport {team} press conference injuries {date.strftime('%B %Y')}"
    ]

    for query in queries:

        print("\nSearching:", query)

        try:
            results = DDGS().text(query, max_results=10)

        except DDGSException as e:
            print("Search failed:", e)
            continue

        for result in results:

            url = result["href"]

            # Only accept BBC Sport football articles
            if "/sport/football/articles/" not in url:
                continue

            if not (
                "bbc.com/sport/" in url
                or "bbc.co.uk/sport/" in url
            ):
                continue

            print("\nCandidate:", result["title"])
            print("URL:", url)

            try:
                response = requests.get(
                    url,
                    headers={"User-Agent": "MySoccerResearch/1.0"},
                    timeout=15
                )

                if response.status_code != 200:
                    print("HTTP status:", response.status_code)
                    continue

            except requests.RequestException as e:
                print("Request failed:", e)
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            article_date = get_article_date(soup)

            if article_date is None:
                print("Publication date not found")
                continue

            print("Article date:", article_date)
            print("Match date:", date)

            if start_date <= article_date <= date:
                print("Date matched!")
                return url

            else:
                print("Article outside date range")

    return None


def get_team_news(url):

    if url is None:
        return None

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "MySoccerResearch/1.0"},
            timeout=15
        )

        response.raise_for_status()

    except requests.RequestException as e:
        print("Could not retrieve article:", e)
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    article = soup.find("article")

    if article is None:
        print("Article element not found")
        return None

    paragraphs = []

    for p in article.find_all(["p", "li"]):

        sentence = p.get_text(" ", strip=True)

        if sentence:
            paragraphs.append(sentence)

    return paragraphs


# -------------------------------
# MAIN
# -------------------------------

team = "Tottenham"
opponent = "Coventry City"
match_date = "2026-10-19"

url = get_bbc_url(team, opponent, match_date)

print("\nArticle URL:", url)

p = ""

if url:
    team_news = get_team_news(url)

    if team_news:
        print("\n--- TEAM NEWS ---\n")

        for paragraph in team_news:
            p += paragraph + " "

        print(p)

        results = analyze_player_availability(p)

        for result in results:
            print(result)

    else:
        print("No team news found in the article.")

else:
    print("No matching BBC Sport article found.")