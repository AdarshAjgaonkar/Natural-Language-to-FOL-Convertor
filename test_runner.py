# test_runner.py  (FINAL — DIRECT CALL, NO BUGS)

from infer_transformer import get_fol

test_sentences = [
    "Every scientist analyzes data",
    "Every athlete runs",
    "Some robots build machines",
    "If a student is tired it sleeps",
    "If a dog is hungry it eats food",
    "Every teacher loves a student",
    "Every bird flies and sings",
    "Every chef cooks food and serves meals",
    "Every fish eats fish",
    "Some cats sleep",
    "If a driver is tired it stops and rests",
    "Every programmer writes code and debugs programs"
]

expected_outputs = [
    "∀x(Scientist(x)→Analyze(x,Data))",
    "∀x(Athlete(x)→Run(x))",
    "∃x(Robot(x)∧Build(x,Machines))",
    "∀x(Student(x)∧Tired(x)→Sleep(x))",
    "∀x(Dog(x)∧Hungry(x)→Eat(x,Food))",
    "∀x(Teacher(x)→∃y(Student(y)∧Love(x,y)))",
    "∀x(Bird(x)→Fly(x)∧Sing(x))",
    "∀x(Chef(x)→Cook(x,Food)∧Serve(x,Meals))",
    "∀x(Fish(x)→Eat(x,Fish))",
    "∃x(Cat(x)∧Sleep(x))",
    "∀x(Driver(x)∧Tired(x)→Stop(x)∧Rest(x))",
    "∀x(Programmer(x)→Write(x,Code)∧Debug(x,Programs))"
]

correct = 0
total = len(test_sentences)

print("\n========== TEST RESULTS ==========\n")

for i in range(total):

    sentence = test_sentences[i]
    predicted = get_fol(sentence)
    expected = expected_outputs[i]

    print(f"Test {i+1}")
    print(f"Input     : {sentence}")
    print(f"Expected  : {expected}")
    print(f"Predicted : {predicted}")

    if predicted == expected:
        print("✅ PASS\n")
        correct += 1
    else:
        print("❌ FAIL\n")

accuracy = (correct / total) * 100

print("=================================")
print(f"Total: {total}")
print(f"Passed: {correct}")
print(f"Accuracy: {accuracy:.2f}%")
print("=================================")