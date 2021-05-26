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

def classy(data, test):
    evidence, labels = label(data)
    ntrue = 0
    nfalse = 0
    p_true = list()
    p_false = list()
    for j in range(len(evidence[0])):
        p_true.append(0)
        p_false.append(0)
    for i in range(len(labels)):
        if labels[i] == 1:
            ntrue += 1
            for f in range(len(evidence[i])):
                p_true[f] += evidence[i][f] 
        else:
            nfalse += 1
            for f in range(len(evidence[i])):
                p_false[f] += evidence[i][f]
    #P(word|class)
    for i in range(len(p_false)):
        p_true[i] += 1
        p_true[i] /= (ntrue + 2)
        p_false[i] += 1
        p_false[i] /= (nfalse + 2)
    #P(true)
    pT = ntrue/(ntrue + nfalse)
    #P(false)
    # pF = 1-pT
    pF = nfalse/(ntrue + nfalse)
    test_data, Tlabels = label(test)
    results = list()
    for i in range(len(test_data)):
        Tprob = -1.0
        Fprob = -1.0
        for j in range(len(test_data[i])):
            if test_data[i][j] == 1:
                if Tprob == -1.0:
                    Tprob = np.log(p_true[j])
                else:
                    Tprob *= np.log(p_true[j])
            # else:
                if Fprob == -1.0:
                    Fprob = np.log(1-p_false[j])
                else:
                    Fprob *= np.log(1- p_false[j])
        Fprob *= pF
        Tprob *= pT
        if Fprob > Tprob:
            results.append(0)
        else:
            results.append(1)
    acc = 0
    index = 0
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
    print(classy(F_train, F_train))
    output_file("preprocessed_train.txt", train_vocab, F_train)
    output_file("preprocessed_test.txt", test_vocab, F_test)

    
main()