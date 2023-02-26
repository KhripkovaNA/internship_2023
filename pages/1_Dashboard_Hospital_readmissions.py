import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.join(FILE_DIR, os.pardir)
IMAGE_PATH = os.path.join(PARENT_DIR, "image", "hospital_readmissions.png")
DATA_PATH = os.path.join(PARENT_DIR, "data", "hospital_readmissions.csv")

@st.cache_data
def load_dataset(data_link):
    dataset = pd.read_csv(data_link)
    return dataset

df_raw = load_dataset(DATA_PATH)
df = df_raw[['age', 'diag_1', 'diag_2', 'diag_3',
         'glucose_test', 'A1Ctest', 'readmitted']]
cols = df.columns.tolist()
renames = ['Age', 'Primary diagnosis', 'Secondary diagnosis',
           'Additional secondary diagnosis', 'Glucose test', 'A1Ctest', 'Readmitted']
col_dict = {col: rename for col, rename in zip(cols, renames)}
df = df.rename(columns=col_dict)

st.header("Dashboard - Hospitals Readmissions Data")

img = plt.imread(IMAGE_PATH)
st.image(img)
show_head = st.checkbox('show raw data')
if show_head:
    st.dataframe(df_raw, height=300, use_container_width=True)

def show_counts(df, category, percent=True):
    if percent == True:
        count_df = pd.DataFrame(df[category].value_counts(normalize=True).rename('Percent'))
    else:
        count_df = pd.DataFrame(df[category].value_counts().rename('Count'))
    count_df.index.name = category
    return count_df

option = st.selectbox('Select feature to display count', ('Feature',
                                                          'Age',
                                                          'Primary diagnosis',
                                                          'Secondary diagnosis',
                                                          'Additional secondary diagnosis',
                                                          'Glucose test',
                                                          'A1Ctest',
                                                          'Readmitted'))

if option != 'Feature':
    st.write('You selected:', option)
    show_percent = st.checkbox('show percent')
    if show_percent:
        count_df = show_counts(df, option)
        st.dataframe(count_df.style.format("{:.2%}"), height=300, use_container_width=True)
    else:
        count_df = show_counts(df, option, False)
        st.dataframe(count_df, height=300, use_container_width=True)

def pct_hist(df, col, order=None, x_rotation=0):
    order = order
    sns.barplot(x=col, y=df.index, data=df, ax=ax,
                estimator=lambda x: len(x)/len(df)*100,
                order = order)
    for p in ax.patches:
        h, w, x = p.get_height(), p.get_width(), p.get_x()
        xy = (x + w / 2, h + 1)
        text = f'{h:0.1f}%'
        ax.annotate(text=text, xy=xy,
                    ha='center', va='center',
                    size=10, xytext=(0, 0),
                    textcoords='offset points')
    sns.despine(left=True)
    ax.set_title(col)
    ax.set(ylabel=None, xlabel=None, yticks=[], yticklabels=[])
    ax.set_xticklabels(ax.get_xticklabels(), rotation=x_rotation)


option_bar = st.selectbox('Select feature to display barchart', ('Feature',
                                                                  'Age',
                                                                  'Primary diagnosis',
                                                                  'Secondary diagnosis',
                                                                  'Additional secondary diagnosis',
                                                                  'Glucose test',
                                                                  'A1Ctest',
                                                                  'Readmitted'))

if option_bar != 'Feature':
    st.write('You selected:', option_bar)
    fig, ax = plt.subplots(figsize=(8, 6))
    if option_bar in ['Primary diagnosis', 'Secondary diagnosis', 'Additional secondary diagnosis']:
        order = df['Primary diagnosis'].value_counts().index
        pct_hist(df, option_bar, order=order, x_rotation=60)
    else:
        if option_bar == 'Age':
            order = sorted(df['Age'].unique())
        elif option_bar in ['Glucose test', 'A1Ctest']:
            order = df['Glucose test'].value_counts().index
        else:
            order = df[option_bar].value_counts().index
        pct_hist(df, option_bar, order=order)
    st.pyplot(fig)
