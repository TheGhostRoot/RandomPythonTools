const mineflayer = require('mineflayer')

console.log('host port bot_name minecraft_version amount');

const args = process.argv.slice(2);
const ip = args[0];
const p = Number(args[1]);
const bot_name = args[2];
const minecraft_version = args[3];
const amount = Number(args[4]);

const bots = [];

let i = 0;
const intervalId = setInterval(() => {
    if (i >= amount) {
        const lastBot = bots.pop();
        lastBot.quit();
        lastBot.end();
        //return;
    }

    console.log(`Creating bot ${bot_name + i.toString()} ...`);
    const bot = mineflayer.createBot({
        host: ip,
        port: p,
        username: bot_name + i.toString(),
        version: minecraft_version
    });

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
        bot.chat('/register 5716198 5716198');
        bot.chat('/login 5716198');

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

    bots.push(bot);
    i++;
}, 5000);

//intervalId.unref();  // Allow the script to exit even if the interval is still running.

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
