import requests
import asyncio
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from HeroList import listOfHeroes
from replit import db
from keep_alive import keep_alive


# call dota2, hero specific, wiki page and parse into html
def requestAndParseHero(heroName):
    r = requests.get("https://dota2.fandom.com/wiki/" + heroName)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    return soup


def requestAndParseLore(heroName):
    r = requests.get("https://dota2.fandom.com/wiki/" + heroName + "/Lore")
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    return soup


client = commands.Bot(command_prefix='!')
loop = asyncio.get_event_loop()
data = asyncio.Queue()


@client.event
async def on_ready():
    print('Bot is ready.')


@client.command()
async def dota2wiki(ctx, hero, infoType):
    if hero in listOfHeroes and infoType == 'attributes':
        dota2Wiki = requestAndParseHero(hero)
        # Locate base attributes and then print them
        # 1. Locate attributes
        table = dota2Wiki.find("a", title="Strength")
        tableHelp = table.parent
        attributes = tableHelp.find_next_siblings("div")
        # 2. Print attributes
        await ctx.send("Strength = " + attributes[2].text)
        await ctx.send("Agility = " + attributes[3].text)
        await ctx.send("Intelligence = " + attributes[4].text)
    # Locate stats and then print them
    if hero in listOfHeroes and infoType == 'stats':
        # 1. Locate stats
        dota2Wiki = requestAndParseHero(hero)
        table1 = dota2Wiki.find("table", {"class": "evenrowsgray"})
        table2 = dota2Wiki.find("table", {"class": "oddrowsgray"})
        statsTable1 = table1.find_all("tr")
        statsTable2 = table2.find_all("td")
        healthTable = statsTable1[1].find_all("td")
        healthRegenTable = statsTable1[2].find_all("td")
        manaTable = statsTable1[3].find_all("td")
        manaRegenTable = statsTable1[4].find_all("td")
        armorTable = statsTable1[5].find_all("td")
        attsecTable = statsTable1[6].find_all("td")
        damageTable = statsTable1[7].find_all("td")
        # 2. Prints stats
        await ctx.send("BASE STATS:")
        await ctx.send("Health: " + healthTable[1].text.replace("\n", ""))
        await ctx.send("Health regen: " + healthRegenTable[1].text.replace("\n", ""))
        await ctx.send("Mana: " + manaTable[1].text.replace("\n", ""))
        await ctx.send("Mana regen: " + manaRegenTable[1].text.replace("\n", ""))
        await ctx.send("Armor: " + armorTable[1].text.replace("\n", ""))
        await ctx.send("Att/sec: " + attsecTable[1].text.replace("\n", ""))
        await ctx.send("Damage: " + damageTable[1].text.replace("\n", ""))
        await ctx.send("Magic resistance: " + statsTable2[0].text.replace("\n", ""))
        await ctx.send("Movement speed: " + statsTable2[1].text)
        await ctx.send("ADVANCED STATS:")
        await ctx.send("Attack speed: " + statsTable2[2].text.replace("\n", ""))
        await ctx.send("Turn rate: " + statsTable2[3].text.replace("\n", ""))
        await ctx.send("Vision range: " + statsTable2[4].text.replace("\n", ""))
        await ctx.send("Attack range: " + statsTable2[5].text.replace("\n", ""))
        await ctx.send("Projectile speed: " + statsTable2[6].text.replace("\n", ""))
        await ctx.send("Attack animation: " + statsTable2[7].text.replace("\n", ""))
        await ctx.send("Base attack time: " + statsTable2[8].text.replace("\n", ""))
        await ctx.send("Damage block: " + statsTable2[9].text.replace("\n", ""))
        await ctx.send("Collision size: " + statsTable2[10].text.replace("\n", ""))
        await ctx.send("Legs: " + statsTable2[11].text.replace("\n", ""))
        await ctx.send("Gib type: " + statsTable2[12].text.replace("\n", ""))
    # Locate lore and print it
    if hero in listOfHeroes and infoType == 'lore':
        dota2Wiki = requestAndParseLore(hero)
        # 1. Locate lore title and print
        loreTitle = dota2Wiki.find("div", {"style": "font-weight:bold;"})
        await ctx.send(loreTitle.text)
        # 2. Convert br tags to \n to simplify string manipulation later on
        for br in dota2Wiki.find_all("br"):
            br.replace_with("\n")
        # 3. Locate lore
        loreHelper = dota2Wiki.find("div", {"style": "font-style:italic; font-size:13px;"})
        lore = loreHelper.text
        # 4. Print lore
        intHelper = 0
        # After converting br tags to /n there will be 2 /n values in a row after each paragraph.
        # This will cause the for loop to crash when trying to print between both of these /n values.
        #skipHelper will skip the second /n value so that the for loop runs properly.
        #skipHelper is initialized to 99999999 as an arbitrarily high number so that it is not reached in the loop
        #before needing to be used.
        skipHelper = 99999999
        for x in range(len(lore)):
            if x == skipHelper:
                continue
            if lore[x] == "\n":
                skipHelper = x + 1
                await ctx.send(lore[intHelper:x + 1])
                intHelper = x

        await ctx.send(lore[intHelper:])


keep_alive()
client.run('Bot Token')
