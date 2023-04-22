const mineflayer = require('mineflayer')

// Access the command line arguments
//const args = process.argv.slice(2);

// Extract the arguments
//const num = args[0];
//const name = args[1];


const name = "Bot name"
const ip = "IP without : and port number"
const p = 25565
const ver = "minecraft version"

console.log(`Creating bot ${name} ...`);

const bot = mineflayer.createBot({
    host: ip,
    port: p,
    username: name,
    version: ver
})

bot.on('kicked', function (reason) {
    console.log(`${bot.username} is kicked for ${reason}. Trying again!`);
    bot.quit();
    bot.end();
    mineflayer.createBot({
        host: bot.host,
        port: bot.port,
        username: bot.username,
        version: bot.version
    });
});

bot.on('error', (error) => {
    console.log(error);
});

bot.on('login', () => {
    console.log(`Bot ${bot.username} has joined the server at ${ip}:${p}`);
});

bot.on('spawn', () => {
    console.log(`${bot.username} successfully connected.`);
    bot.chat('/register 123456789 123456789');
    bot.chat('/login 123456789');

    // Move forward for 3 seconds
    bot.setControlState('forward', true);
    setTimeout(() => {
        bot.setControlState('forward', false);
    }, 3000);

    // Jump
    bot.setControlState('jump', true);
    setTimeout(() => {
        bot.setControlState('jump', false);
    }, 1000);
});


//login - Fired when the bot successfully logs in to the server.
//spawn - Fired when the bot spawns in the world.
//death - Fired when the bot dies.
//health - Fired when the bot's health changes.
//chat - Fired when a player in the game chat something.
//message - Fired when the bot receives a message from another player.
//kicked - Fired when the bot is kicked from the server.
//end - Fired when the server stops or the bot is disconnected.
//blockUpdate - Fired when a block is updated in the world.
//blockBreakProgressObserved - Fired when the bot observes a block being broken by another player.
//entitySpawn - Fired when an entity spawns in the world.
//entityGone - Fired when an entity despawns from the world.
