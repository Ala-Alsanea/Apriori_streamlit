
import pandas as pd
import streamlit as st
import os


def apriori(D, minSup):
    L = []
    result = find_frequent_one_itemsets(D, minSup)
    L1 = result["firstItemSet"]
    # Include the counts from the first itemset
    all_counts = [result["counts"]]
    L.append(L1)
    k = 2
    # print(isinstance(L[k - 2], list))
    # print(len(L[k - 2]))

    while isinstance(L[k - 2], list) and len(L[k - 2]) > 0:
        before_pruning_Ck, after_pruning_Ck = apriori_gen(L[k - 2])
        counts = count_itemsets(after_pruning_Ck, D)
        all_counts.append(counts)
        Lk = filter_by_min_sup(counts, minSup)
        L.append(Lk)
        k += 1

    return L, all_counts


def find_frequent_one_itemsets(D, minSup):
    counts = {}

    for t in D:
        for item in t:
            if str(item) == 'nan':
                continue
            counts[item] = counts.get(item, 0) + 1

    first_item_set = [item for item in counts.keys() if counts[item] >= minSup]
    return {"firstItemSet": first_item_set, "counts": counts}


def apriori_gen(Lk_1):
    new_itemsets_before_pruning = []
    new_itemsets_after_pruning = []
    len_Lk_1 = len(Lk_1)

    for i in range(len_Lk_1):
        for j in range(i + 1, len_Lk_1):
            itemset1 = str(Lk_1[i]).split(',')
            itemset2 = str(Lk_1[j]).split(',')

            # print(itemset1[:-1])
            # print(itemset2[:-1])

            # if itemset1[:-1] == itemset2[:-1]:
            #     if itemset1[-1] != itemset2[-1]:
            # st.write(itemset1)
            # st.write(itemset2[-1])
            new_itemset = sorted(itemset1 + [str(itemset2[-1])])

            new_itemsets_before_pruning.append(
                ','.join(map(str, new_itemset)))

            subsets = get_subsets(new_itemset, len(new_itemset) - 1)
            all_subsets_frequent = all(
                ','.join(map(str, subset)) in Lk_1 for subset in subsets
            )

            if all_subsets_frequent:
                new_itemsets_after_pruning.append(
                    ','.join(map(str, new_itemset)))

    return new_itemsets_before_pruning, new_itemsets_after_pruning


def get_subsets(itemset, k):
    if k == 0:
        return [[]]

    if len(itemset) < k:
        return []

    head, *tail = itemset

    subsets_without_head = get_subsets(tail, k)
    subsets_with_head = [(head, *subset)
                         for subset in get_subsets(tail, k - 1)]

    return subsets_without_head + subsets_with_head


def count_itemsets(Ck, D):
    counts = {}
    for c in Ck:
        counts[c] = 0

    for t in D:
        for c in Ck:
            items = c.split(',')
            if all(item in t for item in items):
                counts[c] = counts.get(c, 0) + 1

    return counts


def filter_by_min_sup(counts, minSup):
    return sorted(
        [itemset for itemset in counts.keys() if counts[itemset] >= minSup],
        key=lambda x: list(map(str, x.split(',')))
    )


file = st.file_uploader('pick datasets',
                        type=['csv'],
                        label_visibility='collapsed',
                        help='')

# st.write(file.readlines())
# st.write(dir(file))


if file is None:
    exit()

try:
    os.mkdir('DataSet')
except OSError:
    pass


with open("DataSet/"+file.name, "w") as f:
    for line in file.readlines():
        # st.write(line)
        # if line.strip("\n") != delLine:
        f.write(line.decode('utf-8'))


minSup = st.number_input('min Support', value=3)

if st.button('start'):

    csv_file = pd.read_csv("DataSet/"+file.name,
                           header=None, error_bad_lines=False)

    st.write(len(csv_file))
    st.table(csv_file.head(10))

    result = apriori(csv_file.values.tolist(), minSup)

    st.write(result[0])
    st.write(result[1])
