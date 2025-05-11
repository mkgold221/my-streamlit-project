import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(
    page_title="Titanic Dashboard",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    url = "https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv"
    return pd.read_csv(url)

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

# Main dashboard
st.title("Titanic Passenger Analysis")
col1, col2, col3 = st.columns(3)
col1.metric("Total Passengers", len(filtered_df))
col2.metric("Survival Rate", f"{filtered_df['Survived'].mean()*100:.1f}%")
col3.metric("Average Age", f"{filtered_df['Age'].mean():.1f} years")

# Visualizations
st.header("Passenger Demographics")

# Age Distribution
fig1, ax1 = plt.subplots()
ax1.hist(filtered_df['Age'].dropna(), bins=20, color='skyblue')
ax1.set_title("Age Distribution")
ax1.set_xlabel("Age")
ax1.set_ylabel("Count")
st.pyplot(fig1)

# Survival by Class
st.subheader("Survival by Passenger Class")
fig2, ax2 = plt.subplots()
class_survival = filtered_df.groupby('Pclass')['Survived'].mean()
class_survival.plot(kind='bar', color=['#1f77b4', '#ff7f0e', '#2ca02c'], ax=ax2)
ax2.set_title("Survival Rate by Class")
ax2.set_xlabel("Passenger Class")
ax2.set_ylabel("Survival Rate")
st.pyplot(fig2)

# Show raw data
if st.checkbox("Show raw data"):
    st.dataframe(filtered_df)
