# Natural Language to First-Order Logic (FOL) Converter with Reasoning

## 📌 Overview

The **Natural Language to First-Order Logic (FOL) Converter with Reasoning** is an AI-based application that converts English sentences into formal First-Order Logic representations using Natural Language Processing (NLP) techniques.

The system extracts subjects, verbs, objects, and properties from natural language, generates corresponding FOL expressions, formats predicates into human-readable descriptions, and performs basic logical reasoning on the generated knowledge.

This project demonstrates the integration of **Artificial Intelligence**, **Natural Language Processing**, and **Knowledge Representation** concepts in a practical application.

---

## 🎯 Features

### ✅ Natural Language Processing

* Sentence tokenization
* Part-of-Speech (POS) tagging
* Lemmatization
* Entity extraction

### ✅ First-Order Logic Generation

* Universal Quantifiers (∀)
* Existential Quantifiers (∃)
* Negation (¬)
* Conjunction (∧)
* Disjunction (∨)
* Implication (→)

### ✅ Predicate Generation

Converts logical predicates into readable descriptions.

Example:

```text
Student(x)
→ x is a Student

Write(x, Exam)
→ x writes Exam
```

### ✅ Logical Reasoning

Supports basic inference and query answering.

Example:

```text
Sentence:
Every student studies and writes exam

Question:
Does student study?

Answer:
Yes, it studies.
```

### ✅ Interactive GUI

* Modern Tkinter-based interface
* Real-time FOL generation
* Predicate visualization
* Logical query support

---

## 🏗️ System Architecture

```text
Input Sentence
       │
       ▼
NLP Processing
(Tokenization + POS Tagging)
       │
       ▼
Entity Extraction
(Subject, Verb, Object)
       │
       ▼
FOL Generator
       │
       ▼
Predicate Formatter
       │
       ▼
Reasoning Engine
       │
       ▼
Output Display
```

---

## 🛠️ Technology Stack

| Technology         | Purpose                     |
| ------------------ | --------------------------- |
| Python             | Core Programming Language   |
| NLTK               | Natural Language Processing |
| Tkinter            | GUI Development             |
| Regex              | Pattern Matching            |
| WordNet Lemmatizer | Word Normalization          |

---

## 📂 Project Structure

```text
fol_project/
│
├── app.py
├── infer_transformer.py
├── requirements.txt
├── README.md
│
├── screenshots/
│   ├── output1.png
│   ├── output2.png
│   └── output3.png
│
└── assets/
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/fol-converter.git
cd fol-converter
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Download NLTK Resources

```python
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
```

### Run Application

```bash
python app.py
```

---

## 🧪 Example Inputs and Outputs

### Example 1

**Input**

```text
Every student studies and writes exam
```

**Output**

```text
∀x(Student(x) → (Study(x) ∧ Write(x,Exam)))
```

Predicates:

```text
Student(x)
→ x is a Student

Study(x)
→ x studies

Write(x,Exam)
→ x writes Exam
```

---

### Example 2

**Input**

```text
Some student reads books
```

**Output**

```text
∃x(Student(x) ∧ Read(x,Book))
```

---

### Example 3

**Input**

```text
No student writes exam
```

**Output**

```text
¬∃x(Student(x) ∧ Write(x,Exam))
```

---

### Example 4

**Input**

```text
Every student is hungry and eats food
```

**Output**

```text
∀x(Student(x) ∧ Hungry(x) → Eat(x,Food))
```

---

## 🧠 Supported Sentence Types

### Universal Statements

```text
Every student studies
Every dog barks
```

### Existential Statements

```text
Some student reads books
A dog barks
```

### Negative Statements

```text
No student writes exam
No dog bites people
```

### Property-Based Statements

```text
Every student is hungry
Every dog is angry
```

### Property + Action Statements

```text
Every student is hungry and eats food
Every dog is angry and bites people
```

### Conditional Statements

```text
If a student is hungry, it eats food
If a dog is angry, it bites people
```

### Relative Clause Statements

```text
Every student who studies passes exam
Every dog that barks scares people
```

---

## 🔍 Reasoning Examples

### Input

```text
Every student studies and writes exam
```

### Query

```text
Does student study?
```

### Result

```text
Yes, it studies.
```

---

## 🚀 Future Enhancements

* Multi-sentence reasoning
* Knowledge base integration
* Context-aware reasoning
* Transformer-based NLP models
* Web deployment using Flask/FastAPI
* Voice input support
* Knowledge graph generation

---

## 📚 References

```text
[1] S. Russell and P. Norvig,
    Artificial Intelligence: A Modern Approach,
    4th Edition, Pearson, 2021.

[2] D. Jurafsky and J. H. Martin,
    Speech and Language Processing,
    3rd Edition, 2023.

[3] NLTK Documentation
    https://www.nltk.org/

[4] A. Turing,
    Computing Machinery and Intelligence,
    Mind, 1950.

[5] J. McCarthy,
    Programs with Common Sense,
    1959.
```
