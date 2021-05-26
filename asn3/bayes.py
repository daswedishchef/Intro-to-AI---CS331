import numpy as np

junk = ("'", ",", ".", "!", "?", "(", ")", "-", "\n")

def strip(testName, trainName):
    test = open(testName, 'r')
    line = test.readline()
    testD = list()
    test_vocab = list()
    testLabel = list()
    print("Testing")
    while line:
        for j in junk:
            line = line.replace(j, "")
        testD.append(line)
        sem = line.split()
        for word in sem:
            if word not in test_vocab:
                test_vocab.append(word)
        line = test.readline()
    test.close()
    train = open(trainName, 'r')
    line = train.readline()
    trainD = list()
    train_vocab = list()
    print("Training")
    while line:
        for j in junk:
            line = line.replace(j, "")
        trainD.append(line)
        sem = line.split()
        for word in sem:
            if word not in train_vocab:
                train_vocab.append(word)
        line = train.readline()
    train.close()

    return testD, trainD, test_vocab, train_vocab


def main():
    prepro = strip('testSet.txt', 'trainingSet.txt')


main()