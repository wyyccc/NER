import pandas as pd
from tqdm import tqdm
from data_preprocess_eval import data_eval
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

tag2index = {
    "O": "O",
    "B-6": "人名", "I-6": "人名",
    "B-7": "地名", "I-7": "地名",
    "B-8": "时间", "I-8": "时间",
    "B-9": "会议", "I-9": "会议",
    "B-11": "核心观点", "I-11": "核心观点",
    "B-12": "组织机构", "I-12": "组织机构",
    "B-13": "政策词汇", "I-13": "政策词汇",
    "B-14": "政策倾向", "I-14": "政策倾向",
}

tag2index = {
    "O": 0,
    "B-6": 1, "I-6": 2, "E-6":3,
    "B-7": 4, "I-7": 5, "E-7":6,
    "B-8": 7, "I-8": 8, "E-8":9,
    "B-9": 10, "I-9": 11, "E-9":12,
    "B-11": 13, "I-11": 14, "E-11":15,
    "B-12": 16, "I-12": 17, "E-12":18,
    "B-13": 19, "I-13": 20, "E-13":21,
    "B-14": 22, "I-14": 23, "E-14":24,
}

def read_data(csv_path):
    result = list(pd.read_csv(csv_path)['result'])
    for i in tqdm(range(len(result))):
        result[i] = result[i].split(' ')
    return result

def evaluation(pred, true):
    pred = sum(pred, [])
    true = sum(true, [])
    for i in tqdm(range(len(pred))):
        pred[i] = tag2index[pred[i]]
        true[i] = tag2index[true[i]]
    print(classification_report(true, pred))
    print('acc:', accuracy_score(pred, true))
    print('precision:', metrics.precision_score(true, pred, average="micro"))
    print('recall:', metrics.precision_score(true, pred, average="micro"))
    print('f1:', metrics.f1_score(true, pred, average="micro"))
    return 0

def evaluation_entity(pred, true, type = 'BIO'):
    TP = 0
    FP = 0
    FN = 0
    for i in range(len(pred)):
        temp_pred = pred[i]
        temp_true = true[i]
        tp = 0
        fp = 0
        gt = 0
        for j in range(len(temp_true)):
            if temp_true[j][0] == 'B':
                gt += 1
        for j in range(len(temp_pred)):
            if temp_pred[j][0] == 'B':
                if temp_true[j] != temp_pred[j]:
                    fp += 1
                    continue
                temp = True
                if type == 'BIO':
                    for k in range(j, len(temp_pred)):
                        if temp_pred[k][0] != 'I':
                            if temp_true[k][0] == 'I':
                                temp = False
                            break
                        if temp_pred[k] != temp_true[k]:
                            temp = False
                            break
                elif type == 'BIOE':
                    for k in range(j, len(temp_pred)):
                        if temp_pred[k][0] == 'E':
                            if temp_true[k] != temp_pred[k]:
                                temp = False
                            break
                        if temp_pred[k] != temp_true[k]:
                            temp = False
                            break
                if temp:
                    tp += 1
                else:
                    fp += 1
        fn = gt - tp
        TP += tp
        FP += fp
        FN += fn
    if TP+FP == 0:
        precision = 0
    else:
        precision = TP/(TP+FP)
    if TP+FN == 0:
        recall = 0
    else:
        recall = TP/(TP+FN)
    if precision == 0 and recall == 0:
        f1 = 0
    else:
        f1 = 2*precision*recall/(precision+recall)
    print('precison:', precision)
    print('recall', recall)
    print('f1:', f1)
    return f1


if __name__ == '__main__':
    type = 'BIOE'
    csv_path = '/mnt/disk2/wyc/ner/bert-bilstm-crf/result/csv/bert-bilstm-crf-v6.csv'
    pred = read_data(csv_path)
    data, true = data_eval(type = type)
    # evaluation(pred, true)
    evaluation_entity(pred, true, type = type)
