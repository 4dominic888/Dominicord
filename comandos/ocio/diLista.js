const messageCreate = require("../../eventos/guild/messageCreate");
const baseDatosPalabra = require("../../schemas/palabraDiSchema");
const {EmbedBuilder, ButtonBuilder, ButtonStyle, ActionRowBuilder} = require('discord.js');

let listaPiedra = new Array();

function setFilaBotones(iterador){
    switch(iterador){
        case 0:{
            filaBotones.components[0].setDisabled(true);
            filaBotones.components[1].setDisabled(false);
            return filaBotones;
        }

        case listaPiedra.length-1 :{
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

function textoSegunIterador(iterador){
    let texto = "";
    for (const letra of listaPiedra[iterador]) {
        texto += `> ${letra}\n`;
    }
    return texto;
}

const meListaPalabras = new EmbedBuilder()
.setColor("Grey")
.setTitle("Lista de palabras existentes")
.setDescription("wn");



module.exports = {
    name: "dilista",
    descripcion: "Te da la lista de palabras usadas",
    async execute(client, message, argumentos, discord){

        //#region Llenar listaPiedra
        listaPiedra = new Array();
        let algo = baseDatosPalabra.find();
        let longitud = (await baseDatosPalabra.find()).length;
        let firstIndexListaPiedra = 0;
        let subLista = new Array();
        (await algo).forEach(item => {
            subLista.push(item.palabra);
            if(longitud >= 10)
            {
                firstIndexListaPiedra++;
                if(firstIndexListaPiedra == 10){
                    longitud-=10;
                    listaPiedra.push(subLista);
                    firstIndexListaPiedra = 0;
                    subLista = new Array();
                }
            }
        } );
        listaPiedra.push(subLista);
        //#endregion

        let indiceElegido = 0;
        for (const iterator of argumentos) { indiceElegido = iterator; break; }
        indiceElegido--;
        if(!(indiceElegido > 0 && indiceElegido < listaPiedra.length)){
            indiceElegido = 0;
        }

        //*#region botones funciones no borrar

        meListaPalabras.setFooter({text: `Pedido por ${message.author.username}`, iconURL: message.author.displayAvatarURL()});
        meListaPalabras.setTitle(`Lista de palabras existentes pág ${indiceElegido+1} de ${listaPiedra.length}`);
        const m = await message.reply({embeds: [meListaPalabras.setDescription(textoSegunIterador(indiceElegido))], components: [setFilaBotones(indiceElegido)]});
        const ifilter = i => i.user.id === message.author.id;
        const collector = m.createMessageComponentCollector({filter: ifilter, time: 50000});

        collector.on("collect", async i => {
            await i.deferUpdate();
            switch(i.customId){
                case "atr" : {
                    indiceElegido--;
                    meListaPalabras.setDescription(textoSegunIterador(indiceElegido))
                    meListaPalabras.setTitle(`Lista de palabras existentes pág ${indiceElegido+1} de ${listaPiedra.length}`);
                    await i.editReply({embeds: [meListaPalabras], components: [setFilaBotones(indiceElegido)] });
                    break;
                }
                case "ade" :{
                    indiceElegido++;
                    meListaPalabras.setDescription(textoSegunIterador(indiceElegido))
                    meListaPalabras.setTitle(`Lista de palabras existentes pág ${indiceElegido+1} de ${listaPiedra.length}`);
                    await i.editReply({embeds: [meListaPalabras], components: [setFilaBotones(indiceElegido)] });
                    break;
                }
                default: break;
            }
        });
        //*#endregion
    }
}