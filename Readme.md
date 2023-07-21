# SAP Attendance Bot

This is a python selenium program to get attendance details from the SAP Prtal of KIIT University. It uses the selenium webdriver to automate the process of logging in and getting the attendance details. It sends the attendance details to th user's telegram account.

## Features

* Updates attendance details periodically.
* Sends the attendance details to the user's telegram account.
* Stores the attendance details in a csv file.
* Sends a notification to the user's telegram account if the attendance is below 80%.

## Requirements

* Python 3.6 or higher
* APScheduler==3.0.0
* requests==2.26.0
* requests-oauthlib==1.3.0
* selenium==4.3.0

## Deployment
1. Clone the repository from GitHub:

```bash
git clone https://github.com/Satyajit-2003/SAP-bot.git
```

2. Create a virtual environment and activate it.

```bash
python -m venv venv && source venv/bin/activate
```

3. Install the dependencies.
```bash
pip install -r requirements.txt
```

4. Edit the `config.py` file and add your credentials.

5. Run the `clock.py` file.
```bash
python clock.py
```


## Filling details in config.py

> :warning: **Hosting Services**: If you are using a hosting service like Heroku, you need to add the credentials as environment variables. You can do this by going to the settings of your app and adding the credentials as environment variables.

* If you don't have a telegram bot, create one using the [BotFather](https://t.me/botfather) and add the bot token to the `config.py` file.

* You can get your telegram chat id by sending a message to the bot and then visiting the following url: `https://api.telegram.org/bot<yourtoken>/getUpdates` or any 3rd party bot like [Bot Info](https://t.me/chatIDrobot).

* Add your SAP credentials to the `config.py` file. If multiple users are using the bot, add the credentials of all the users in the `config.py` file, separated by commas. BE SURE TO MAINTAIN THE ORDER OF THE CREDENTIALS ACCROSS ALL THE LISTS.

* You can edit the timing of the scheduler. Be sure to use the 24 hour format. Give the timing in the timezone of the server. (In case of a hosting service, the timezone of the server is generally UTC)

## Usage

You will get details on your telegram account automatically, no need to do anything.

## Contributing

If you would like to contribute to the project, please fork the repository and submit a pull request.

## Bugs

If you find a bug, please open an issue on the GitHub repository.

## License

The project is licensed under the MIT License.
