const discord = require("discord.js");
const {Client, GatewayIntentBits, Partials, EmbedBuilder, Embed, EmbedAssertions, inlineCode} = require('discord.js');
const {token} = require('./config.json');
const client  = new discord.Client({intents: [
  GatewayIntentBits.Guilds,
  'GuildMessages',
  'MessageContent'
]});

client.comandos = new discord.Collection();
client.eventos = new discord.Collection();

["commandHandler", "eventHandlder"].forEach((file) => {
  require(`./handlers/${file}`)(client, discord);
});



function randomNumero(){
  min = Math.ceil(0);
  max = Math.floor(listaMemes.length-1);
  return Math.floor(Math.random() * (max - min + 1) + min);
}

const prefix = "dominic";
const IMGDominicord = "https://cdn.discordapp.com/attachments/1059093873508491326/1067640360580419654/4dominic8881.jpg";
const meInfo = new EmbedBuilder()
  .setColor("Grey")
  .setTitle("Información de Dominicord")
  .setAuthor({
    name: "Dominicord",
    iconURL: IMGDominicord
  })
  .setDescription("Dominicord en un bot aún en desarrollo creado por 4dominic888 con ayuda de tutoriales de yt y páginas que se encuentra.")
  .setThumbnail(IMGDominicord)
  .addFields(
    {name: "ayuda", value: "Activa este comando en el cual están todos los listados de comandos."},
    {name: "hola", value: "Te saluda xd.", inline: true},
    {name: "meme", value: "Pone puros memes robados.", inline: true})
    .setImage("https://cdn.discordapp.com/attachments/1047370200045080696/1066939735764893706/FB_IMG_1628883321179.png")
    .setTimestamp()
    .setFooter({text: "Dominicord", iconURL: IMGDominicord});

/*client.on("messageCreate", (mensaje)=>{
  if(!mensaje.author.bot){
    //lista de mensajes a responder todo miedo
    
    for (const key in listaPiedra) {
        if(mensaje.content.toLowerCase().trim().includes(key.toLowerCase())){
          mensaje.reply("NO JODAN");
          return;
        }
      }
    
    


    //Mensajes de llamada
    if(mensaje.content.toLowerCase().startsWith(prefix)){
      const argumentos = mensaje.content.slice(prefix.length).trim().split(/ +/);
      const comando = argumentos.shift().toLowerCase();

      if(comando === "ayuda"){
        mensaje.reply({embeds:[meInfo]});
      }

      let memeAleatorio = listaMemes[randomNumero()];
      let meMeme = new EmbedBuilder().setColor('Grey').setTitle("Dominicord ha elegido un meme")
      .setAuthor({
        name: "Dominicord",
        iconURL: IMGDominicord
      }).setImage(memeAleatorio).setTimestamp().setFooter({text: "Dominicord", iconURL: IMGDominicord});

      if(comando === "meme"){
        mensaje.reply({embeds:[meMeme]});
      }

      if(mensaje.content.toLowerCase().includes("hola")){
        mensaje.reply("¿Qué necesitas ahora?");
        return;
      }
    }
  }
});*/

client.login(token);