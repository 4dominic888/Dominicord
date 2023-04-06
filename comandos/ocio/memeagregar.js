const messageCreate = require("../../eventos/guild/messageCreate");
const memesDB = require("../../schemas/memeSchema");
const {EmbedBuilder, ButtonBuilder, ButtonStyle, ActionRowBuilder} = require('discord.js');
const IMGDominicord = "https://cdn.discordapp.com/attachments/1059093873508491326/1067640360580419654/4dominic8881.jpg";

//https://cdn.discordapp.com/attachments/1047370200045080696/1070797666692374569/GrP176q7q_VeT7fP_1.mov

module.exports = {
    name: "memeagregar",
    descripcion: "Agregas memes todo feos",
    async execute(client, message, argumentos, discord){
        let URLMeme = "";
        for (const iterator of argumentos) {URLMeme = iterator; break}
        let imagen = "";
        let nombre = "";
        try {
            imagen = message.attachments.first().url;
            nombre = message.attachments.first().name;
        } catch (error) {
            if(error instanceof TypeError){
                message.reply("Al parecer no has colocado un meme o video, intentalo de esta forma\n" + 
                "https://cdn.discordapp.com/attachments/1059093873508491326/1071263609390387231/MemeAgregarExample.gif");
                return;
            }
        }

        let memeExistente;
        try {
            memeExistente = await memesDB.findOne({memeURL: imagen});
            if(!memeExistente){
                let momazoEnviado = await memesDB.create({
                    username: message.author.username,
                    memeURL: imagen,
                    memeName: nombre
                });
            momazoEnviado.save();
            }
            else{
                message.reply("Parece que este meme ya está registrado");
            }
        } catch (error) {
            console.log(error);
        }

        let meAgregadoMeme = new EmbedBuilder()
        .setColor("Grey")
        .setTitle("Meme enviado, espera a que dominic lo agrege 👍")
        .setDescription(`${nombre}`)
        .setFooter({text: `Recomendado por ${message.author.username}`, iconURL: message.author.displayAvatarURL()});

        message.reply({embeds: [meAgregadoMeme]});
    }
}