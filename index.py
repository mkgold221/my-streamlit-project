
import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="Data Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    url = "https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv"
    data = pd.read_csv(url)
    return data

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
gender_filter = st.sidebar.multiselect(
    "Select Gender:",
    options=df['Sex'].unique(),
    default=df['Sex'].unique()
)

class_filter = st.sidebar.multiselect(
    "Select Passenger Class:",
    options=df['Pclass'].unique(),
    default=df['Pclass'].unique()
)

age_range = st.sidebar.slider(
    "Select Age Range:",
    min_value=int(df['Age'].min()),
    max_value=int(df['Age'].max()),
    value=(int(df['Age'].min()), int(df['Age'].max()))
)

# Apply filters
filtered_df = df[
    (df['Sex'].isin(gender_filter)) & 
    (df['Pclass'].isin(class_filter)) &
    (df['Age'] >= age_range[0]) & 
    (df['Age'] <= age_range[1])
]

# Main content
st.title("🚢 Titanic Passenger Analysis Dashboard")
st.markdown("""
This interactive dashboard analyzes passenger data from the Titanic. 
Use the filters in the sidebar to explore the data.
""")

# Key metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Passengers", len(filtered_df))
col2.metric("Survival Rate", f"{filtered_df['Survived'].mean()*100:.1f}%")
col3.metric("Average Age", f"{filtered_df['Age'].mean():.1f} years")

st.divider()

# Charts
tab1, tab2, tab3 = st.tabs(["Survival Analysis", "Demographics", "Fare Distribution"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Survival by class
        fig1 = px.pie(
            filtered_df,
            names='Pclass',
            title='Passenger Distribution by Class'
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Survival by gender
        fig2 = px.histogram(
            filtered_df,
            x='Sex',
            color='Survived',
            barmode='group',
            title='Survival by Gender',
            labels={'Survived': 'Survived'},
            color_discrete_map={0: '#FFA07A', 1: '#20B2AA'}
        )
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        # Age distribution
        fig3 = px.histogram(
            filtered_df,
            x='Age',
            nbins=20,
            title='Age Distribution',
            color_discrete_sequence=['#4682B4']
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        # Age vs Fare
        fig4 = px.scatter(
            filtered_df,
            x='Age',
            y='Fare',
            color='Sex',
            title='Age vs Fare',
            hover_data=['Name']
        )
        st.plotly_chart(fig4, use_container_width=True)

with tab3:
    # Fare distribution by class
    fig5 = px.box(
        filtered_df,
        x='Pclass',
        y='Fare',
        color='Pclass',
        title='Fare Distribution by Passenger Class'
    )
    st.plotly_chart(fig5, use_container_width=True)

# Show raw data
st.divider()
if st.checkbox("Show raw data"):
    st.subheader("Filtered Data")
    st.dataframe(filtered_df)