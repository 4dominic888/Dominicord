const messageCreate = require("../../eventos/guild/messageCreate");
const {EmbedBuilder, ButtonBuilder, ButtonStyle, ActionRowBuilder} = require('discord.js');
const IMGDominicord = "https://cdn.discordapp.com/attachments/1059093873508491326/1067640360580419654/4dominic8881.jpg";

const filaBotones = new ActionRowBuilder()
.addComponents(
  new ButtonBuilder()
  .setCustomId("atr")
  .setLabel("⏪")
  .setStyle(ButtonStyle.Danger)
  ,
  new ButtonBuilder()
  .setCustomId("ade")
  .setLabel("⏩")
  .setStyle(ButtonStyle.Success)
);

function setFilaBotones(iterador){
  switch(iterador){
      case 0:{
          filaBotones.components[0].setDisabled(true);
          filaBotones.components[1].setDisabled(false);
          return filaBotones;
      }

      case listaMemes.length-1 :{
          filaBotones.components[0].setDisabled(false);
          filaBotones.components[1].setDisabled(true);
          return filaBotones;
      }
      
      default: {
          filaBotones.components[0].setDisabled(false);
          filaBotones.components[1].setDisabled(false);
          return filaBotones; 
      }
  }
}

function setMeme(index){
  let info = (index == listaMemes.length-1) ? " `último agregado`\n" : "\n";
  return `\`meme número ${index+1}\`` + info + listaMemes[index]
}

let listaMemes = [
    "https://cdn.discordapp.com/attachments/912817040832737304/1067841233424224256/20230125_111939.jpg",
    "https://cdn.discordapp.com/attachments/912817040832737304/1067669280973406208/819232eb67032125bafe356293ec60d4.jpg",
    "https://cdn.discordapp.com/attachments/912817040832737304/1067667494900342855/FB_IMG_16744523482500381.jpg",
    "https://cdn.discordapp.com/attachments/912817040832737304/1067667494652891206/FB_IMG_16745515586626556.jpg",
    "https://cdn.discordapp.com/attachments/912817040832737304/1067667494438969394/FB_IMG_16745522772903608.jpg",
    "https://cdn.discordapp.com/attachments/912817040832737304/1067667494233452625/FB_IMG_16745524814007514.jpg",
    "https://cdn.discordapp.com/attachments/912817040832737304/1067667493541392475/FB_IMG_16745526594153095.jpg",
    "https://cdn.discordapp.com/attachments/912817040832737304/1067667493361045514/FB_IMG_16745951622158455.jpg",
    "https://cdn.discordapp.com/attachments/1047370200045080696/1070797666692374569/GrP176q7q_VeT7fP_1.mov",
    "https://cdn.discordapp.com/attachments/1059093873508491326/1071248367784575026/eggman_chileno.mp4",
    "https://cdn.discordapp.com/attachments/1059093873508491326/1071248679102586970/image.png",
  ]

module.exports = {
    name: "meme",
    descripcion: "Pone puros memes robados",
    async execute(client, message, argumentos, discord){

      let indiceElegido = 0;
      for (const iterator of argumentos) { indiceElegido = iterator; break; }
      indiceElegido--;
      if(!(indiceElegido >= 0 && indiceElegido < listaMemes.length)){
          indiceElegido = listaMemes.length-1;
      }

      const m = await message.reply({content: setMeme(indiceElegido), components: [setFilaBotones(indiceElegido)]});
      const ifilter = i => i.user.id === message.author.id;
      const collector = m.createMessageComponentCollector({filter: ifilter, time: 200000});

        collector.on("collect", async i => {
            await i.deferUpdate()
            switch(i.customId){
                case "atr" : {
                    indiceElegido--;
                    await i.editReply({content: setMeme(indiceElegido), components: [setFilaBotones(indiceElegido)]});
                    break;
                }
                case "ade" :{
                    indiceElegido++;
                    await i.editReply({content: setMeme(indiceElegido), components: [setFilaBotones(indiceElegido)]});
                    break;
                }
                default: break;
            }
        });
    }
}