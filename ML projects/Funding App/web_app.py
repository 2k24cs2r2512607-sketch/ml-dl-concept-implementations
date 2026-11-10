import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(
    layout='wide',
    page_title='Startup Analysis'
)

df = pd.read_csv(r"D:\Campusx\Streamlit\startup_cleaned.csv")
df['date']=pd.to_datetime(df['date'],errors='coerce')
df['year']=df['date'].dt.year
df['month']=df['date'].dt.month
def overall_analysis():
    st.title("Overall ")
    total=round(df['amount'].sum())
    max_funding=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    avg_funding=round(df.groupby('startup')['amount'].sum().mean())
    num_startup=df['startup'].nunique()
    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric('Total',str(total)+'Cr')
    with col2:
        st.metric('Max',str(max_funding)+'Cr')
    with col3:
        st.metric('Average Funding',str(avg_funding)+'Cr')
    with col4:
        st.metric('Funded Startups',str(num_startup))
    st.header("MOM graph")
    select_op=st.selectbox('Select Type',['Total','Count'])
    if select_op=='Total':
    
        temp_df=(df.groupby(['year','month'])['amount'].sum().reset_index())
        temp_df['x_axis']=temp_df['month'].astype('str')+'-'+temp_df['year'].astype('str')
        fig4,ax4=plt.subplots()
        ax4.plot(temp_df['x_axis'],temp_df['amount'])
        st.pyplot(fig4)
    else:
        temp_df=(df.groupby(['year','month'])['startup'].count().reset_index())
        temp_df['x_axis']=temp_df['month'].astype('str')+'-'+temp_df['year'].astype('str')
        fig4,ax4=plt.subplots()
        ax4.plot(temp_df['x_axis'],temp_df['startup'])
        st.pyplot(fig4)

    
def load_investor_details(investor):

    st.title(investor)

    # ==========================================
    # Recent 5 Investments
    # ==========================================

    last5_df = df[
        df['investors'].str.contains(investor, na=False)
    ].head()[[
        'date',
        'startup',
        'vertical',
        'city',
        'round',
        'amount'
    ]]

    st.subheader("Most Recent Investments")

    st.dataframe(
        last5_df,
        use_container_width=True
    )


    # ==========================================
    # Biggest Investments
    # ==========================================

    big_series = (
        df[
            df['investors'].str.contains(investor, na=False)
        ]
        .groupby('startup')['amount']
        .sum()
        .sort_values(ascending=False)
    )

    st.subheader("Biggest Investments")

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.bar(
        big_series.index,
        big_series.values
    )

    ax.set_xlabel("Startup")
    ax.set_ylabel("Investment Amount")

    ax.set_title(
        f"Investments by {investor}",
        fontsize=15,
        fontweight='bold'
    )

    plt.xticks(
        rotation=45,
        ha='right'
    )

    ax.grid(
        axis='y',
        linestyle='--',
        alpha=0.3
    )

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()

    st.pyplot(fig)


    # ==========================================
    # Other Analysis
    # ==========================================

    vertical_series = (
        df[
            df['investors'].str.contains(investor, na=False)
        ]
        .groupby('vertical')['amount']
        .sum()
    )

    round_series = (
        df[
            df['investors'].str.contains(investor, na=False)
        ]
        .groupby('round')['amount']
        .sum()
    )

    city_series = (
        df[
            df['investors'].str.contains(investor, na=False)
        ]
        .groupby('city')['amount']
        .sum()
    )


    # ==========================================
    # TWO COLUMNS
    # ==========================================

    col1, col2 = st.columns(2)


    # ------------------------------------------
    # Sectors / Vertical
    # ------------------------------------------

    with col1:

        st.subheader("Sectors Invested In")

        fig1, ax1 = plt.subplots(figsize=(6, 5))

        ax1.pie(
            vertical_series,
            labels=vertical_series.index,
            autopct='%0.1f%%',
            startangle=90,
            wedgeprops=dict(width=0.45)
        )

        ax1.set_title(
            "Investment by Sector",
            fontsize=13,
            fontweight='bold'
        )

        plt.tight_layout()

        st.pyplot(fig1)


    # ------------------------------------------
    # Rounds
    # ------------------------------------------

    with col2:

        st.subheader("Rounds Invested In")

        fig2, ax2 = plt.subplots(figsize=(6, 5))

        ax2.pie(
            round_series,
            labels=round_series.index,
            autopct='%0.1f%%',
            startangle=90,
            wedgeprops=dict(width=0.45)
        )

        ax2.set_title(
            "Investment by Round",
            fontsize=13,
            fontweight='bold'
        )

        plt.tight_layout()

        st.pyplot(fig2)


    # ==========================================
    # Cities
    # ==========================================

    st.subheader("Cities Invested In")

    fig3, ax3 = plt.subplots(figsize=(10, 5))

    ax3.pie(
        city_series,
        labels=city_series.index,
        autopct='%0.1f%%',
        startangle=90,
        wedgeprops=dict(width=0.45)
    )

    ax3.set_title(
        "Investment by City",
        fontsize=13,
        fontweight='bold'
    )

    plt.tight_layout()

    st.pyplot(fig3)
    df['year']=df['date'].dt.year
    year_series=df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader("YOY Investment")
    fig4,ax4=plt.subplots()
    ax4.plot(year_series.index,year_series.values)
    st.pyplot(fig4)

# ==============================================
# SIDEBAR
# ==============================================

st.sidebar.title("Startup Funding Analysis")

option = st.sidebar.selectbox(
    'Select One',
    [
        'Overall Analysis',
        'Startup',
        'Investor'
    ]
)


# ==============================================
# OVERALL ANALYSIS
# ==============================================

if option == 'Overall Analysis':

    st.title("Overall Analysis")
    # bst.sidebar.button("Show Overall Analysis")
    overall_analysis()



# ==============================================
# STARTUP
# ==============================================

elif option == 'Startup':

    st.sidebar.selectbox(
        "Select StartUp",
        sorted(
            df['startup'].unique().tolist()
        )
    )

    btn1 = st.sidebar.button(
        'Find StartUp Details'
    )


# ==============================================
# INVESTOR
# ==============================================

else:

    selected_investor = st.sidebar.selectbox(
        'Select Investor',
        sorted(
            set(
                df['investors']
                .str.split(',')
                .sum()
            )
        )
    )

    btn2 = st.sidebar.button(
        "Find Investor Details"
    )

    if btn2:
        load_investor_details(
            selected_investor
        )

    st.title("Investor Analysis")