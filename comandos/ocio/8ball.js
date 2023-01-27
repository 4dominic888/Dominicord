const messageCreate = require("../../eventos/guild/messageCreate");
const {EmbedBuilder} = require('discord.js');
const IMGDominicord = "https://cdn.discordapp.com/attachments/1059093873508491326/1067640360580419654/4dominic8881.jpg";
let siNoMensajes = [
    "https://cdn.discordapp.com/attachments/1059093873508491326/1068277410774138961/image.png",
    "https://cdn.discordapp.com/attachments/1059093873508491326/1068283417768243200/image.png",
    "https://cdn.discordapp.com/attachments/1059093873508491326/1068284097581035612/image.png",
    "https://cdn.discordapp.com/attachments/1059093873508491326/1068284257748918324/image.png",
    "https://cdn.discordapp.com/attachments/1059093873508491326/1068284395657629716/image.png",
    "Yo digo que si",
    "NO",
    "Puede ser",
    "Pos esta dificil eso",
    "Confia en lo que tu crees",
    "NONONONONONONONONONONO",
    "Ni idea",
    "No sé",
    "Por supuesto",
    "mira mi huevo y dime que respuesta te da",
    "NUNCA",
    "absolutamente",
    "Sis",
    "SISISISISISISISISISISI",
    "Non",
    "Pasará de todos modos",
    "Deja veo que ha programado dominic... dice que no",
    "Deja veo que ha programado dominic... dice que si",
    "Mejor lanza una moneda y ve que te sale",
    "Anda chinga tu madre",
]

function randomNumero(mini, maxi){
    min = Math.ceil(mini);
    max = Math.floor(maxi);
    return Math.floor(Math.random() * (max - min + 1) + min);
  }

module.exports = {
    name: "8ball",
    descripcion: "Cuando hagas una pregunta, te responderá de manera binaria",
    async execute(client, message, argumentos, discord){
        let texto = " ";
        for (const i of argumentos) { texto += i.trim().toLowerCase() + " ";}
        let indice = randomNumero(0, siNoMensajes.length-1);
        console.log(indice);

        const me8ball = new EmbedBuilder()
        .setColor("Grey")
        .setTitle(texto)
        .setDescription(siNoMensajes[indice])
        .setThumbnail(IMGDominicord);


        if(texto.length <= 1){
            message.reply("Joeputa no colocaste nada");
        }
        else{
            if(indice <= 4){
                const me8ballImagen = new EmbedBuilder()
                .setColor("Grey")
                .setTitle(texto)
                .setImage(siNoMensajes[indice])
                .setThumbnail(IMGDominicord);
                message.reply({embeds: [me8ballImagen]});
            }
            else message.reply({embeds: [me8ball]});
        }

    }
}