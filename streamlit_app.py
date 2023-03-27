import streamlit as st
import pandas as pd
from apriori import runApriori, dataFromFile, to_str_results


st.markdown("# Apriori Streamlit")

# st.sidebar.markdown(
#     """
#     """
# )

# ? init dataset
default_csv = st.file_uploader('pick datasets',
                               type=['csv'],
                               label_visibility='collapsed',
                               help='')

if default_csv == None:
    default_csv = 'tesco.csv'
    st.markdown(
        'The dataset is a toy dataset contain frequently purchased grocery items')

header = 0 if st.button('Head') else None
st.markdown('Here are some sample rows from the dataset ')
csv_file = pd.read_csv(default_csv, header=header,)
st.table(csv_file.head())

st.markdown('---')
st.markdown("## Inputs")

st.markdown('''
            **Support** shows transactions with items purchased together in a single transaction.
            
            **Confidence** shows transactions where the items are purchased one after the other.''')

st.markdown(
    'Support and Confidence for Itemsets A and B can be represented by formulas')

support_helper = ''' > Support(A) = (Number of transactions in which A appears)/(Total Number of Transactions') '''

confidence_helper = ''' > Confidence(A->B) = Support(AUB)/Support(A)') '''
st.markdown('---')

support = st.slider("Enter the Minimum Support Value", min_value=0.1,
                    max_value=0.9, value=0.15,
                    help=support_helper)

confidence = st.slider("Enter the Minimum Confidence Value", min_value=0.1,
                       max_value=0.9, value=0.6, help=confidence_helper)

inFile = dataFromFile(default_csv)
st.write(inFile)


items, rules = runApriori(inFile, support, confidence)

i, r = to_str_results(items, rules)

st.markdown("## Results")

st.markdown("### Frequent Itemsets")
st.table(items)

st.markdown("### Frequent Rules")
st.table(rules)


# debug
debug = True

if debug:
    st.write(inFile)


# ! end debug
