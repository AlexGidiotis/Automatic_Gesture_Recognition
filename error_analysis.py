import os
import re
import  numpy as np

classes = ["SIL", "BS", "BN", "CP", "CV", "CN", "CF", "DC", "FM", "FN", "FU", "MC", "OK", "PF", "PR", "SP", "TT", "ST", "VA", "VQ", "NU"]
classnum=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
out_file = "/home/alex/Documents/Data/Training_Scripts/recout.mlf"

tf = open(out_file,'r')
clnums = []
pr_classes = []
count = 0
for line in tf:
    if line.rstrip().startswith('"'): 
        clnum = int(re.findall('.*_(\d+).rec',line)[0])
        clnums.append(clnum)
        count = 0
    elif line.rstrip().startswith('0'):
        count += 1
        if count == 1:
            cls = re.findall('0 \d+ (\w{2,3})',line)[0]
            pr_classes.append(cls)

true_pos_total = 0.0
for cln,cl in zip(classnum, classes):
    total = clnums.count(cln)
    predicted_positives = pr_classes.count(cl)

    true_pos = 0.0
    false_neg = 0.0
    false_pos = 0.0
    for i,j in zip(clnums,pr_classes):

        if i == cln:
            if j == cl:
                true_pos += 1.0  
            else:
                false_neg += 1.0 
        else:
            if j == cl:
                false_pos += 1.0
    if predicted_positives > 0:         
        precision = true_pos/predicted_positives
    else: 
        precision = 0
        print "Haven't predicted anything for this class."
    recall = true_pos/total
    if (precision+recall) > 0:
        f1_score = 2*(precision*recall)/(precision+recall)
    else:
        f1_score = 0
        print "No f1-score available."
    print("Class: %s" % cl)
    print("Precision: %f Recall: %f F1 score: %f" %(precision,recall,f1_score))
    true_pos_total += true_pos
      
N = len(clnums)
acc = true_pos_total/N
print acc

        