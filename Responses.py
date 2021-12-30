
# -----------------------------------------
#
# Responses to guest request
#
# -----------------------------------------
def sample_responses(input_text, update):
    user_message = str(input_text).lower()
    
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

    # return "I do not understand you."
    return None
