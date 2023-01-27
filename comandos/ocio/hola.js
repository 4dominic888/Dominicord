const messageCreate = require("../../eventos/guild/messageCreate");

module.exports = {
    name: "hola",
    descripcion: "Te saluda",
    async execute(client, message, argumentos, discord){
        message.reply("¿Qué necesitas ahora?");
    }
}