import discord

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_message(message):

    # Ignore messages sent by the bot
    if message.author == client.user:
        return
    
    # Check if the message contains inappropriate language
    if any(word in message.content for word in ["swear", "curse", "hate"]):
        # Send a message reminding the user to follow the code of conduct
        await message.channel.send("Please remember to follow the clan's code of conduct and use appropriate language.")
        # Apply a warning to the user"s account
        apply_warning(message.author)
        
    # Check if the user is participating in clan events and activities
    if not has_recent_activity(message.author):
        # Send a message reminding the user to participate in clan events and activities
        await message.channel.send("Please remember to participate in clan events and activities.")
        # Apply a warning to the user"s account
        apply_warning(message.author)
        
    # Check if the user is respecting the decisions of higher-ranked members
    if not is_respecting_decisions(message.author):
        # Send a message reminding the user to respect the decisions of higher-ranked members
        await message.channel.send("Please remember to respect the decisions of higher-ranked members.")
        # Apply a warning to the user"s account
        apply_warning(message.author)


def apply_warning(user):

    # Increment the user"s warning count by 1
    user.warning_count += 1
    # Check if the user has reached the maximum number of warnings
    if user.warning_count >= MAX_WARNINGS:
        # Demote the user to the next lower rank
        demote(user)
        
def demote(user):

    # Check the user"s current rank and demote them to the next lower rank
    if user.rank == "Admin":
        user.rank = "Moderator"
    elif user.rank == "Moderator":
        user.rank = "Regular Member"
    elif user.rank == "Regular Member":
        user.rank = "Member"

def has_recent_activity(user):

    # Check if the user has participated in a clan event or activity within the past week
    return user.last_activity_date >= datetime.datetime.now() - datetime.timedelta(weeks=1)


def is_respecting_decisions(user):

    # Check if the user has recently argued with or disagreed with a higher-ranked member
    return not any(conversation.start_date >= datetime.datetime.now() - datetime.timedelta(weeks=1) and conversation.has_disagreement(user) for conversation in user.conversations)


def main():
    try:
        with open("token.txt", "r") as file:
            token = file.read().strip()
    except FileNotFoundError:
        print("Please put your bot token in a file called 'token.txt' in the same folder as this script.")
    else:
        client.run(token)


if __name__ == "__main__":
    main()
