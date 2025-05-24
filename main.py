import streamlit
from streamlit_option_menu import option_menu
import Home, Predict, Project, Chat, track

pages = {
    "home": Home,
    "predict": Predict,
    "project": Project,
    "chat": Chat,
    "track": track
} 

if "user" not in streamlit.session_state:
    streamlit.session_state.users = True

with streamlit.sidebar:
    selected = option_menu(
        "main menu", ['home', 'predict', 'project', 'chat', 'track'], 
        icons=['house', 'activity', 'graph-up-arrow', 'chat-left-text', 'card-checklist'], 
        menu_icon="clipboard-data", 
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#efffdf"},
            "menu-title": {"font-family": "Verdana", "font-weight": "bold", "color": "#077B1D"},
            "icon": {"color": "black", "font-size": "25px"}, 
            "nav-link": {"font-size": "16px", "font-family": "Verdana", "font-weight": "bold", "color": "#077B1D", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#077B1D", "color": "#f5faf9"},
        }
    )

page = pages[selected]
page.run()
