const mensaje = document.getElementById('prompt');
const buttom = document.getElementById('enviar');
const chat = document.getElementById('zona-chat');



function enviarPrompt(){
    const pregunta = document.createElement('p');
    const text = mensaje.value;
    pregunta.innerText = text;
    chat.append(pregunta); //Podemos usar tambien append.child, pero este solo acepta texto html
    //Ademas, al usar appendChild, te devuelve el texto insertado. Al usar append, no te devuelve nada
    mensaje.value = ""; mensaje.focus();

    //Ahora enviaremos el mensaje al backend

    fetch('http://127.0.0.1:8000/realizar-pregunta', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            contenido: text
        })
    })
    .then(answer => answer.json())
    .then(ansStr => {
        const ans = document.createElement('p');
        ans.innerText = ansStr.mensaje;
        chat.append(ans);
        console.log(ansStr.auth);
    })
    .catch(error => {
        console.error("Hubo un problema: ", error);
    })
}


buttom.addEventListener('click', enviarPrompt)

mensaje.addEventListener('keydown', (tecla) => {
    if(tecla.key === "Enter"){
        if(tecla.shiftKey || mensaje.value === "")
            return;
        tecla.preventDefault();

        enviarPrompt();
    }
})