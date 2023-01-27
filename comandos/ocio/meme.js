const messageCreate = require("../../eventos/guild/messageCreate");
const {EmbedBuilder} = require('discord.js');
const IMGDominicord = "https://cdn.discordapp.com/attachments/1059093873508491326/1067640360580419654/4dominic8881.jpg";

function randomNumero(mini, maxi){
    min = Math.ceil(mini);
    max = Math.floor(maxi);
    return Math.floor(Math.random() * (max - min + 1) + min);
  }

let listaMemes = [
    "https://cdn.discordapp.com/attachments/912817040832737304/1067841233424224256/20230125_111939.jpg",
    "https://cdn.discordapp.com/attachments/912817040832737304/1067669280973406208/819232eb67032125bafe356293ec60d4.jpg",
    "https://cdn.discordapp.com/attachments/912817040832737304/1067667494900342855/FB_IMG_16744523482500381.jpg",
    "https://cdn.discordapp.com/attachments/912817040832737304/1067667494652891206/FB_IMG_16745515586626556.jpg",
    "https://cdn.discordapp.com/attachments/912817040832737304/1067667494438969394/FB_IMG_16745522772903608.jpg",
    "https://cdn.discordapp.com/attachments/912817040832737304/1067667494233452625/FB_IMG_16745524814007514.jpg",
    "https://cdn.discordapp.com/attachments/912817040832737304/1067667493998579772/FB_IMG_16745532475101096.jpg",
    "https://cdn.discordapp.com/attachments/912817040832737304/1067667493541392475/FB_IMG_16745526594153095.jpg",
    "https://cdn.discordapp.com/attachments/912817040832737304/1067667493361045514/FB_IMG_16745951622158455.jpg"
  ]

module.exports = {
    name: "meme",
    descripcion: "Pone puros memes robados",
    async execute(client, message, argumentos, discord){
        let memeAleatorio = listaMemes[randomNumero(0, listaMemes.length - 1)];
        let meMeme = new EmbedBuilder().setColor('Grey').setTitle("Dominicord ha elegido un meme")
        .setAuthor({
          name: "Dominicord",
          iconURL: IMGDominicord
        }).setImage(memeAleatorio).setTimestamp().setFooter({text: "Dominicord", iconURL: IMGDominicord});
        message.reply({embeds:[meMeme]});
    }
}