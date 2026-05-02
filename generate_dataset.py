import random

def load_list(file):
    with open(file, "r") as f:
        return [line.strip() for line in f if line.strip()]

subjects = load_list("data/subjects.txt")
verbs_transitive = load_list("data/verbs_transitive.txt")
verbs_intransitive = load_list("data/verbs_intransitive.txt")
objects = load_list("data/objects.txt")
conditions = load_list("data/conditions.txt")


def generate(num_samples=3000):

    lines = []

    for i in range(num_samples):

        s = random.choice(subjects)

        # 🔥 balanced pattern
        choice = i % 5

        is_transitive = random.random() < 0.5

        if is_transitive:
            v = random.choice(verbs_transitive)
            o = random.choice(objects)
        else:
            v = random.choice(verbs_intransitive)

        # ---------- UNIVERSAL ----------
        if choice == 0:

            if is_transitive:
                sentence = f"Every {s.lower()} {v.lower()}s {o.lower()}"
                fol = f"∀x ({s}(x) → {v}(x,{o}))"
            else:
                sentence = f"Every {s.lower()} {v.lower()}s"
                fol = f"∀x ({s}(x) → {v}(x))"

        # ---------- EXISTENTIAL ----------
        elif choice == 1:

            if is_transitive:
                sentence = f"Some {s.lower()}s {v.lower()} {o.lower()}"
                fol = f"∃x ({s}(x) ∧ {v}(x,{o}))"
            else:
                sentence = f"Some {s.lower()}s {v.lower()}"
                fol = f"∃x ({s}(x) ∧ {v}(x))"

        # ---------- CONDITIONAL ----------
        elif choice == 2:

            c = random.choice(conditions)

            if is_transitive:
                sentence = f"If a {s.lower()} is {c.lower()} it {v.lower()}s {o.lower()}"
                fol = f"∀x ({s}(x) ∧ {c}(x) → {v}(x,{o}))"
            else:
                sentence = f"If a {s.lower()} is {c.lower()} it {v.lower()}s"
                fol = f"∀x ({s}(x) ∧ {c}(x) → {v}(x))"

        # ---------- NESTED ----------
        elif choice == 3:

            s2 = random.choice(subjects)
            sentence = f"Every {s.lower()} loves a {s2.lower()}"
            fol = f"∀x ({s}(x) → ∃y ({s2}(y) ∧ Love(x,y)))"

        # ---------- MULTI ----------
        else:

            v2 = random.choice(verbs_intransitive)

            if is_transitive:
                sentence = f"Every {s.lower()} {v.lower()}s {o.lower()} and {v2.lower()}s"
                fol = f"∀x ({s}(x) → {v}(x,{o}) ∧ {v2}(x))"
            else:
                sentence = f"Every {s.lower()} {v.lower()}s and {v2.lower()}s"
                fol = f"∀x ({s}(x) → {v}(x) ∧ {v2}(x))"

        lines.append(f"{sentence}\t{fol}")

    return lines


if __name__ == "__main__":

    data = generate(3000)

    with open("dataset.txt", "w", encoding="utf-8") as f:
        for line in data:
            f.write(line + "\n")

    print("✅ Dataset generated")