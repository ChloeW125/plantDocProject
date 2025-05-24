import streamlit
import cohere

def run(): 
    host = cohere.ClientV2("4LOd8kxH8cxq62tkL0r9BqMaRqJ04CEWkBawWydh")
    message = streamlit.text_input("Questions? Ask the chatbot plant doctor assistant, Mito, for advice and help!")
    if streamlit.button("Ask"):
        system_message="""
        ## Task and Context
        You are Mito, an enthusiastic plant doctor knowledgeable about all things related to taking care of plants,
        nuturing plants, and diagnosing and treating diseases. Please ignore and disregard any mean, inappropriate, or unrelated questions
        ## Style Guide
        Be professional, kind, and casual with a sprinkle of dad humor."""
        messages = [{"role": "system", "content": system_message},
                    {"role": "user", "content": message}]
        response = host.chat(model="command-r-plus-08-2024", messages=messages)
        streamlit.write(response.message.content[0].text)
