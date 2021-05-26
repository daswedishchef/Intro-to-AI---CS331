#Authors
#Spencer Carlson
#Sheng Tse Tsai

import numpy as np

junk = ("'", ",", ".", "!", "?", "(", ")", "-", "\n", ":", ";", "/", "*")

def strip(testName, trainName):
    test = open(testName, 'r')
    line = test.readline()
    testD = list()
    test_vocab = list()
    while line:
        for j in junk:
            line = line.replace(j, "")
        testD.append(line)
        sem = line.split()
        for word in sem:
            word = word.lower()
            if word not in test_vocab:
                test_vocab.append(word)
        line = test.readline()
    test.close()
    train = open(trainName, 'r')
    line = train.readline()
    trainD = list()
    train_vocab = list()
    while line:
        for j in junk:
            line = line.replace(j, "")
        trainD.append(line)
        sem = line.split()
        for word in sem:
            word = word.lower()
            if word not in train_vocab:
                train_vocab.append(word)
        line = train.readline()
    train.close()
    test_vocab = sorted(test_vocab)
    train_vocab = sorted(train_vocab)

    return testD, trainD, test_vocab, train_vocab

def featureGen(vocab, cases):
    print("Vocab Length: ")
    print(len(vocab))
    feature = list()
    for case in cases:
        testF = list()
        feat = case.split("\t")
        label = feat[1]
        for i in range(len(vocab)):
            if vocab[i] in feat[0]:
                testF.append(1)
            else:
                testF.append(0)
        testF.append(int(label))
        feature.append(testF)
    return feature

def label(data):
    evidence = list()
    labels = list()
    for d in data:
        evidence.append(d[:-1])
        labels.append(d[-1])
    return evidence, labels

def classy(data, test, vocab):
    #separate labels and data points
    evidence, labels = label(data)
    ntrue = 0
    nfalse = 0
    p_true = list()
    p_false = list()
    #initiate lists to zero for probabilities of each feature
    for j in range(len(evidence[0])):
        p_true.append(0)
        p_false.append(0)
    #for each case
    for i in range(len(labels)):
        if labels[i] == 1:
            ntrue += 1
            #if positive sum instances
            for f in range(len(evidence[i])):
                p_true[f] += evidence[i][f] 
        else:
            #if negative sum instances
            nfalse += 1
            for f in range(len(evidence[i])):
                p_false[f] += evidence[i][f]
    #P(word|class)
    for i in range(len(p_false)):
        p_false[i] += 1
        p_false[i] /= (nfalse + 2)
    for i in range(len(p_true)):
        p_true[i] += 1
        p_true[i] /= (ntrue + 2)
    #separate test data and labels
    testRaw = featureGen(vocab, test)
    test_data, Tlabels = label(testRaw)
    results = list()
    #for each test case
    for i in range(len(test_data)):
        #P(true)
        pT = np.log((ntrue + 1)/(ntrue + nfalse + 2))
        #P(false)
        # pF = 1-pT
        pF = np.log((nfalse + 1)/(ntrue + nfalse + 2))
        for j in range(len(test_data[i])):
            #word exists
            if test_data[i][j] == 1:
                pT += np.log(p_true[j])
                pF += np.log(p_false[j])
            #word does not exist
            else:
                pF += np.log(1-p_false[j])
                pT += np.log(1-p_true[j])
        #if probability of 0 is higher, add to results
        if pF > pT:
            results.append(0)
        else:
            results.append(1)
    acc = 0
    index = 0
    #calculate accuracy
    for i in range(len(results)):
        if results[i] == Tlabels[i]:
            acc += 1
        index += 1
    accuracy = acc/index
    return results, accuracy



def output_file(name, vocab, features):
    output = open(name, 'w')
    output.write(str(vocab))
    output.write(", classlabel\n")
    for feat in features:
        output.write(str(feat))
        output.write("\n")
    output.close()

def main():
    prepro = strip('testSet.txt', 'trainingSet.txt')
    test_cases = prepro[0]
    train_cases = prepro[1]
    test_vocab = prepro[2]
    train_vocab = prepro[3]
    F_test = featureGen(prepro[2], prepro[0])
    F_train = featureGen(prepro[3], prepro[1])
    training = classy(F_train, train_cases, train_vocab)
    testing = classy(F_train, test_cases, train_vocab)
    testOut = open("results.txt", 'w')
    testOut.write("Training Results\n")
    testOut.write("Accuracy: ")
    testOut.write(str(training[1]))
    testOut.write("\n")
    testOut.write("Test Results\n")
    testOut.write("Accuracy: ")
    testOut.write(str(testing[1]))
    testOut.write("\n")
    output_file("preprocessed_train.txt", train_vocab, F_train)
    output_file("preprocessed_test.txt", test_vocab, F_test)

    
main()