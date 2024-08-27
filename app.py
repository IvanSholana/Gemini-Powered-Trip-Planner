import streamlit as st
import google.generativeai as genai
import os
import json
from gemini import Gemini
import spacy

# Set up the API key and NLP model
api_key = os.getenv("AIzaSyAwnWCj9gkgGN9v397HROgWlLzU_7M6ms0") or "AIzaSyAwnWCj9gkgGN9v397HROgWlLzU_7M6ms0"
genai.configure(api_key=api_key)  # Replace with your actual API key
nlp = spacy.load("en_core_web_sm")

# Initialize session states
if 'counter' not in st.session_state:
    st.session_state['counter'] = 0
if 'generate_button_clicked' not in st.session_state:
    st.session_state["generate_button_clicked"] = False
if 'model' not in st.session_state:
    st.session_state["model"] = None
if 'response' not in st.session_state:
    st.session_state["response"] = {}

# Main function to run the app
def main():
    session_state = st.session_state

    # Title and layout
    st.markdown(
        """
        <style>
        .title {
            text-align: center;
            color: #1E90FF; /* DodgerBlue for a fresh look */
            font-size: 3rem;
            font-weight: bold;
        }
        .subtitle {
            text-align: center;
            color: #32CD32; /* LimeGreen for a vibrant feel */
            font-size: 1.5rem;
        }
        .image {
            display: block;
            margin: 0 auto;
            width: 400px;
            border-radius: 10px;
        }
        .day-header {
            text-align: center;
            color: #1E90FF;
            font-size: 1.5rem;
            font-weight: bold;
        }
        .button {
            background-color: #32CD32;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            cursor: pointer;
            font-size: 16px;
        }
        .button:hover {
            background-color: #228B22; /* Darker green for hover effect */
        }
        .container {
            padding: 20px;
        }
        </style>
        <div class="title">
            <h1>PUNGGAWA TRAVEL 🛫</h1>
        </div>
        <div class="subtitle">
            <h3>Rencanakan perjalanan yang tak terlupakan dengan Travel Planner</h3>
        </div>
        <img src='https://i.pinimg.com/originals/20/cb/f3/20cbf31ecf279ccab1a3264a2cec80c6.jpg' 
             alt='Travel Image' class='image'>
        """, 
        unsafe_allow_html=True
    )
    st.markdown("---")

    st.sidebar.header("📋 **Trip Details**")

    # Sidebar inputs for trip details
    with st.sidebar.form("trip_form"):
        country = st.text_input("🌍 Enter the country", "Russia")
        city = st.text_input("🏙️ Enter the city", "Moscow")
        days = st.number_input("📅 For how many days?", min_value=1, value=3)
        members = st.number_input("👥 How big is your group?", min_value=1, value=1)
        generate_plan = st.form_submit_button("Generate Trip Plan 🗺️")

    if generate_plan:
        # Reset the counter and response when a new trip plan is generated
        st.session_state['counter'] = 0
        model = Gemini(city, country, days, members)
        model.get_response(markdown=False)
        st.session_state["model"] = model
        session_state["generate_button_clicked"] = True
        st.session_state["response"] = {}
        try:
            with open(r'./gemini_answer.json', 'r', encoding="utf-8") as file:
                st.session_state["response"] = json.load(file)
        except FileNotFoundError:
            st.error("Response file not found. Please ensure the correct path and file name.")

    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col2:
        response = st.session_state.get("response", {})
        current_day = f"Day {st.session_state['counter'] + 1}"
        st.markdown(f"<h3 class='day-header'>{current_day} 📅</h3>", unsafe_allow_html=True)

        model = st.session_state.get("model")
        
        current_day_infos = st.empty()
        
        if model is not None:
            if current_day in response:
                info = "".join([f"**{key}**: {value}\n" for key, value in response[current_day].items()])
                current_day_infos.write(model.to_markdown(info))
            else:
                current_day_infos.write("Generate a Trip Plan to see the details here! ✨")

        st.markdown("---")
        
        if st.button("Next Day ➡️", help="Click to view the plan for the next day."):
            if st.session_state['counter'] < len(response) - 1:
                st.session_state['counter'] += 1
                current_day = f"Day {st.session_state['counter'] + 1}"
                if current_day in response:
                    current_day_infos.empty()
                    info = "".join([f"**{key}**: {value.strip()}\n" for key, value in response[current_day].items()])
                    current_day_infos.write(model.to_markdown(info))
                else:
                    current_day_infos.empty()
                    current_day_infos.write("No information available for this day. 🛑")

if __name__ == '__main__':
    main()
