from transformers import pipeline
ner = pipeline(
    "ner",
    model="dslim/bert-base-NER",
    aggregation_strategy="max",
    device="mps"
    )

qa = pipeline(
    "question-answering",
    model="deepset/roberta-base-squad2",
    device="mps"
)

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device="mps"
)

status_labels = [
    "OUT",
    "DOUBTFUL",
    "QUESTIONABLE",
    "LIKELY_AVAILABLE",
    "AVAILABLE"
]

hyphenated_players = [
    "Morgan Gibbs-White",
    "Callum Hudson-Odoi",
    "Aaron Wan-Bissaka",
    "James Ward-Prowse",
    "Dominic Calvert-Lewin",
    "Kiernan Dewsbury-Hall",
    "Rayan Ait-Nouri",
    "Keane Lewis-Potter",
    "Kyle Walker-Peters",
    "Bobby De Cordova-Reid",
    "Taylor Harwood-Bellis",
    "Armel Bella-Kotchap",
    "Kaine Kesler-Hayden",
    "Myles Peart-Harris",
    "Amario Cozier-Duberry",
    "Benicio Baker-Boaitey",
    "Sam Amo-Ameyaw"
]

managers = [
    "Xabi Alonso",
    "Keith Andrews",
    "Álvaro Arbeloa",
    "Mikel Arteta",
    "Michael Carrick",
    "Roberto De Zerbi",
    "Unai Emery",
    "Daniel Farke",
    "Oliver Glasner",
    "Fabian Hürzeler",
    "Andoni Iraola",
    "Matthias Jaissle",
    "Sergej Jakirović",
    "Frank Lampard",
    "Régis Le Bris",
    "Enzo Maresca",
    "David Moyes",
    "Gary O'Neil",
    "Marco Rose",
    "Pierre Sage",
    "Alonso",
    "Andrews",
    "Arbeloa",
    "Arteta",
    "Carrick",
    "De Zerbi",
    "Emery",
    "Farke",
    "Glasner",
    "Hürzeler",
    "Iraola",
    "Jaissle",
    "Jakirović",
    "Lampard",
    "Le Bris",
    "Maresca",
    "Moyes",
    "O'Neil",
    "Rose",
    "Sage"
]

def correct_player_names(names, text):
    corrected = []

    for name in names:
        full_name = name

        for player in hyphenated_players:
            if player.lower() in text.lower():
                parts = player.replace("-", " ").split()

                if name.lower() == player.lower():
                    full_name = player
                    break

                if name.lower() in [part.lower() for part in parts]:
                    full_name = player
                    break

                if name.lower() in player.lower():
                    full_name = player
                    break

        if full_name not in corrected:
            corrected.append(full_name)

    return corrected

def is_relevant_player(name, context):
    context_lower = context.lower()
    name_lower = name.lower()

    if "in place of " + name_lower in context_lower:
        return False

    if name_lower + " gets a start" in context_lower:
        return False

    keywords = [
        "injury",
        "injured",
        "suspension",
        "suspended",
        "ineligible",
        "doubtful",
        "ruled out",
        "unavailable",
        "returned from injury",
        "back in the starting line-up",
        "back on the bench"
    ]

    return any(keyword in context_lower for keyword in keywords)

def filter_injury_news(text):
    keywords = [
        "injury", "injured", "fitness", "hamstring",
        "ankle", "knee", "thigh", "muscle",
        "suspended", "suspension", "banned",
        "doubt", "doubtful",
        "ruled out", "will miss", "will not feature",
        "unavailable", "sidelined",
        "return", "returning", "back in training",
        "recovered", "fit again"
    ]

    sentences = text.replace("\n", " ").split(". ")

    relevant = []

    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in keywords):
            relevant.append(sentence)

    return ". ".join(relevant)

def classify_player(name, context):
    context_lower = context.lower()

    # 1. Confirmed available or returning
    available_phrases = [
        "returned from injury",
        "back on the bench",
        "back in the starting line-up",
        "back in the starting lineup",
        "comes into the starting xi",
        "returns to the starting xi",
        "returns to the squad",
        "available as substitutes",
        "available for selection",
        "back from suspension",
        "returned from suspension",
        "fit again",
        "back in training"
    ]

    # 2. Confirmed unavailable
    out_phrases = [
        "ruled out",
        "will not feature",
        "will miss the match",
        "will miss the game",
        "set to miss",
        "suspended for",
        "serving a suspension",
        "ineligible to face",
        "unavailable for"
    ]

    # 3. Doubtful
    doubtful_phrases = [
        "doubtful",
        "unlikely to feature",
        "unlikely to play",
        "fitness doubt",
        "major doubt"
    ]

    # 4. Questionable
    questionable_phrases = [
        "fitness test",
        "late fitness test",
        "could miss",
        "may miss",
        "uncertain whether",
        "questionable"
    ]



    if any(phrase in context_lower for phrase in out_phrases):
            return "OUT"
    
    if any(phrase in context_lower for phrase in available_phrases):
        return "AVAILABLE"

    if any(phrase in context_lower for phrase in doubtful_phrases):
        return "DOUBTFUL"

    if any(phrase in context_lower for phrase in questionable_phrases):
        return "QUESTIONABLE"


    hypotheses = {
        "OUT": f"{name} will not play in the upcoming match.",
        "DOUBTFUL": f"{name} is doubtful for the upcoming match.",
        "QUESTIONABLE": f"It is uncertain whether {name} will play.",
        "LIKELY_AVAILABLE": f"{name} is expected to be available for the match.",
        "AVAILABLE": f"{name} is confirmed fit and available."
    }

    scores = {}

    for status, hypothesis in hypotheses.items():
        result = classifier(
            context,
            candidate_labels=[hypothesis, "Something unrelated"],
            hypothesis_template="{}",
            multi_label=True
        )

        index = result["labels"].index(hypothesis)
        scores[status] = result["scores"][index]

    best_status = max(scores, key=scores.get)

   
    if scores[best_status] < 0.65:
        return "UNKNOWN"

    return best_status

def extract_players(text):
    results = ner(text)

    name_corrections = {
        "Kiernan Dewsbury": "Kiernan Dewsbury-Hall",
        "Hall": "Kiernan Dewsbury-Hall"
    }

    names = []

    for result in results:
        if result["entity_group"] == "PER":
            name = result["word"]

            name = name_corrections.get(name, name)

            if name not in names and name not in managers:
                names.append(name)

    full_names = []

    for name in names:
        if not any(name != other and name in other for other in names):
            full_names.append(name)

    return full_names

def get_player_context(names, text):
    players = []

    sentences = text.replace("\n", " ").split(". ")

    separators = [
        ", while ",
        ", but ",
        " so ",
        " whereas ",
        "; "
    ]

    for name in names:
        matching = []

        for sentence in sentences:
            clauses = [sentence]

            
            for separator in separators:
                new_clauses = []

                for clause in clauses:
                    parts = clause.split(separator)
                    new_clauses.extend(parts)

                clauses = new_clauses

           
            for clause in clauses:
                if name.lower() in clause.lower():
                    matching.append(clause.strip())

        if matching:
            players.append({
                "name": name,
                "context": " ".join(matching)
            })

    return players

def get_injuries(name, text):
    result = qa(
        question=f"What is the injury or availability status of {name}?",
        context=text
    )

    return {
        "name": name,
        "sentence": result["answer"],
        "score": round(result["score"], 3)
    }


def analyze_player_availability(text):
    filtered_text = filter_injury_news(text)

    if not filtered_text:
        return []

    full_names = extract_players(filtered_text)
    full_names = correct_player_names(full_names, filtered_text)
    players = get_player_context(full_names, filtered_text)

    ans = []

    for player in players:
        name = player["name"]
        context = player["context"]

        if not is_relevant_player(name, context):
            continue

        injury = get_injuries(name, context)

        injury["status"] = classify_player(name, context)

        ans.append(injury)

    return ans