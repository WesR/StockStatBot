# StockStatBot
A bot that fetches stats about the markets.
You need an IEX and IEA key (both free for what I call, but you can pay for IEX and get better stats)

It goes into a json file in the same dir called ```apiKeys.json```.
The formatting of that json is below:
```json
{
    "discord": "THATDISCORD.APIKEYTHATHAS.TWODOTS",
    "iexDev": "Tpk_0xIEXDEVKEY_soYOUcanTestSavingCredits",
    "iex": "pk_0xIEXprodKeyForRealData",
    "iea": "IEAkey_thanksGoverment"
}

```

### Current commands:
+book <ticker>
+oil    [spot; defaults to future]
+gas    [future, retail[premium, defaults to avg]; defaults to spot]
+diesel [defaults to spot]
+ngas   [defaults to future]
+help

Example ```@get gas retail premium``` or ```@get gas ngas oil``` (my bot is named @get)
We do some extra code so the user can use the autocomplete @get or just type it and still have it called. See my weather bot to just get the code for an @ only.
