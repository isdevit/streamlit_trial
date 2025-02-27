import streamlit as st
import requests
from datetime import datetime
import time
from streamlit_image_comparison import image_comparison


NASA_API_KEY = "" 

st.set_page_config("Hubble vs Webb & Live Feed", "🔭")

st.header("🔭 Hubble vs Webb Telescope & Live Observations")

#function to get latest Hubble image from NASA's APOD API
def get_nasa_apod():
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&count=10"  
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching NASA APOD data: {e}")
        return None

#Function to get Hubble live feed (if available)
def get_hubble_live():
    hubble_live_url = "https://hubblesite.org/api/v3/live"  #Hubble live API
    try:
        response = requests.get(hubble_live_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching Hubble live data: {e}")
        return None

#📡 **Hubble Live Feed**
st.subheader("📡 Hubble Live Feed")

hubble_data = get_hubble_live()

if hubble_data:
    target_name = hubble_data.get("target", "Unknown Object")
    image_url = hubble_data.get("image", "")
    observation_time = hubble_data.get("timestamp", "")

    # Convert timestamp to readable format
    if observation_time:
        observation_time = datetime.utcfromtimestamp(observation_time).strftime("%Y-%m-%d %H:%M:%S UTC")

    st.markdown(f"### Currently Observing: {target_name}")
    if image_url:
        st.image(image_url, caption=f"Hubble's Live View - {target_name}", use_container_width=True)
    st.markdown(f"📅 **Observation Time:** {observation_time}")
else:
    st.warning("Hubble live feed is currently unavailable.")

# 🛰️ **Latest NASA Space Images**
st.subheader("🛰️ Latest NASA Space Images")

nasa_images = get_nasa_apod()

if nasa_images:
    for img_data in nasa_images:
        title = img_data.get("title", "Unknown Observation")
        image_url = img_data.get("url", "")
        explanation = img_data.get("explanation", "No details available.")
        date = img_data.get("date", "")

        st.markdown(f"### {title}")
        if image_url:
            st.image(image_url, caption=f"{title} ({date})", use_container_width=True)
        st.markdown(f"📅 **Observation Date:** {date}")
        st.markdown(f"📝 **Description:** {explanation}")
        st.write("---")

# 🔭 **Hubble vs Webb Telescope Image Comparison**
st.subheader("🔭 Hubble vs Webb Telescope Comparison")

comparisons = [
    {
        "title": "Southern Ring Nebula",
        "hubble": "https://www.webbcompare.com/img/hubble/southern_nebula_700.jpg",
        "webb": "https://www.webbcompare.com/img/webb/southern_nebula_700.jpg"
    },
    {
        "title": "Galaxy Cluster SMACS 0723",
        "hubble": "https://www.webbcompare.com/img/hubble/deep_field_700.jpg",
        "webb": "https://www.webbcompare.com/img/webb/deep_field_700.jpg"
    },
    {
        "title": "Carina Nebula",
        "hubble": "https://www.webbcompare.com/img/hubble/carina_2800.png",
        "webb": "https://www.webbcompare.com/img/webb/carina_2800.jpg"
    },
    {
        "title": "Stephan's Quintet",
        "hubble": "https://www.webbcompare.com/img/hubble/stephans_quintet_2800.jpg",
        "webb": "https://www.webbcompare.com/img/webb/stephans_quintet_2800.jpg"
    }
]

for comp in comparisons:
    st.markdown(f"### {comp['title']}")
    image_comparison(
        img1=comp["hubble"],
        img2=comp["webb"],
        label1="Hubble",
        label2="Webb"
    )

# Auto-refresh every 60 seconds
time.sleep(60)
st.experimental_rerun()
