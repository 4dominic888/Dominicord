const messageCreate = require("../../eventos/guild/messageCreate");
const baseDatosPalabrasDi= require("../../schemas/palabraDiSchema");

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
    let resultado = enieMinus.replace(/['|°¬!^`~"#$%&/()Çç=?¿{}_,.´+<>¡¨*:;]/gi,'');

    return resultado;
}

let listaPiedra = { };

module.exports = {
    name: "di",
    descripcion: "Te responde según la palabra que coloques, si no colocas nada MUERTE",
    async execute(client, message, argumentos, discord){
        let algo = baseDatosPalabrasDi.find();
        (await algo).forEach(item => { listaPiedra[item.palabra] = item.descripcion;} );

        let texto = "";
        for (const i of argumentos) { texto += i.trim().toLowerCase() + " ";}

        for (const key in listaPiedra) {
            if(texto.includes(key.toLowerCase().trim())){
                message.reply(listaPiedra[key]);
                return;
            }
        }
        message.reply("No conozco esa palabra, puedes agregarla con:\n"+
        "> *dominic diagregar {palabra clave} - {lo que va a decir dominicord}*");
    }
}