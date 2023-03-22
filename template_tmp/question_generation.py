import random

operations = ["union", "intersection", "difference"]

set1 = []
set2 = []

def generateRandomNumbers():
    set1_length = random.randint(1,5)
    set2_length = random.randint(1,5)

    for i in range(set1_length):
        value1 = random.randint(0,30)
        if value1 not in set1:
            set1.append(value1)

    for j in range(set2_length):
        value2 = random.randint(0,30)
        if value2 not in set2:
            set2.append(value2)

    return sorted(set1), sorted(set2)


def generateRandomQuestion():
    operation = random.choice(operations)
    generateRandomNumbers()
    question = "Calculate the {} of {} and {}".format(operation, set1, set2)
    print(question)


generateRandomQuestion()
