import discord
import json, requests
from datetime import datetime

client = discord.Client()
#url = "https://sandbox.iexapis.com/stable" #dev
url = "https://cloud-sse.iexapis.com/stable" # prod
url_iea = "https://api.eia.gov/" # U.S. Energy Information Administration

#Where we store the API keys
class globalVars:
    def __init__(self, apiKeys = dict()):
        self.apiKeys = apiKeys

def loadKeys():
    #Loads two api keys under the values discord and iex
    with open('apiKeys.json') as data:    
        globalVars.apiKeys = json.load(data)
    print("Loaded API keys")

#Using requests to get json from IEX
def httpGETJSON(endpoint = "", query = ""):
    return requests.get(url + endpoint + "?token=" + globalVars.apiKeys["iex"] + query).json() 
    #return json.loads('{"YELP":{"bids":[{"price":63.09,"size":300,"timestamp":1494538496261}],"asks":[{"price":63.92,"size":300,"timestamp":1494538381896},{"price":63.97,"size":300,"timestamp":1494538381885}]}}')

#get json from IEA
def httpGETJSON_iea(endpoint = "", query = ""):
    return requests.get(url_iea + endpoint + "?api_key=" + globalVars.apiKeys["iea"] + query).json() 

#Get the outstanding orders on the book for a given stock or index
def getBook(ticker):
    resp = httpGETJSON("/deep/book", "&symbols=" + ticker)
    
    if not resp:
        return "symbol not found"

    output = "BID\n"
    for x in resp[ticker.upper()]['bids']:
        output+= datetime.utcfromtimestamp(x['timestamp']/1000).strftime('%H:%M:%S') + " - $" + str(x['price']) + " x " + str(x['size']) +"\n"
    
    output+= "============\nASK\n"
    for x in resp[ticker.upper()]['asks']:
        output+= datetime.utcfromtimestamp(x['timestamp']/1000).strftime('%H:%M:%S') + " - $" + str(x['price']) + " x " + str(x['size']) +"\n"
    
    #print(output)
    return output

#Get the current commoditie (oil, corn, etc) price
def getCommoditiesDaily(ticker):
    resp = httpGETJSON_iea("/series/", "&series_id=" + ticker)
    #resp = httpGETJSON("/time-series/energy/"+ ticker)[0]

    output = resp['series'][0]['name']+ "\n"
    output += str(resp['series'][0]['data'][0][1]) + " @ " + datetime.strptime(resp['series'][0]['data'][0][0], '%Y%m%d').strftime('%m/%d')

    return output
    #return 'Oil is ' + str(resp['value']) + ' as of ' + datetime.utcfromtimestamp(resp['updated']/1000).strftime('%H:%M:%S')

#halp
def help():
    message = "Commands:\n"
    message+= "```+book <ticker>\n"
    message+= "+oil    [spot; defaults to future]\n"
    message+= "+gas    [future, retail[premium, defaults to avg]; defaults to spot]\n"
    message+= "+diesel [defaults to spot]\n"
    message+= "+ngas   [defaults to future]\n"
    message+= "+help```"
    return message

@client.event
async def on_ready():
    print("Online") #so we know client side
    await client.change_presence(activity=discord.Game(name='Running Numbers'))#so the server knows whats up


#The way I do commands is nonridged and allows for cool chaining. This does require some thought on when you run specific thing though
@client.event
async def on_message(message):
    #print(message.content)
    if message.content.startswith('<@!' + str(client.user.id) + ">") or message.content.startswith('<@' + str(client.user.id) + ">"):#So we get with and without the ! (because we want without autocomplete)
        message.channel.typing()# this doesnt work. I'll eventually put the good code from another bot here
        if message.content.startswith('<@!' + str(client.user.id) + ">"):#we gotta split diffrently because of the bang
            command = message.content.split('<@!' + str(client.user.id) + ">")[1].strip().rstrip().lower()
        else:
            command = message.content.split('<@' + str(client.user.id) + ">")[1].strip().rstrip().lower()
        if 'help' in command:
            await message.channel.send(help())
        if 'book' in command:
            ticker = message.content.split("book")[1].strip().rstrip().lower()
            print("book "+ ticker)
            await message.channel.send(getBook(ticker))
        if 'oil' in command:
            if 'spot' in command:
                print("oil spot price")
                await message.channel.send(getCommoditiesDaily('PET.RWTC.D'))
            else:
                print("oil future price")
                await message.channel.send(getCommoditiesDaily('PET.RCLC1.D'))
        if ' gas' in " " + command:#We add the space so we dont get natural gas. Its kinda a cheap trick
            if 'future' in command:
                print("gas reformulated future price")#note, out api doesnt have futures for regular
                await message.channel.send(getCommoditiesDaily('PET.EER_EPMRR_PE1_Y35NY_DPG.D'))
            elif 'retail' in command:
                if 'premium' in command:
                    print('Premium Retail Gasoline Prices')#all formulations, weekly, east coast
                    await message.channel.send(getCommoditiesDaily('PET.EMM_EPMP_PTE_R1Y_DPG.W'))
                else:
                    print('Retail Gasoline Prices')#all formulations, weekly, east coast
                    await message.channel.send(getCommoditiesDaily('PET.EMM_EPM0_PTE_R1Y_DPG.W'))
            else:
                print("gas spot price")
                await message.channel.send(getCommoditiesDaily('PET.EER_EPMRU_PF4_Y35NY_DPG.D'))
        if 'diesel' in command:
            print("diesel spot price")
            await message.channel.send(getCommoditiesDaily('PET.EER_EPD2DXL0_PF4_Y35NY_DPG.D'))
        if 'ngas' in command:
            print("natural gas future price")
            await message.channel.send(getCommoditiesDaily('NG.RNGC1.D'))


def main():
    client.run(globalVars.apiKeys['discord'])

if __name__ == '__main__':
    loadKeys()
    main()