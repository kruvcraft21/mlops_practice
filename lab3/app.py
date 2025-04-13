import pickle
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
import streamlit as st
from bs4 import BeautifulSoup
import base64


def get_token():
    with open("key.pickle", 'rb') as file:
        token = pickle.load(file)
    return token


giga = GigaChat(
        credentials=get_token(),
        verify_ssl_certs=False
    )


def create_app():
    st.title('Преврати текст в изображение')
    st.text('Сервис предоставляет возможность генерировать изображения с помощью GigaChat😎')
    st.set_option('client.showErrorDetails', False)
    container = st.container(height=50, border=False)
    prompt = container.chat_input('Опишите изображение...', accept_file=False)
    if prompt:
        with st.spinner("Получаю изображение", show_time=True):
            response = get_response(prompt)
            try:
                image = get_image(response, prompt)
                st.image(image, caption=prompt)
                st.download_button(label='Загрузить изображение',
                                   data=image,
                                   file_name=f'{prompt}.jpeg',
                                   mime='image/jpeg',
                                   icon=':material/download:',
                                   on_click='ignore')                
            except Exception as e: pass


def get_response(prompt):
    payload = Chat(
        messages=[
            Messages(
                role=MessagesRole.USER,
                content=prompt
                )
            ],
        function_call="auto"
    )
    response = giga.chat(payload).choices[0].message.content
    print(response)
    return response


def get_image(response, prompt):
    try:
        file_id = BeautifulSoup(response, 'html.parser').find('img').get('src')
        image = giga.get_image(file_id)
        image = base64.b64decode(image.content)        
    except Exception as e:        
        st.warning(f"""Модель не смогла нарисовать изображение по вашему запросу:
                   "{prompt}".😥 Попробуйте сформулировать нейтральное описание желаемого изображения.
                   Например: \"Белая субмарина в порту\" или 
                   \"Красные розы в прозрачной пленке, перевязанные синей лентой\"""", 
                   icon='⚠️')

    return image


if __name__ == "__main__":
    create_app()