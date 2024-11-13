import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="CHIKty",
    page_icon="/Users/luli/AP/My proyecto/img/Captura de pantalla 2024-10-21 a la(s) 10.56.32 p. m-Photoroom.png",
    layout="centered",
    initial_sidebar_state="expanded",)
st.subheader("Bienvenidx!")
st.write("¡Descubre el potencial ilimitado de la IA con CHIK.IA ahora!")
st.write("Habla con el chatbot de IA sobre cualquier tema")
nombre = st.text_input("Cuál es tu nombre?")

left, middle, right = st.columns(3)
if left.button("Saludo", icon="👋", use_container_width=True):
    left.markdown(f"chik.AI: Hola {nombre}, como puedo ayudarte hoy?")
elif middle.button("La temperatura de hoy?", icon="🌤️", use_container_width=True):
    middle.markdown("chik.AI: La temperatura mínima de hoy es 21° y máxima 21°")
elif right.button("Random", icon="🎲", use_container_width=True):
    right.markdown("chik.AI: El primer producto vendido en Internet fue una pizza. El mérito se lo llevó Pizza Hut, que vendió su primera pizza 'online' en 1994!")
elif st.button("Salir", type="primary"):
    st.text(f"Nos vemos! {nombre}")

modelo = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

def crear_usuarioGroq():
    claveSecreta = st.secrets["Clave_API"]
    return Groq(api_key=claveSecreta)

def configurarModeloIA(cliente, modeloSeleccionado, mensajeEntrada):
    return cliente.chat.completions.create(
        messages=[{"role": "system", "content": "mensajesys"}, {"role": "user", "content": mensajeEntrada}],
        model=modeloSeleccionado,
        stream=True,
    )

def inicializarEstado():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

def configuracion():
    st.sidebar.balloons()
    st.sidebar.image('/Users/luli/AP/My proyecto/img/image (2)-1.png', width=200)
    st.sidebar.title("Menú")
    elegirmodelo = st.sidebar.selectbox(
        "Modelo",
        modelo,
        index=2
    )
    if st.sidebar.button("Descargar la APP", type='secondary', icon= '🐚'):
        st.sidebar.write("(*Link de descarga*)")
    if st.sidebar.button("Sobre nosotros", type='secondary', icon= '🏖️'):
        st.sidebar.write("Somos un chatbot completamente gratis y libre, con respuestas amplias en muchos temas!")
    return elegirmodelo

def actualizaHistorial(rol, contenido, avatar):
    st.session_state["messages"].append(
        {"role": rol, "content": contenido, "avatar": avatar}
    )

def mostrarHistorial():
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"], avatar=message.get("avatar", "default_avatar.png")):
            st.markdown(message["content"])

def areachat():
    contenedorDelChat = st.container(height=400, border=True)
    with contenedorDelChat:
        mostrarHistorial()

def generarRespuesta(chatCompleto):
    respuestaCompleta = ""
    if not chatCompleto:
        return "Error: No se pudo obtener el chat completo."
    for frase in chatCompleto:
        if hasattr(frase, 'choices') and len(frase.choices) > 0 and hasattr(frase.choices[0], 'delta'):
            contenido = getattr(frase.choices[0].delta, "content", "")
            if contenido:
                respuestaCompleta += contenido
                yield contenido
            else:
                yield "Error: No hay contenido disponible en la respuesta."
        else:
            yield "Error: No se encontró una estructura válida en la respuesta."
    return respuestaCompleta

def main():
    modeloSeleccionado = configuracion()
    clienteUsuario = crear_usuarioGroq()
    inicializarEstado()
    areachat()
    mensaje = st.chat_input("Escribí un mensaje...")
    chatCompleto = None
    if mensaje:
        actualizaHistorial(rol=nombre, contenido=mensaje, avatar="🏄🏼‍♂️")
        chatCompleto = configurarModeloIA(clienteUsuario, modeloSeleccionado, mensaje)
    if chatCompleto:
        with st.chat_message("assistant"):
            respuestaCompleta = st.write_stream(generarRespuesta(chatCompleto))
            actualizaHistorial("assistant", contenido=respuestaCompleta, avatar="🤖")
            st.rerun()

if __name__ == "__main__":
    main()