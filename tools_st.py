import config
from atlassian import Jira
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import pyodbc


class ConnectionManager:
    """
    Implements static responses to function calls for ease of testing the gpt-4o audio preview APIs.
    Use this class instead of tools.py if you want to see this demo in action and not worry about integration with back end services like SQL, Jira, AI Search, etc.
    You need to call this class instead of tools.py in bot-app.py
    """

    def __init__(self):

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
        return ConnectionManager.reg_grievance_response

    async def register_user_grievance(self, grievance_category, grievance_description):
        return ConnectionManager.reg_grievance_response

    async def perform_search_based_qna(self, query):
        return ConnectionManager.search_qna_response

    async def get_game_status_summary(self, user_name: str):
        response_message = ""
        return ConnectionManager.game_status_response

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
    """
