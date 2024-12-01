import streamlit as st
from database import SongRecommendation

def show_recommendation_page():
    st.markdown(
        """
        <style>
        body {
            background-color: #f0f2f6;
        }
        h1 {
            color: #3498db;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<h1>song recommendations</h1>", unsafe_allow_html=True)
    
    mood = st.selectbox(
        "select your current mood:",
        ["cheerful", "melancholy", "calm", "energetic", "romantic"]
    )

    location = st.selectbox(
        "select your location:",
        ["çim amfi", "fuaye", "kütüphane", "etü mutfak"]
    )
    
    if st.button("get recommendations"):
        recommendations = SongRecommendation.get_recommendations_by_mood_and_location(mood, location)
        
        if recommendations:
            st.write(f"### here are some songs for your mood: **'{mood}'** and your location: **'{location}'**")
            
            import pandas as pd
            recommendations_df = pd.DataFrame(recommendations)

            recommendations_df.index = range(1, len(recommendations_df) + 1)
            recommendations_df.index.name = "No."

            st.table(recommendations_df.rename(columns={
                "title": "Song Title",
                "artist": "Artist",
                "genre": "Genre"
            }))
        else:
            st.warning("no recommendations found for this mood and location")

    if st.button("back to homepage"):
        st.session_state["current_page"] = "home"