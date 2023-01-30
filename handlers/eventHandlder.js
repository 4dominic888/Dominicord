const fs = require("fs");

module.exports = (client, discord) => {
    console.log("-----------------Eventos-------------------------")

    fs.readdirSync("./eventos/").forEach((dir) => {
        const events = fs.readdirSync(`./eventos/${dir}`);/*filter((file) => {file.endsWith(".js")});*/
        events.forEach(file => {if(!file.endsWith(".js")) events.shift()});
        console.log(events);
        for (const file of events) {
            try {
                let evn = require(`../eventos/${dir}/${file}`);
                if(evn.events && typeof evn.events !== "string"){
                    continue;
                }
                evn.events = evn.events || file.replace(".js","");
                client.on(evn.events, evn.bind(null, client, discord));
            } catch (error) {
                console.log("Error en la carga de eventos:\n" + error);
                }
            }
        
    });

    console.log("---------------------------------------------------")
}