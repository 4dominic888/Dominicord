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
    name: "dieditar",
    descripcion: "Editas una palabra ya existente",
    async execute(client, message, argumentos, discord){
        let texto = "";
        for (const i of argumentos) { texto += i.trim() + " ";}

        let palabraReservada = texto.substring(0,texto.search("-")).toLocaleLowerCase().trim();
        palabraReservada = darFormato(palabraReservada);

        let descripcion = texto.slice(texto.search("-")+1).trim();

        if(palabraReservada.length == 0 || descripcion.length == 0) {message.reply("Recuerda que para editar una palabra debes usar la siguiente sintaxis:\n\n" + 
        "*dominic diEditar {palabra clave} - {lo que va a decir dominicord}*\n" +
        "> **Ejemplo:** dominic dieditar hola - hola usuario\n\n*Solo funciona si la palabra ya ha sido creada*"); return;}
        //#region mensajeEmbed
        let meUser = new EmbedBuilder()
        .setColor("Grey")
        .setTitle("Palabra recomendada: " + palabraReservada)
        .setDescription("Descripción de la palabra: " + descripcion)
        .setFooter({text: `Editado por ${message.author.username}`, iconURL: message.author.displayAvatarURL()});    
        //#endregion
        
        //* Registrar palabra
        let palabraBuscar;
        try {
            palabraBuscar = await palabraModelo.findOne({palabra: palabraReservada});
            if(palabraBuscar){
                await palabraModelo.updateOne({ palabra: palabraReservada},{
                    $set : {
                        username: message.author.username,
                        profilePhoto: message.author.displayAvatarURL(),
                        descripcion: descripcion
                        }
                });
            }
            else{
                message.reply("Esta palabra no ha sido creada aún, intente crearla con dominic diAgregar");
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
