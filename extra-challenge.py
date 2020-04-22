import streamlit as st
import pandas as pd
import numpy as np
import base64
import matplotlib.pyplot as plt



def remove_outlier(df_in, col_name):
    q1 = df_in[col_name].quantile(0.25)
    q3 = df_in[col_name].quantile(0.75)
    iqr = q3-q1 #Interquartile range
    fence_low  = q1-1.5*iqr
    fence_high = q3+1.5*iqr
    df_out = df_in.loc[(df_in[col_name] > fence_low) & (df_in[col_name] < fence_high)]
    return df_out

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
    return href

def main():
   
    # SIDEBAR
    st.sidebar.image('faceDiogo.png', width= 200,)
    st.sidebar.markdown('## Author:')
    st.sidebar.markdown('# Diogo Puppim de Oliveira')
    st.sidebar.markdown('## Linkedin:') 
    st.sidebar.markdown('### https://www.linkedin.com/in/diogo-puppim-de-oliveira-207905a7/')
   

    # BODY
    # st.image('logo.png', lswidth= 200)
    st.title('AceleraDev Data Science')
    st.subheader('Extra Challenge')
    st.markdown('## **Generic data set cleaning and basic analysis** ')
    st.image('panda-3-1325641.jpg', width=300)
    
    option = st.selectbox(
        'Select you dataset',
            ('sample01', 'sample02','my dataset')
       )

    if option == 'sample01':
            file = 'movies.csv'
    elif option == 'sample02':
            file = 'ratings.csv'
    else:
        file  = st.file_uploader('Add you file (.csv)', type = 'csv')
   
    if file is not None:
        st.markdown('# **Data Visualization**')
        df = pd.read_csv(file)    
        st.markdown(f'**Dataset:**')
        numberLine = st.slider('Choose the number of rows you want to see', min_value=5, max_value=30)
        st.dataframe(df.head(numberLine))
        st.markdown(f'**Number of rows:** {df.shape[0]}')
        st.markdown(f'**Number of columns:** {df.shape[1]}')
        st.markdown(f'**Name of columns:** {list(df.columns)}')
        st.markdown(f'**Statistics:**')
        st.write(df.describe())

        aux = pd.DataFrame({'name' : df.columns, 'types' : df.dtypes, 'NA #': df.isna().sum(), 'NA %' : (df.isna().sum() / df.shape[0]) * 100})
        st.markdown('**Count of types:**')
        st.write(aux.types.value_counts())
        st.markdown('**Table with column and percentage of missing data :**')
        st.table(aux[aux['NA #'] != 0][['types', 'NA %']])

        check_hist = st.checkbox( 'Display a bar chart',value=True ,key='hist')
        if check_hist:
        
            optionHist = st.selectbox(
            'Select you column',
                (df.columns),index=0, key='thit'
            )
            try:
                plt.hist(df[optionHist], bins=20)
                st.pyplot()
            except:
                st.markdown('####  Impossible in this column, select other! ')

        check_bar = st.checkbox( 'Display a bar chart',value=True ,
        key='bar')
        if check_bar:
           
            optionbar = st.selectbox(
            'Select you column',
                (df.columns),index=0, key='bar'
            )
            try:
                st.bar_chart(df[optionbar])
            except:
                st.markdown('####  Impossible in this column, select other! ')

        check_plot = st.checkbox( 'Display a line chart',value=True ,
        key='check_plot')
        if check_plot:
            optionplot = st.selectbox(
            'Select you column',
                (df.columns),index=0 , key='tplot'
            )
            try:
                st.line_chart(df[optionplot])
            except:
                st.markdown('####  Impossible in this column, select other! ')

        st.markdown('# Data set cleaning')
        checkout = st.checkbox('Remove outlier',value=False,key='out')
        if checkout:
            optionout = st.selectbox(
            'Select you column',
                (df.columns),index=0, key='outop'
            )
            try:
                df= remove_outlier(df, optionout)
            except:
                st.markdown('####  in numeric columns only, select another! ')
        checkWhite = st.checkbox('Remove whitespace on columns',value=False,key='white')
        if checkWhite:
            cols = df.columns
            cols = cols.map(lambda x: x.replace(' ','_')if isinstance(x, (str)) else x)
            df.columns = cols
            st.markdown(f'**Name of columns:** {list(df.columns)}')


        checkNull = st.checkbox('Drop rows of dataset nan ou null',value=False,key='null')
        if checkNull:
            df.dropna(inplace=True)
            st.subheader('has no rows with null values')
            st.subheader('download new dataset : ')
            st.markdown(get_table_download_link(df), unsafe_allow_html=True)
        else:
            df = pd.read_csv(file)
            st.subheader('Input of numerical data :')
            select_method = st.radio('Choose a method below :', ('Mean', 'Median'))
           
            if select_method == 'Mean':
                dfmean= df[df.columns].fillna(value=df[df.columns].mean())
                st.subheader('download new dataset : ')
                st.markdown(get_table_download_link(dfmean), unsafe_allow_html=True)
            if select_method == 'Median':
                dfmedian= df[df.columns].fillna(value=df[df.columns].median())
                st.subheader('download new dataset : ')
                st.markdown(get_table_download_link(dfmedian), unsafe_allow_html=True)


if __name__ == '__main__':
	main()