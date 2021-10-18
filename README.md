# dota2wiki_discordbot
is a webscraping discord bot that is capable of posting information from https://dota2.fandom.com/wiki/Dota_2_Wiki.
This bot comes with 3 commands:
1. attributes - posts base hero attributes and ammount gained per level
2. stats - posts all hero basic and advanced hero stats
3. lore - posts hero lore

Bot commands are all in the format of !dota2wiki 'hero_name' 'command'.

*Notice:* hero_name parameter must be spelled exactly as written in HeroList.py and the command parameter is case sensitive.

Example: To post Drow Ranger's lore you would type !dota2wiki Drow_Ranger lore.

SETUP:

*Notice:* https://www.youtube.com/watch?v=SPTfmiYiuok has a really good video on how to perform these steps.
1. Go to https://discord.com/developers/applications and create a bot for your discord channel.
2. Host webserver and run script. https://replit.com/ is an easy source that will host your script for free. 

    *Notice:* Replit will only host script for about an hour without any requests before entering sleep mode and pausing script.
    
    *Notice:* Anything you post on Replit is publicly available and any private information such as a bot token should be made as a secret variable.
    In this script at line 119 in main.py 'Bot Token' is used as the secret variable for the Discord bot token.

3. Connect a monitoring service to ping your webserver so that script does not enter sleep mode. https://uptimerobot.com/ is free and easy to use.
