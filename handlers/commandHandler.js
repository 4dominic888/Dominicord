const fs = require("fs");

module.exports = (client, discord) => {
    console.log("-----------------Commandos-------------------------")
    fs.readdirSync("./comandos/").forEach((dir) => {
        const commands = fs.readdirSync(`./comandos/${dir}`);/*.filter((file) => {file.endsWith(".js");});*/
        commands.forEach(file =>{if(!file.endsWith(".js")) commands.shift()});
        console.log(commands);
        for (const file of commands) {
            const cmd = require(`../comandos/${dir}/${file}`);
            if(cmd.name){
                client.comandos.set(cmd.name, cmd);
            }
            else{
                console.log(`Error: ${cmd.name}`)
            }
        }
    });
    console.log("---------------------------------------------------")
};