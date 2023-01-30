const messageCreate = require("../../eventos/guild/messageCreate");
const palabraModelo = require("../../schemas/palabraDiSchema");
const {EmbedBuilder} = require('discord.js');

function darFormato(cadena){
    let aMayus = cadena.replace(/[ÁÀÄÂ]/g,'A');
    let aMinus = aMayus.replace(/[áàäâ]/g,'a');
    let eMayus = aMinus.replace(/[ÉÈËÊ]/g,'E');
    let eMinus = eMayus.replace(/[éèëê]/g,'e');
    let iMayus = eMinus.replace(/[ÍÌÏÎ]/g,'I');
    let iMinus = iMayus.replace(/[íìïî]/g,'i');
    let oMayus = iMinus.replace(/[ÓÒÖÔ]/g,'O');
    let oMinus = oMayus.replace(/[óòöô]/g,'o');
    let uMayus = oMinus.replace(/[ÚÙÜÛ]/g,'U');
    let enieMinus = uMayus.replace(/[úùüû]/g,'u');
    let resultado = enieMinus.replace(/['|°¬^`~"#$%&/()Çç={}_,.<>¨*:;]/gi,'');

    return resultado;
}

module.exports = {
    name: "diagregar",
    descripcion: "Recomiendas una palabra a dominic para que con el comando di lo diga",
    async execute(client, message, argumentos, discord){
        let texto = "";
        for (const i of argumentos) { texto += i.trim() + " ";}

        let palabraReservada = texto.substring(0,texto.search("-")).toLocaleLowerCase().trim();
        palabraReservada = darFormato(palabraReservada);

        let descripcion = texto.slice(texto.search("-")+1).trim();

        if(palabraReservada.length == 0 || descripcion.length == 0) {message.reply("Recuerda que para recomendar una palabra debes usar la siguiente sintaxis:\n\n" + 
        "*dominic diagregar {palabra clave} - {lo que va a decir dominicord}*\n" +
        "> **Ejemplo:** dominic diagregar hola - hola usuario"); return;}
        //#region mensajeEmbed
        let meUser = new EmbedBuilder()
        .setColor("Grey")
        .setTitle("Palabra recomendada: " + palabraReservada)
        .setDescription("Descripción de la palabra: " + descripcion)
        .setFooter({text: `Recomendado por ${message.author.username}`, iconURL: message.author.displayAvatarURL()});    
        //#endregion
        
        //* Registrar palabra
        let palabraBuscar;
        try {
            palabraBuscar = await palabraModelo.findOne({palabra: palabraReservada});
            if(!palabraBuscar){
            let palabraRecomendada = await palabraModelo.create({
                username: message.author.username,
                profilePhoto: message.author.displayAvatarURL(),
                palabra: palabraReservada,
                descripcion: descripcion
            });
            palabraRecomendada.save();
            }
            else{
                message.reply("Ya existe una palabra con ese nombre, use otro o use dominic diEditar");
                return;
            }
        } catch (error) {
            console.log(error);
            return;
        }

        message.reply({embeds:[meUser]});
        //*

    }
}
