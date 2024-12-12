import config
from atlassian import Jira
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import pyodbc

"""
This module contains the ConnectionManager class, which manages connections to a SQL database, Jira ticketing system and Azure AI Search, 
and implements various function calls to interact with them. The back end services used in this class must be provisioned first to 
have the full fledged integration in the application working. 
To see gpt-4o-audio-preview in action without these integrations, tools.py can be used, where the function calls return static data without
the need for integration. This class has been retained here only for reference purposes. 
"""

class ConnectionManager:
    """
    Manages connections to a SQL database and Jira ticketing system, and provides various functions to interact with these systems.
    Attributes:
        l_connection (pyodbc.Connection): Connection object for the SQL database.
        l_jira (Jira): Jira connection object.
        functions (list): List of available functions with their descriptions and parameters.
    Methods:
        get_grievance_status(grievance_id):
            Fetches the status of a grievance from the Jira ticketing system.
        register_user_grievance(grievance_category, grievance_description):
            Registers a user grievance in the Jira ticketing system.
        perform_search_based_qna(query):
            Performs a search-based QnA using Azure Cognitive Search.
        get_game_status_summary(user_name):
            Retrieves the game status summary for a user from the SQL database.
    """

    def __init__(self):
        self.l_connection = None
        self.l_jira = None

        try:
            self.l_connection = pyodbc.connect(
                "Driver={ODBC Driver 18 for SQL Server};SERVER="
                + config.az_db_server
                + ";DATABASE="
                + config.az_db_database
                + ";UID="
                + config.az_db_username
                + ";PWD="
                + config.az_db_password
            )
            print("Connected to the database....")
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            print("Exiting the program....")
            exit(1)
        try:
            self.l_jira = Jira(
                url=config.attlassian_url,
                username=config.attlassian_user_name,
                password=config.attlassian_api_key,
            )
            self.l_jira.myself()
            print("Connected to Jira ticketing system....")
        except Exception as e:
            print(f"Error connecting to Jira: {e}")
            print("Exiting the program....")
            exit(1)

        self.functions = [
            {
                "name": "register_user_grievance",
                "description": "register a grievance, or complaint or issue from the user in the Ticketing system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "grievance_category": {
                            "type": "string",
                            "enum": [
                                "wallet issues",
                                "reward points issues",
                                "gaming experience issues",
                                "usage history issues",
                                "other issues",
                            ],
                        },
                        "grievance_description": {
                            "type": "string",
                            "description": "The detailed description of the grievance faced by the user",
                        },
                    },
                    "required": ["grievance_category", "grievance_description"],
                },
            },
            {
                "name": "perform_search_based_qna",
                "description": "Seek general assistance or register complaint with the AI assistant. This requires performing a search based QnA on the query provided by the user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The user query pertaining to gaming services",
                        }
                    },
                    "required": ["query"],
                },
            },
            {
                "name": "get_grievance_status",
                "description": "fetch real time grievance status for a grievance id",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "grievance_id": {
                            "type": "number",
                            "description": "The grievance id of the user registered in the Ticketing System",
                        }
                    },
                    "required": ["grievance_id"],
                },
            },
            {
                "name": "get_game_status_summary",
                "description": "retrieve the game status summary for a user based on the user name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_name": {
                            "type": "string",
                            "description": "The user name of the user registered in the Gaming System",
                        }
                    },
                    "required": ["user_name"],
                },
            },
        ]

    async def get_grievance_status(self, grievance_id):
        response_message = ""
        response = ""
        JQL = (
            "project = "
            + config.grievance_project_name
            + " AND id = "
            + str(grievance_id)
        )

        try:
            response_message = self.l_jira.jql(JQL)
            print("Issue status retrieved successfully!")
            # print("grievance status response .. ", response_message)
            if response_message["issues"]:
                response = (
                    "\n Here is the updated status of your grievance. grievance_id : "
                    + response_message["issues"][0]["id"]
                )
                response += (
                    "\n , priority is "
                    + response_message["issues"][0]["fields"]["priority"]["name"]
                )
                response += (
                    "\n , status is "
                    + response_message["issues"][0]["fields"]["status"][
                        "statusCategory"
                    ]["key"]
                )
                response += (
                    "\n , grievance description is "
                    + response_message["issues"][0]["fields"]["description"]
                )
                if response_message["issues"][0]["fields"]["duedate"]:
                    response += (
                        "\n , due date is "
                        + response_message["issues"][0]["fields"]["duedate"]
                    )
                else:
                    response += "\n , due date is not assigned by the system yet."
            else:
                response = "sorry, we could not locate a grievance with this ID. Can you please verify your input again?"
        except Exception as e:
            print(f"Error retrieving the grievance: {e.args[0]}")
            response = "We had an issue retrieving your grievance status. Please check back in some time"
            print(response)
        return response

    async def register_user_grievance(self, grievance_category, grievance_description):
        response_message = ""
        try:
            # Define the issue details (project key, summary, description, and issue type)
            issue_details = {
                "project": {"key": config.grievance_project_key},
                "summary": grievance_category,
                "description": grievance_description,
                "issuetype": {"name": "Task"},
            }

            # Create the issue
            response = self.l_jira.create_issue(fields=issue_details)
            response_message = (
                "We are sorry about the issue you are facing. We have registered a grievance with id "
                + response["id"]
                + " to track it to closure. Please quote that in your future communications with us"
            )
            print("grievance registered!")
        except Exception as e:
            print(f"Error registering the grievance issue: {e.args[0]}")
            response_message = "We had an issue registering your grievance. Please check back in some time"
            print(response_message)
        return response_message

    async def perform_search_based_qna(self, query):
        print("performing document search ....")
        credential = AzureKeyCredential(config.ai_search_key)
        client = SearchClient(
            endpoint=config.ai_search_url,
            index_name=config.ai_index_name,
            credential=credential,
        )
        results = list(
            client.search(
                search_text=query,
                query_type="semantic",
                semantic_configuration_name=config.ai_semantic_config,
            )
        )
        response_docs = ""
        counter = 0
        for result in results:
            # print(f"search result............\n {result}")
            response_docs += (
                " --- Document context start ---"
                + result["content"]
                + "\n ---End of Document ---\n"
            )
            counter += 1
            if counter == 2:
                break
        print(f"search results from the User manual Archives are : \n {response_docs}")
        return response_docs

    async def get_game_status_summary(self, user_name: str):
        response_message = ""
        cursor = None
        print("querying database to get game status summary for ", user_name)
        try:
            cursor = self.l_connection.cursor()
            query = "SELECT user_name, game_type, COUNT(*) AS games_played, SUM(entry_fee) AS total_entry_fee, SUM(points_earned) AS total_points_earned, SUM(cash_won) AS total_cash_won FROM Gaming_Transaction_History AS gth WHERE user_name = ? GROUP BY user_name, game_type ORDER BY user_name, game_type;"
            cursor.execute(query, user_name.lower())
            print("executed query successfully")
            response_message += "The game status summary is:"
            # add the column name corresponding to each value in the row to the response message first
            column_names = [description[0] for description in cursor.description]
            for row in cursor:
                # print("data returned :", row)
                response_message += "\n"
                for column, value in zip(column_names, row):
                    response_message += f"{column}: {value}\n"

        except Exception as e:
            print(e)
            print("Error in database query execution")
            return "We had an issue retrieving your grievance status. Please check back in some time"

        print("game status summary from database - ", response_message)
        return response_message

    available_functions = {
        "register_user_grievance": register_user_grievance,
        "perform_search_based_qna": perform_search_based_qna,
        "get_grievance_status": get_grievance_status,
        "get_game_status_summary": get_game_status_summary,
    }

    reg_grievance_response = """
    We are sorry about the issue you are facing. We have registered a grievance with id 10091 to track it to closure. 
    Please quote that in your future communications with us
    """

    get_grievance_status_response = """
    Here is the updated status of your grievance. grievance_id : 10091
    , priority is Medium
    , status is new
    , grievance description is The game continues to crash my computer despite updating drivers, ensuring system requirements, verifying game files, and reinstalling the game. I am disappointed with the gaming experience.
    , due date is not assigned by the system yet.
    """

    search_qna_response = """
    --- Document context start ---3. Detailed Question and Answer Section
    Q: What should I do if my game crashes frequently? A: Frequent crashes can be caused by various factors, including outdated drivers, insufficient system resources, or corrupted game files. Try the following steps:
    1.      Update your graphics and system drivers.
    2.      Ensure your system meets the minimum requirements for the game.
    3.      Verify the integrity of the game files through the game launcher.
    4.      Reinstall the game if the issue persists.
    Q: How can I improve my game performance? A: Improving game performance can enhance your gaming experience. Consider the following tips:
    1.      Lower the in-game graphics settings.
    2.      Close unnecessary background applications.
    3.      Ensure your system is free from malware.
    4.      Upgrade your hardware if possible (e.g., more RAM, better GPU).
    Q: How do I link my account to social media? A: Linking your account to social media platforms can enhance your gaming experience. Go to the account settings on our website, find the social media linking section, and follow the instructions to connect your accounts.
    Q: What do I do if I encounter a hacker or cheater in the game? A: Report the player using the in-game reporting tool. Provide details such as the player's username and a description of the suspicious activity. Our team will investigate and take appropriate action.
    Q: How can I participate in beta testing for new games? A: To participate in beta testing, sign up for our beta program on our website. Selected participants will receive an invitation with instructions on how to access the beta version of the game.
    4. User Guidance Documents
    Setting Up Your Account
    1.      Creating an Account:
    o       Visit our website and click on "Sign Up."
    o       Fill in the required details: email, username, and password.
    o       Verify your email address through the verification link sent to you.
    2.      Securing Your Account:
    o       Enable two-factor authentication (2FA) in your account settings.
    o       Use a strong, unique password and change it regularly.
    o       Avoid sharing your account details with others.

    ---End of Document ---
    --- Document context start ---Troubleshooting Common Issues
    1.      Game Won't Launch:
    o       Ensure your system meets the game's minimum requirements.
    o       Update your graphics drivers.
    o       Verify the game files through the game launcher.
    o       Disable any conflicting background applications.
    2.      Lag and Connectivity Issues:
    o       Check your internet connection speed and stability.
    o       Use a wired connection instead of Wi-Fi for better stability.
    o       Close bandwidth-heavy applications running in the background.
    Understanding Game Mechanics
    1.      Basic Controls:
    o       Refer to the in-game tutorial or settings menu for control mappings.
    o       Customize controls to your preference if the game allows it.
    2.      Advanced Strategies:
    o       Join community forums and discussions to learn from other players.
    o       Watch gameplay videos and streams for tips and tricks.
    o       Practice regularly to improve your skills.
    Safe and Responsible Gaming
    1.      Setting Limits:
    o       Set time limits for your gaming sessions to avoid excessive play.
    o       Take regular breaks to rest your eyes and stretch.
    2.      Recognizing Problematic Behavior:
    o       Be aware of signs of gaming addiction, such as neglecting responsibilities or social activities.
    o       Seek support if you or someone you know is struggling with gaming addiction.
    Contacting Support
    1.      Submitting a Ticket:
    o       Visit our support page and click on "Submit a Ticket."
    o       Fill in the required details, including a description of your issue.
    o       Attach any relevant screenshots or files.
    2.      Live Chat Support:
    o       Access live chat support through our website during available hours.
    o       Provide your account details and a brief description of your issue to the support agent.

    ---End of Document ---

    Output of function call: >  --- Document context start ---3. Detailed Question and Answer Section
    Q: What should I do if my game crashes frequently? A: Frequent crashes can be caused by various factors, including outdated drivers, insufficient system resources, or corrupted game files. Try the following steps:
    1.      Update your graphics and system drivers.
    2.      Ensure your system meets the minimum requirements for the game.
    3.      Verify the integrity of the game files through the game launcher.
    4.      Reinstall the game if the issue persists.
    Q: How can I improve my game performance? A: Improving game performance can enhance your gaming experience. Consider the following tips:
    1.      Lower the in-game graphics settings.
    2.      Close unnecessary background applications.
    3.      Ensure your system is free from malware.
    4.      Upgrade your hardware if possible (e.g., more RAM, better GPU).
    Q: How do I link my account to social media? A: Linking your account to social media platforms can enhance your gaming experience. Go to the account settings on our website, find the social media linking section, and follow the instructions to connect your accounts.
    Q: What do I do if I encounter a hacker or cheater in the game? A: Report the player using the in-game reporting tool. Provide details such as the player's username and a description of the suspicious activity. Our team will investigate and take appropriate action.
    Q: How can I participate in beta testing for new games? A: To participate in beta testing, sign up for our beta program on our website. Selected participants will receive an invitation with instructions on how to access the beta version of the game.
    4. User Guidance Documents
    Setting Up Your Account
    1.      Creating an Account:
    o       Visit our website and click on "Sign Up."
    o       Fill in the required details: email, username, and password.
    o       Verify your email address through the verification link sent to you.
    2.      Securing Your Account:
    o       Enable two-factor authentication (2FA) in your account settings.
    o       Use a strong, unique password and change it regularly.
    o       Avoid sharing your account details with others.


    ---End of Document ---
    --- Document context start ---Troubleshooting Common Issues
    1.      Game Won't Launch:
    o       Ensure your system meets the game's minimum requirements.
    o       Update your graphics drivers.
    o       Verify the game files through the game launcher.
    o       Disable any conflicting background applications.
    2.      Lag and Connectivity Issues:
    o       Check your internet connection speed and stability.
    o       Use a wired connection instead of Wi-Fi for better stability.
    o       Close bandwidth-heavy applications running in the background.
    Understanding Game Mechanics
    1.      Basic Controls:
    o       Refer to the in-game tutorial or settings menu for control mappings.
    o       Customize controls to your preference if the game allows it.
    2.      Advanced Strategies:
    o       Join community forums and discussions to learn from other players.
    o       Watch gameplay videos and streams for tips and tricks.
    o       Practice regularly to improve your skills.
    Safe and Responsible Gaming
    1.      Setting Limits:
    o       Set time limits for your gaming sessions to avoid excessive play.
    o       Take regular breaks to rest your eyes and stretch.
    2.      Recognizing Problematic Behavior:
    o       Be aware of signs of gaming addiction, such as neglecting responsibilities or social activities.
    o       Seek support if you or someone you know is struggling with gaming addiction.
    Contacting Support
    1.      Submitting a Ticket:
    o       Visit our support page and click on "Submit a Ticket."
    o       Fill in the required details, including a description of your issue.
    o       Attach any relevant screenshots or files.
    2.      Live Chat Support:
    o       Access live chat support through our website during available hours.
    o       Provide your account details and a brief description of your issue to the support agent.
    ---End of Document ---
    """

    game_status_response = """
    user_name: srikantan
    game_type: Chess
    games_played: 5
    total_entry_fee: 35
    total_points_earned: 676
    total_cash_won: 60

    user_name: srikantan
    game_type: Ludo
    games_played: 7
    total_entry_fee: 55
    total_points_earned: 2628
    total_cash_won: 115

    user_name: srikantan
    game_type: Poker
    games_played: 4
    total_entry_fee: 75
    total_points_earned: 1164
    total_cash_won: 165

    user_name: srikantan
    game_type: Rummy
    games_played: 5
    total_entry_fee: 65
    total_points_earned: 1182
    total_cash_won: 100

    Output of function call: > The game status summary is:
    user_name: srikantan
    game_type: Chess
    games_played: 5
    total_entry_fee: 35
    total_points_earned: 676
    total_cash_won: 60

    user_name: srikantan
    game_type: Ludo
    games_played: 7
    total_entry_fee: 55
    total_points_earned: 2628
    total_cash_won: 115

    user_name: srikantan
    game_type: Poker
    games_played: 4
    total_entry_fee: 75
    total_points_earned: 1164
    total_cash_won: 165

    user_name: srikantan
    game_type: Rummy
    games_played: 5
    total_entry_fee: 65
    total_points_earned: 1182
    total_cash_won: 100
    """
