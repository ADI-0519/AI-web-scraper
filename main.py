import streamlit as st
from scrape import scrape_website, clean_body_content, extract_body_content, split_dom_content

from parse import parse_with_ollama


st.title("AI web scraper")

url = st.text_input("Enter a website URL")

if st.button("Scrape site"):
    if url:
        st.write("Scraping...")
        result = scrape_website(url)
        body_content = extract_body_content(result)
        cleaned_content = clean_body_content(body_content)
        
        st.session_state.dom_content = cleaned_content
        
        with st.expander("View DOM content"): # button to toggle what we are showing
            st.text_area("DOM content", cleaned_content, height = 300)

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you would like to parse")
    
    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing content")

            dom_chunks = split_dom_content(st.session_state.dom_content)
            parsed_result = parse_with_ollama(dom_chunks, parse_description)
            st.write(parsed_result)


