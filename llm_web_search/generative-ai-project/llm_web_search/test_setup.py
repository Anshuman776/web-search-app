import streamlit as st
import os
import requests
from dotenv import load_dotenv

# Page configuration
st.set_page_config(
    page_title="Web Search",
    page_icon="🔍",
    layout="wide"
)

# Replace environment variables with Streamlit secrets
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]

def search_web(query):
    """Perform web search using Serper API"""
    try:
        url = "https://google.serper.dev/search"
        headers = {
            'X-API-KEY': SERPER_API_KEY,
            'Content-Type': 'application/json'
        }
        params = {'q': query}
        
        response = requests.get(url, headers=headers, params=params)
        results = response.json()
        
        return results.get('organic', [])
    except Exception as e:
        st.error(f"Search error: {str(e)}")
        return []

# Search interface
st.title("🔍 A3 Search")
query = st.text_input("Search:", placeholder="Enter your search query")

if st.button("Search"):
    if query:
        with st.spinner("Searching..."):
            results = search_web(query)
            
            if results:
                st.success(f"Found {len(results)} results")
                
                for result in results:
                    st.write("---")
                    title = result.get('title', 'No Title')
                    link = result.get('link', '#')
                    snippet = result.get('snippet', 'No description available')
                    
                    st.markdown(f"### [{title}]({link})")
                    st.write(snippet)
                    st.markdown(f"🔗 `{link}`")
            else:
                st.error("No results found")
    else:
        st.warning("Please enter a search query")


