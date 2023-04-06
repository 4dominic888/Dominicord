//const {token} = require('./config.json');
const datos = require('../../config.json');
const prefix = datos.prefix;
module.exports = async(client, discord, message) => {
    if(!message.author.bot){
    if(message.content.toLowerCase().startsWith(prefix)){
    const argumentos = message.content.slice(prefix.length).trim().split(/ +/);
    const cmd = argumentos.shift().toLowerCase();
    const comando = client.comandos.get(cmd);
    if(comando) comando.execute(client, message, argumentos, discord);
    }
}}