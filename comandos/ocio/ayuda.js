const messageCreate = require("../../eventos/guild/messageCreate");
const {EmbedBuilder} = require('discord.js');
const IMGDominicord = "https://cdn.discordapp.com/attachments/1059093873508491326/1067640360580419654/4dominic8881.jpg";
//#region meInfo
    const meInfo = new EmbedBuilder()
        .setColor("Grey")
        .setTitle("Información de Dominicord")
        .setAuthor({
        name: "Dominicord",
        iconURL: IMGDominicord
    })
    .setDescription("Dominicord en un bot aún en desarrollo creado por 4dominic888 con ayuda de tutoriales de yt y páginas que se encuentra.")
    .setThumbnail(IMGDominicord)
    .addFields(
        {name: "Lista de comandos", value: "coloca dominic ayuda {nombre del comando} para saber su información\n" + 
        "> **hola**\n" +
        "> **di**\n" + 
        "> **8ball**\n" + 
        "> **meme**\n\n" + 
        "*Ejemplo: dominic ayuda meme*"},
        )
    .setImage("https://cdn.discordapp.com/attachments/1047370200045080696/1066939735764893706/FB_IMG_1628883321179.png")
    .setTimestamp()
    .setFooter({text: "Dominicord", iconURL: IMGDominicord});
//#endregion
let ayudaComandos = {
    "Hola" : "Te saluda el bot, no tiene mucha historia este comando.",
    "Meme" : "Te manda puro meme robado.\n**Variaciones**: MemeAgregar\n*Estas variaciones tienen su propio comando ayuda*",
    "MemeAgregar" : "Agregas memes para que el bot siga almacenandolos por la eternidad... supongo",
    "DiAgregar" : "Recomiendas una palabra a dominic para que con el comando \"di\" lo diga",
    "DiEditar" : "Editas una palabra a dominic para que con el comando \"di\" lo diga",
    "DiLista" : "Te muestra la lista de las palabras agregadas",
    "Di"   : "coloca \"dominic di {texto}\", te pondrá una mamada o dirá que no sabe como responder.\n" + 
             "**Variaciones:**: DiAgregar, **DiEditar**, **DiLista**\n" + 
             "*Estas variaciones tienen su propio comando ayuda*",
    "8ball" : "Si tienes una pregunta, la haces y te responderá. Solo se admiten preguntas binarias de si y no",
}

module.exports = {
    name: "ayuda",
    descripcion: "Activa este comando en el cual están todos los listados de comandos.",
    async execute(client, message, argumentos, discord){
        let texto = "";
        for (const i of argumentos) { texto += i.trim().toLowerCase() + " ";}
        for (const key in ayudaComandos) {
            if(texto.includes(key.toLowerCase().trim())){
                const meAyuda = new EmbedBuilder()
                .setColor("Grey")
                .setTitle(key)
                .setDescription(ayudaComandos[key])
                .setThumbnail(IMGDominicord);

                message.reply({embeds:[meAyuda]});
                return;
            }
        }
        message.reply({embeds:[meInfo]});
    }
}