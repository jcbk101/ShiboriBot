import Constants as Keys

from bscscan import BscScan
from decimal import Decimal
from pythonpancakes import PancakeSwapAPI


# -----------------------------------------
#
# Return the value from BSCSCAN decreased
# by the decimal size
#
# -----------------------------------------
def get_decimal_value(number, decimals):
    factor = Decimal("10") ** Decimal("-{}".format(decimals))
    return Decimal(number) * factor


def get_ticker_value(number, decimals):
    factor = Decimal("10") ** Decimal("+{}".format(decimals))
    return Decimal(number) * factor


# -----------------------------------------
#
# Trim long numbers down for better
# formatting
#
# -----------------------------------------
def Shrink(number, isDecimal):
    numLevels = [ '', 'K', 'M', 'B', 'T', 'Q', 'QUINT', 'SEXT', 'SEPT' ]
    value = int(number)

    # Get th elevel index
    for i in range(6):
        value /= 1000
        if int(value) <= 0:
            value *= 1000
            break
        #

    if i == 5:
        value *= 1000

    # Get final value
    if isDecimal:
        return "{:,.2f}{}".format(value, numLevels[ i ])
    else:
        return "{:,}{}".format(int(value), numLevels[ i ])


# -----------------------------------------
#
# Responses to guest request
#
# -----------------------------------------
def sample_responses(input_text, update):
    user_message = str(input_text).lower()

    if ("/buy") in user_message:
        message = "💫🥷<b>Buy SNT</b>🥷💫\n\n" \
                  "Being that <b>Shib Ninja Token</b> is a BSC token, we're naturally\n" \
                  "on Pancake Swap, as it is the BSC equivalent of Uniswap!\n" \
                  "We are currently ONLY available on PCS. If you see us somewhere\n" \
                  "else, its a FAKE TOKEN!\n\n" \
                  "Please! ONLY use official links from https://www.ShibNinja.com or\n" \
                  "associated social media accounts.\n\n" \
                  "This is to protect YOU the investor!\n\n" \
                  "⚠️IMPORTANT⚠️\n" \
                  "MAKE SURE YOU ADD SNT TO YOUR WALLET:\n" \
                  "0x97329Bce201D86bbCBeebBB3B03256ABDF7b7De6\n\n"

        buy = "💵Ready to buy $SNT?💵\n\n👇👇Click here👇👇\nhttps://shibninja.com/buy-%24snt"
        update.message.reply_text(message + buy, parse_mode = 'Html', disable_web_page_preview = True)

        # All handled here
        return

    # -----------------------------------------
    # Info
    # -----------------------------------------
    if ("/info") in user_message:
        message = "🤬Tired of being scammed?😩\n\n" \
                  "💥🥷Join Clan Shibori!🥷💥\n\n" \
                  "We've created a SAFE BSC community for ALL!\n\n" \
                  "•Shib Ninja Token: 12/07/21\n" \
                  "•Website: <a href = 'https://www.ShibNinja.com'>Shib Ninja Token</a>\n\n" \
                  "Tokenomics:\n" \
                  " •Hyper Deflationary\n" \
                  " •Reflections: 5%\n" \
                  " •Total Taxes: 15%"
        update.message.reply_text(message, parse_mode = 'Html', disable_web_page_preview = True)
        # All handled here
        return

    # -----------------------------------------
    # Rewards
    # -----------------------------------------
    if ("/rewards") in user_message:
        message = "💥🥷<b><u>Rewards</u></b>!🥷💥\n\n" \
                  "5% Rewards in SHIB!\n" \
                  "\n" \
                  "5% of every transaction is taken and\n" \
                  "reflected back to the holders in #SHIB!\n" \
                  "\n" \
                  "This is REAL $SHIB you can trade at any\n" \
                  "time for BNB!\n" \
                  "\n" \
                  "[These Rewards are AUTO claimed when the Dividends Wallet has reached its minimum fill point for distribution.]\n" \
                  "\n" \
                  "Keep your $SNT and make your gains with SHIB, adding a little extra skin in the game in our favorite Dog Coin!\n" \
                  "\n" \
                  "⚠<b><u>Note:</u></b>⚠\n" \
                  "Rewards REQUIRE volume (Up or Down) to be distributed, this is why initial marketing funds are mandatory. If there is little volume, there are little rewards. Patience."
        update.message.reply_text(message, parse_mode = 'Html', disable_web_page_preview = True)
        # All handled here
        return

    if ("/donate") in user_message:
        return "Coming soon...Stay tuned. 😁"

    if ("/roadmap") in user_message:
        return "https://shibninja.com/road-map"

    # -----------------------------------------
    # Chart
    # -----------------------------------------
    if ("/chart") in user_message:
        chart = "<b>SNT/BSC:</b> <a href ='https://www.dextools.io/app/bsc/pair-explorer/0xbd9f1171322fce907d8bc3406d867c16ba916c3c'>DexTools</a>\n" \
                f"<b>SNT/BSC:</b> <a href ='https://poocoin.app/tokens/{Keys.SNT_CONTRACT}'>Poocoin</a>\n" \
                "<b>SNT/BSC:</b> <a href ='https://coinmarketcap.com/currencies/shib-ninja-token/'>Coin Market Cap</a>\n"

        update.message.reply_text(chart, parse_mode = 'Html', disable_web_page_preview = True)
        return

    # -----------------------------------------
    # Chart
    # -----------------------------------------
    if ("/contract") in user_message:
        chart = "🥷<b><u>Contract</u></b>🥷\n\n" \
                "Name: <a href = 'https://www.shibninja.com/'>Shib Ninja Token</a>\n\n" \
                f"[SNT]: <a href = 'https://bscscan.com/address/{Keys.SNT_CONTRACT}'>{Keys.SNT_CONTRACT}</a>\n" \
                "[SHIB]: <a href = 'https://bscscan.com/address/0x2859e4544c4bb03966803b044a93563bd2d0dd4d'>0x2859e4544c4bb03966803b044a93563bd2d0dd4d</a>\n"
        update.message.reply_text(chart, parse_mode = 'Html', disable_web_page_preview = True)
        return

    # -----------------------------------------
    # Voting sites
    # -----------------------------------------
    if ("/vote") in user_message:
        voter = "💥💥🥷<b><u>Vote/Action</u></b>🥷💥💥\n\n" \
                "👇👇👇VOTE👇👇👇\n" \
                "✅<a href = 'https://coinmerge.io'>CoinMerge</a> [Vote]\n" \
                "✅<a href = 'https://coinsniper.net/coin/22578'>Coin Sniper</a> [Vote]\n" \
                "✅<a href = 'https://watcher.guru/coin/shib-ninja-token'>Watcher Guru</a> [Vote]\n" \
                "✅<a href = 'https://www.coinscope.co/coin/snt?'>Coin Scope</a> [Vote]\n" \
                "✅<a href = 'https://coinwolfs.com/tokenInfo?Shib_Ninja_Token'>Coin Wolf</a> [Vote]\n" \
                "✅<a href = 'https://gemhunters.net/coin/shib-ninja-token/'>Gem Hunters</a> [Vote]\n" \
                "✅<a href = 'https://coindiscovery.app/coin/shib-ninja-token'>Coin Discovery</a> [Vote]\n" \
                "✅<a href = 'https://coinhunt.cc/coin/1903225630'>Coin Hunt</a> [Vote]\n\n" \
                "👇SEARCH & COMMENT👇\n" \
                "✅<a href = 'https://twitter.com/search?q=($SNT OR #ShibNinjaToken OR @Shibori Or #ShiboriClan)&src=typed_query&f=live'>Twitter Search</a>\n\n" \
                "Thank you for being an active\n" \
                "member of the Shibori Clan!🙏"
        #
        update.message.reply_text(voter, parse_mode = 'Html', disable_web_page_preview = True)
        # All handled here
        return

    # -----------------------------------------
    #
    #
    #
    # -----------------------------------------
    if ("/website") in user_message:
        return "https://www.ShibNinja.com"

    if ("/twitter") in user_message:
        return "https://twitter.com/ShiboriClan"

    if ("/discord") in user_message:
        return "https://discord.gg/KVyG2vzjnU"

    if ("/reddit") in user_message:
        return "https://www.reddit.com/r/ShibNinjaToken/"

    if ("/ninja") in user_message:
        founder = "<b>Ninja Master</b>\nhttps://twitter.com/RealShibNinja"
        return founder

    # -----------------------------------------
    # Return all social media contact info
    # -----------------------------------------
    if ("/social") in user_message:
        header = "<b>💥💥🥷Shibori Clan🥷💥💥</b>\n"
        # Twitter
        social = "<a href = 'https://www.ShibNinja.com'>Shib Ninja Website</a>\n<a href = 'https://twitter.com/ShiboriClan'>Shibori: Twitter</a>\n<a href = 'https://www.reddit.com/r/ShibNinjaToken/'>Shibori: Reddit</a> \n<a href = 'https://discord.gg/KVyG2vzjnU'>Shibori: Discord</a>\n\n"

        team_1 = "<b>Twitter Team:</b>\n<a href ='https://twitter.com/RealShibNinja'>RealShibNinja</a> \n<a href = 'https://twitter.com/ShibSoldier'>ShibSoldier</a> \n<a href = 'https://twitter.com/CNelson580'>CNelson580</>\n"
        team_2 = "<a href = 'https://twitter.com/OlgaNel16824866'>OlgaNel16824866</a> \n<a href = 'https://twitter.com/CodeIsLife101'>CodeIsLife</a>"
        update.message.reply_text(header + social + team_1 + team_2, parse_mode = 'Html',
                                  disable_web_page_preview = True)
        return

    # -----------------------------------------
    #
    # Return the Supplies and market cap value
    #
    # -----------------------------------------
    if ("/mc") in user_message:
        # bsc = BscScan(Keys.BSC_KEY)
        with BscScan(Keys.BSC_KEY, asynchronous = False) as bsc:
            try:
                total = bsc.get_total_supply_by_contract_address(Keys.SNT_CONTRACT)
                #            dev = bsc.get_acc_balance_by_token_contract_address(Keys.SNT_CONTRACT, Keys.SNT_DEVELOPER)
                mark = bsc.get_acc_balance_by_token_contract_address(Keys.SNT_CONTRACT, Keys.SNT_MARKETING)
                #            tour = bsc.get_acc_balance_by_token_contract_address(Keys.SNT_CONTRACT, Keys.SNT_TOURNAMENT)
                burn = bsc.get_acc_balance_by_token_contract_address(Keys.SNT_CONTRACT, Keys.SNT_BURNED)
                #            mcap = bsc.get_su
                circ = int(total) - (int(burn) + int(mark))

                # ------------------------------------------
                # Get the price info!
                # ------------------------------------------
                ps = PancakeSwapAPI()
                summary = ps.tokens(Keys.SNT_CONTRACT)
                price_bnb = Decimal(summary[ "data" ][ "price_BNB" ])
                price = Decimal(summary[ "data" ][ "price" ])

                # Format the numbers
                circ = get_decimal_value(circ, 18)
                total = get_decimal_value(int(total), 18)
                burn = (total - circ)

                # ------------------------------------------
                # Shrink the values
                # ------------------------------------------
                # mcap = (circ ** price)
                mcap = "{:,.2f}".format(total * price)
                total = Shrink(total, False)

                circ = Shrink(circ, True)
                burn = Shrink(burn, True)
            except:
                return "Cannot process now..."
            else:
                # Format the string
                mc_string = "<b>📊📈Market Cap💵</b>\nTotal SNT Supply: <b>{0}</b>\nTotal SNT Burned: <b>{1}</b>\nCirculating SNT: <b>{2}</b>\nSNT Market Cap: <b>${3}</b>".format(
                    total, burn, circ, mcap)
                return str(mc_string)

    # I do not understand you.
    return None
