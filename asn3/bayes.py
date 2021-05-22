import numpy as np

def strip(testName, trainName):
    test = open(testName, 'r')
    line = test.readline()
    testD = list()
    test_vocab = list()
    print("Testing")
    while line:
        line = line.replace("'", "")
        line = line.replace(",", "")
        line = line.replace(".", "")
        line = line.replace("!", "")
        line = line.replace("?", "")
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
        line = line.replace("'", "")
        line = line.replace(",", "")
        line = line.replace(".", "")
        line = line.replace("!", "")
        line = line.replace("?", "")
        trainD.append(line)
        sem = line.split()
        for word in sem:
            if word not in train_vocab:
                train_vocab.append(word)
        line = train.readline()
    train.close()
    return test_vocab, train_vocab


def main():
    vocab = strip('testSet.txt', 'trainingSet.txt')
    print("test", vocab[0])
    print("train", vocab[1])

main()