const discord = require("discord.js");
const {Client, GatewayIntentBits, Partials, EmbedBuilder, Embed, EmbedAssertions, inlineCode} = require('discord.js');
const {token} = require('./config.json');
const datos = require('./config.json');
const client  = new discord.Client({intents: [
  GatewayIntentBits.Guilds,
  'GuildMessages',
  'MessageContent'
]});

//* Base de datos
const mongoose = require("mongoose");
const messageCreate = require("./eventos/guild/messageCreate");
mongoose.set('strictQuery', false);

mongoose.connect(datos.baseDatos,)
.then(() => {
  console.log("Conectado a la Base de Datos MongoDB");
  console.log("------------------LOGS-------------------");
}).catch((e) => {
  console.log(e);
});

//* Base de datos


client.comandos = new discord.Collection();
client.eventos = new discord.Collection();

["commandHandler", "eventHandlder"].forEach((file) => {
  require(`./handlers/${file}`)(client, discord);
});


client.login(token);