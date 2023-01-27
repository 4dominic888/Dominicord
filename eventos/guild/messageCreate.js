//const {token} = require('./config.json');
const prefix = "dominic";
module.exports = async(client, discord, message) => {
    if(!message.author.bot){
    const argumentos = message.content.slice(prefix.length).trim().split(/ +/);
    const cmd = argumentos.shift().toLowerCase();

    const comando = client.comandos.get(cmd);
    if(comando) comando.execute(client, message, argumentos, discord);
}}