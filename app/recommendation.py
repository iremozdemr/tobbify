import streamlit as st
from database import SongRecommendation

def show_recommendation_page():
    st.markdown("<h1>Song Recommendations</h1>", unsafe_allow_html=True)
    
    # Kullanıcıdan ruh hali girişi
    mood = st.selectbox(
        "Select your current mood:",
        ["cheerful", "melancholy", "calm", "energetic", "romantic"]
    )

    location = st.selectbox(
        "Select your location:",
        ["çim amfi", "fuaye", "kütüphane", "etü mutfak"]
    )
    
    if st.button("Get Recommendations"):
        recommendations = SongRecommendation.get_recommendations_by_mood_and_location(mood, location)
        
        if recommendations:
            st.write(f"Here are some songs for your mood: '{mood}' and your location: '{location}'")
            for song in recommendations:
                st.write(f"- **{song['title']}** by {song['artist']} (Genre: {song['genre']})")
        else:
            st.write("No recommendations found for this mood.")

    if st.button("back to homepage"):
        st.session_state["current_page"] = "home"