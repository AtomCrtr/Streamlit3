import streamlit as st
import pandas as pd
from streamlit_authenticator import Authenticate
from streamlit_option_menu import option_menu
import requests

csv_url = "https://raw.githubusercontent.com/AtomCrtr/Streamlit3/refs/heads/main/users.csv"

#Code Alex
# Télécharger le CSV et charger dans un DataFrame
response = requests.get(csv_url)
if response.status_code == 200:
    with open("temp.csv", "wb") as file:
        file.write(response.content)
    # Charger le fichier CSV en DataFrame
    df = pd.read_csv("temp.csv")


required_columns = ['name', 'password', 'email', 'failed_login_attempts', 'logged_in', 'role']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    st.error(f"Colonnes manquantes dans le fichier CSV : {missing_columns}")
else:
    df['logged_in'] = df['logged_in'].astype(bool)
    df['failed_login_attempts'] = df['failed_login_attempts'].astype(int)
    
    lesDonneesDesComptes = {
        'usernames': {
            row['name']: {
                'name': row['name'],
                'password': row['password'],
                'email': row['email'],
                'failed_login_attempts': row['failed_login_attempts'],
                'logged_in': row['logged_in'],
                'role': row['role']
            }
            for _, row in df.iterrows()
        }
    }

    authenticator = Authenticate(
        lesDonneesDesComptes,
        "cookie_name",
        "cookie_key",
        30
    )

    authenticator.login()

    def accueil():
        st.title("Bienvenue les Gadjos !")

    def album_photo():
        st.title("Ou est mon chat ?")
        images = [
            {"title": "Photo 1", "url": "https://www.demotivateur.fr/images-buzz/190498/13714059_311271969205288_1183699015_n.jpg"},
            {"title": "Photo 2", "url": "https://sevetys.fr/_next/image/?url=https%3A%2F%2Fcharming-angel-5ca83bf286.media.strapiapp.com%2FMaine_Coon_62b7c10518.webp&w=3840&q=75"},
            {"title": "Photo 3", "url": "https://maine-coon-elevage.com/wp-content/uploads/2023/03/Maine-Coon-Black-Smoke-XXL-geant-Tommy-chatterie-Makatea-Maine-Coon.jpg"},
            {"title": "Photo 4", "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR8JjeJy3Ckw8PHBI-FfdO8G3UXnLOA2CKu-lMOaaJnrwQEa__kJgJOZcPX0KNRIK4WcCk&usqp=CAU"},
            {"title": "Photo 5", "url": "https://www.ranchdaska.fr/media/breeder/801/breeding/le-ranch-de-daska/animal/maine-coon-polydactyle-tany/photos/57533/chaton-maine-coon-polydactyle-black-silver-blotched-tabby-tany-le-ranch-de-daska-15.png"},
            {"title": "Photo 6", "url": "https://www.coondesabyss.com/images/Black.jpg"},
        ]
        for i in range(0, len(images), 3):
            cols = st.columns(3)
            for col, image in zip(cols, images[i:i + 3]):
                with col:
                    st.header(image["title"])
                    st.image(image["url"])

    if "authentication_status" not in st.session_state:
        st.session_state["authentication_status"] = None

    if "username" not in st.session_state:
        st.session_state["username"] = ""

    if st.session_state["authentication_status"]:
        with st.sidebar:
            selection = option_menu(
                menu_title=None,
                options=["Accueil", "Album Photo"]
            )
            st.write(f"Bienvenue {st.session_state['username']}")
            authenticator.logout("Déconnexion")

        if selection == "Accueil":
            accueil()
        elif selection == "Album Photo":
            album_photo()

    elif st.session_state["authentication_status"] is False:
        st.error("L'username ou le password est/sont incorrect")
    elif st.session_state["authentication_status"] is None:
        st.warning("Les champs username et mot de passe doivent être remplis")