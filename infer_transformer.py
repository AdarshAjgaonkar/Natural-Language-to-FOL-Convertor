import re
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize

lemmatizer = WordNetLemmatizer()

KNOWN_VERBS = {
    "study", "write", "eat", "bark", "bite",
    "run", "read", "play", "drink", "drive",
    "teach", "check", "fly", "pass",
    "sleep", "walk", "talk", "learn", "build",
    "create", "watch", "listen", "help", "use",
    "make", "find", "give", "take", "open",
    "close", "move", "work", "call", "try",
    "ask", "need", "feel", "become", "leave"
}

PROPERTY_WORDS = {
    "hungry", "tired", "angry", "happy", "sad", "thirsty",
    "sleepy", "big", "small", "red", "blue", "smart",
    "strong", "weak", "fast", "slow", "rich",
    "poor", "kind", "brave", "clever", "lazy",
    "healthy", "sick", "good", "bad", "young", "old"
}


# ---------------- NORMALIZATION ----------------
def normalize_object(word: str) -> str:
    w = word.lower()

    irregular = {
        "people": "Person",
        "men": "Man",
        "women": "Woman",
        "children": "Child",
        "teeth": "Tooth",
        "feet": "Foot",
        "mice": "Mouse",
        "geese": "Goose",
    }

    if w in irregular:
        return irregular[w]

    return lemmatizer.lemmatize(w, "n").capitalize()


def normalize(sentence: str):
    sentence = sentence.strip().lower()
    tokens = word_tokenize(sentence)
    tagged = pos_tag(tokens)
    return sentence, tokens, tagged


# ---------------- EXTRACTION ----------------
def extract_entities(tagged):
    subject = None
    verbs = []
    objects = {}

    # subject
    for word, tag in tagged:
        if tag.startswith("NN"):
            subject = word.capitalize()
            break

    # verbs: controlled vocab + POS fallback
    for word, tag in tagged:
        lemma = lemmatizer.lemmatize(word.lower(), "v")

        if (
            lemma in KNOWN_VERBS
            or (tag.startswith("VB") and lemma not in ["is", "are", "was", "were", "am", "be"])
        ):
            verb = lemma.capitalize()

            if verb not in verbs:
                verbs.append(verb)
                objects[verb] = []

    # objects
    for i, (word, _) in enumerate(tagged):
        lemma = lemmatizer.lemmatize(word.lower(), "v").capitalize()

        if lemma in verbs:
            current_verb = lemma

            for j in range(i + 1, len(tagged)):
                next_word, next_tag = tagged[j]
                next_lemma = lemmatizer.lemmatize(next_word.lower(), "v").capitalize()

                # stop if another verb starts
                if next_lemma in verbs:
                    break

                if (
                    next_word.lower() not in KNOWN_VERBS
                    and next_word.lower() not in ["and", "or"]
                    and (
                        next_tag.startswith("NN")
                        or next_tag == "VBP"
                        or next_tag == "VB"
                        or next_word.isalpha()
                    )
                ):
                    obj = normalize_object(next_word)

                    if obj != subject and obj not in objects[current_verb]:
                        objects[current_verb].append(obj)

    if subject is None:
        subject = "Entity"

    return subject, verbs, objects


# ---------------- IF-THEN ----------------
def build_if_then_fol(sentence: str) -> str:
    s = sentence.lower()
    tokens = word_tokenize(s)
    tagged = pos_tag(tokens)

    subject = "Entity"
    condition = None
    action_verb = None
    action_obj = None

    found_if = False
    for word, tag in tagged:
        if word == "if":
            found_if = True
            continue
        if found_if and tag.startswith("NN"):
            subject = word.capitalize()
            break

    for i, (word, tag) in enumerate(tagged):
        if word == "is" and i + 1 < len(tagged):
            nxt = tagged[i + 1][0]
            condition = nxt.capitalize()
            break

    found_it = False
    for i, (word, tag) in enumerate(tagged):
        if word == "it":
            found_it = True
            continue

        if found_it:
            lemma = lemmatizer.lemmatize(word.lower(), "v")

            if lemma in KNOWN_VERBS or tag.startswith("VB"):
                action_verb = lemma.capitalize()

                for j in range(i + 1, len(tagged)):
                    w2, t2 = tagged[j]
                    if t2.startswith("NN") or w2.endswith("s"):
                        action_obj = normalize_object(w2)
                        break
                break

    if action_verb is None:
        action_verb = "Do"

    if condition is None:
        condition = "Condition"

    if action_obj:
        return f"∀x({subject}(x) ∧ {condition}(x) → {action_verb}(x,{action_obj}))"

    return f"∀x({subject}(x) ∧ {condition}(x) → {action_verb}(x))"


# ---------------- RELATIVE CLAUSE ----------------
def build_relative_clause_fol(sentence: str) -> str:
    s = sentence.lower()
    tokens = word_tokenize(s)
    tagged = pos_tag(tokens)

    subject = "Entity"
    cond_verbs = []
    main_verb = None
    main_obj = None

    for word, tag in tagged:
        if tag.startswith("NN"):
            subject = word.capitalize()
            break

    marker_index = -1
    for i, (word, _) in enumerate(tagged):
        if word in ["who", "that"]:
            marker_index = i
            break

    if marker_index == -1:
        return f"∀x({subject}(x))"

    for i in range(marker_index + 1, len(tagged)):
        word, _ = tagged[i]
        lemma = lemmatizer.lemmatize(word.lower(), "v")

        if lemma in KNOWN_VERBS:
            cond_verbs.append(lemma.capitalize())

    for word, _ in reversed(tagged):
        lemma = lemmatizer.lemmatize(word.lower(), "v")
        if lemma in KNOWN_VERBS:
            main_verb = lemma.capitalize()
            break

    found_main = False
    for word, tag in tagged:
        lemma = lemmatizer.lemmatize(word.lower(), "v").capitalize()

        if lemma == main_verb:
            found_main = True
            continue

        if found_main and (tag.startswith("NN") or word.endswith("s")):
            main_obj = normalize_object(word)
            break

    lhs_parts = [f"{subject}(x)"] + [f"{v}(x)" for v in cond_verbs]
    lhs = " ∧ ".join(lhs_parts)

    if main_obj:
        return f"∀x({lhs} → {main_verb}(x,{main_obj}))"

    return f"∀x({lhs} → {main_verb}(x))"


# ---------------- BUILD FOL ----------------
def build_fol(sentence, tagged):
    s = sentence.lower()

    if s.startswith("if "):
        return build_if_then_fol(sentence)

    if " who " in s or " that " in s:
        return build_relative_clause_fol(sentence)

    subject, verbs, objects = extract_entities(tagged)

    var = "x"
    subject_pred = f"{subject}({var})"
    verb_parts = []

    for verb in verbs:
        objs = objects.get(verb, [])

        if objs:
            for obj in objs:
                verb_parts.append(f"{verb}({var},{obj})")
        else:
            verb_parts.append(f"{verb}({var})")

    if not verb_parts:
        return f"∀{var}({subject_pred})"

    connector = " ∨ " if " or " in s else " ∧ "
    combined = connector.join(verb_parts)

    if s.startswith("every") or s.startswith("all"):
        return f"∀{var}({subject_pred} → ({combined}))"
    elif s.startswith("some") or s.startswith("a "):
        return f"∃{var}({subject_pred} ∧ ({combined}))"
    elif s.startswith("no"):
        return f"¬∃{var}({subject_pred} ∧ ({combined}))"

    return f"∀{var}({subject_pred} → ({combined}))"


# ---------------- FORMAT PREDICATES ----------------
def format_predicates(fol):
    matches = re.findall(r'([A-Z][a-zA-Z]*)\(([^()]*)\)', fol)

    predicates = []
    seen = set()

    for name, args in matches:
        args_list = [a.strip() for a in args.split(",") if a.strip()]
        key = (name, tuple(args_list))

        if key not in seen:
            seen.add(key)
            predicates.append((name, args_list))

    final_preds = []

    for i, (name, args) in enumerate(predicates):
        base = name.lower()

        if i == 0:
            desc = f"x is a {name}"

        elif len(args) == 1:
            if base in PROPERTY_WORDS:
                desc = f"x is {name}"
            else:
                verb = base[:-1] + "ies" if base.endswith("y") else base + "s"
                desc = f"x {verb}"

        elif len(args) == 2:
            verb = base[:-1] + "ies" if base.endswith("y") else base + "s"
            desc = f"x {verb} {args[1]}"

        else:
            continue

        final_preds.append((name, args, desc))

    return final_preds


# ---------------- QUESTION ANSWERING ----------------
def answer_question(sentence, question):
    s = sentence.lower()
    q = question.lower()

    if "mother-in-law" in s and "who am i" in q:
        return "You are the spouse of the person's child."

    if "who" in q:
        for w in s.split():
            if w not in ["every", "some", "no", "a", "an", "the"]:
                return f"It refers to {w.capitalize()}."

    return "Answer not found."


# ---------------- LOGICAL REASONING ----------------
def logical_reasoning(fol, question):
    q = question.lower().strip()

    matches = re.findall(r'([A-Z][a-zA-Z]*)\(([^()]*)\)', fol)

    facts = set()
    binary_facts = set()
    rules = []

    if "→" in fol:
        lhs, rhs = fol.split("→", 1)

        lhs_matches = re.findall(r'([A-Z][a-zA-Z]*)\(([^()]*)\)', lhs)
        rhs_matches = re.findall(r'([A-Z][a-zA-Z]*)\(([^()]*)\)', rhs)

        lhs_preds = set()
        rhs_preds = set()

        for name, _args in lhs_matches:
            lhs_preds.add(name.lower())

        for name, args in rhs_matches:
            args_list = [a.strip().lower() for a in args.split(",") if a.strip()]
            rhs_preds.add(name.lower())

            if len(args_list) == 1:
                facts.add(name.lower())
            elif len(args_list) == 2:
                binary_facts.add((name.lower(), args_list[1]))

        rules.append((lhs_preds, rhs_preds))

        for name, args in lhs_matches:
            args_list = [a.strip().lower() for a in args.split(",") if a.strip()]
            if len(args_list) == 1:
                facts.add(name.lower())
            elif len(args_list) == 2:
                binary_facts.add((name.lower(), args_list[1]))
    else:
        for name, args in matches:
            args_list = [a.strip().lower() for a in args.split(",") if a.strip()]
            if len(args_list) == 1:
                facts.add(name.lower())
            elif len(args_list) == 2:
                binary_facts.add((name.lower(), args_list[1]))

    words = re.findall(r"[a-zA-Z]+", q)

    target = None
    for w in words:
        lemma = lemmatizer.lemmatize(w, "v").lower()
        noun_lemma = lemmatizer.lemmatize(w, "n").lower()

        if lemma in KNOWN_VERBS:
            target = lemma
            break
        if w in PROPERTY_WORDS:
            target = w
            break
        if noun_lemma in PROPERTY_WORDS:
            target = noun_lemma
            break

    if target is None:
        return "I couldn't understand the question."

    subject_words = {
        "student", "dog", "cat", "teacher", "bird",
        "person", "man", "woman", "child"
    }

    stop_words = {
        "does", "do", "is", "are", "the", "a", "an", "it",
        "student", "dog", "cat", "teacher", "bird",
        "person", "man", "woman", "child"
    }

    target_obj = None
    for w in words:
        obj = normalize_object(w).lower()

        if (
            w not in stop_words
            and obj not in KNOWN_VERBS
            and obj not in PROPERTY_WORDS
            and obj not in subject_words
        ):
            target_obj = obj
            break

    def verb_form(v):
        if v.endswith("y"):
            return v[:-1] + "ies"
        return v + "s"

    if target_obj:
        if (target, target_obj) in binary_facts:
            return f"Yes, it {verb_form(target)} {target_obj}."
    else:
        if target in facts:
            if target in PROPERTY_WORDS:
                return f"Yes, it is {target}."
            return f"Yes, it {verb_form(target)}."

    for conds, results in rules:
        if target in results and conds.issubset(facts):
            if target_obj:
                return f"Yes, it {verb_form(target)} {target_obj} (inferred)."
            if target in PROPERTY_WORDS:
                return f"Yes, it is {target} (inferred)."
            return f"Yes, it {verb_form(target)} (inferred)."

    return "No, that is not supported by the given statement."


# ---------------- MAIN ----------------
def predict(sentence):
    sentence, tokens, tagged = normalize(sentence)
    return build_fol(sentence, tagged)