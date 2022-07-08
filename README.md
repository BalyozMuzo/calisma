
## Steps to Install:

1-Download python from https://www.python.org/downloads/

2-Run the installer.

3-Go into command prompt and enter the following code command

* *Windows:* ```py -m pip install discord```
 
  *MacOS:* ```python3 -m pip install discord```

* *Windows:* `py -m pip install discord asyncio`

   *MacOS:* `python3 -m pip install discord asyncio`
   
* *Windows:* `py -m pip install github`

   *MacOS:* `python3 -m pip install github`  
   
* *Windows:* `py -m pip install py-cord==2.0.0b1`

   *MacOS:* `python3 -m pip install py-cord==2.0.0b1`    
   
   
4. Go to https://discordapp.com/developers/applications and create your application, go to the bot section, and copy your token. Place it into the quotes on the last line of code in main.py, replacing the word **TOKEN**   


## Creating an Application

An application allows you to interact with Discord’s APIs by providing authentication tokens, designating permissions, and so on.

To create a new application, select New Application:
![image](https://user-images.githubusercontent.com/96955054/178004505-379004c5-37fc-44fa-808c-ad75361128c8.png)
Next, you’ll be prompted to name your application. Select a name and click Create:
![image](https://user-images.githubusercontent.com/96955054/178004551-17261278-aff1-4fd4-9f7f-e83ed6c5e1cb.png)
Congratulations! You made a Discord application. On the resulting screen, you can see information about your application:
![image](https://user-images.githubusercontent.com/96955054/178004590-82cec564-8e8c-41c1-a662-e903e62f445b.png)
Keep in mind that any program that interacts with Discord APIs requires a Discord application, not just bots. Bot-related APIs are only a subset of Discord’s total interface.

However, since this tutorial is about how to make a Discord bot, navigate to the Bot tab on the left-hand navigation list.

## Creating a Bot

As you learned in the previous sections, a bot user is one that listens to and automatically reacts to certain events and commands on Discord.

For your code to actually be manifested on Discord, you’ll need to create a bot user. To do so, select Add Bot:
![image](https://user-images.githubusercontent.com/96955054/178004709-93c2e0fa-afdd-4ab9-b508-148b3a9978f1.png)
Once you confirm that you want to add the bot to your application, you’ll see the new bot user in the portal:
![image](https://user-images.githubusercontent.com/96955054/178004752-d5e25ee4-ae8e-440f-941e-fa27c67846f3.png)
Notice that, by default, your bot user will inherit the name of your application. Instead, update the username to something more bot-like, such as RealPythonTutorialBot, and Save Changes:
![image](https://user-images.githubusercontent.com/96955054/178004795-3a71f484-581f-4fd1-8fb6-683a4e21be01.png)
Now, the bot’s all set and ready to go, but to where?

A bot user is not useful if it’s not interacting with other users. Next, you’ll create a guild so that your bot can interact with other users.

## Adding a Bot to a Guild

A bot can’t accept invites like a normal user can. Instead, you’ll add your bot using the OAuth2 protocol.
To do so, head back to the Developer Portal and select the OAuth2 page from the left-hand navigation:
![image](https://user-images.githubusercontent.com/96955054/178005013-ce7b0b7f-58b3-4492-b511-cc66abbd24d4.png)
From this window, you’ll see the OAuth2 URL Generator.

This tool generates an authorization URL that hits Discord’s OAuth2 API and authorizes API access using your application’s credentials.

In this case, you’ll want to grant your application’s bot user access to Discord APIs using your application’s OAuth2 credentials.

To do this, scroll down and select bot from the SCOPES options and Administrator from BOT PERMISSIONS:
![image](https://user-images.githubusercontent.com/96955054/178005056-67989ffb-d180-4eae-8382-8818ffdbc2cb.png)
Now, Discord has generated your application’s authorization URL with the selected scope and permissions.
Select Copy beside the URL that was generated for you, paste it into your browser, and select your guild from the dropdown options:
![image](https://user-images.githubusercontent.com/96955054/178005143-698d1cd5-f6e6-4aa3-a96b-87e12e0f5377.png)
Click Authorize, and you’re done!

## User guide:

## Commands:

1- /add_question (for mods and admins only)

![image](https://user-images.githubusercontent.com/96955054/178001662-1a8e1441-4a7d-47dc-bc5f-30f95642c547.png)

With this command, you can add questions to the pool . Example: /add_question question: "question info ..." answer: "the answer to the question..."

2- /dell_question (for mods and admins only)

![image](https://user-images.githubusercontent.com/96955054/178002239-0d26bca6-e1bf-4181-b2c5-5c6d47cc681a.png)

Allows you to delete the desired question . The "id" of the question can be found at this link = https://github.com/BalyozMuzo/calisma/blob/main/discord1.json

3- /start (for mods and admins only)

![image](https://user-images.githubusercontent.com/96955054/178002737-b741b369-a7e9-4f5e-986a-c14ed6a8df2d.png)

This command starts the contest,2 pieces of information are entered .You determine how many rounds there will be and how many people will win .

4- /answer

![image](https://user-images.githubusercontent.com/96955054/178003390-a453218c-d387-4987-9913-1c85f347b147.png)

Contestants answer the questions with the "answer" command if their answers are correct, they will go to the next round.

![image](https://user-images.githubusercontent.com/96955054/178003596-a04aa5df-b8a5-4b82-ad5a-b0da15a8bb1e.png)
