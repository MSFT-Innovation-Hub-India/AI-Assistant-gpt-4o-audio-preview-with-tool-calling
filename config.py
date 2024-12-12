
from dotenv import load_dotenv
import os
load_dotenv()

# this is the API key for OpenAI. This API is not available in Azure OpenAI at the time of this writing
api_key=os.getenv("api_key")
model=os.getenv("model")

# Jira connection details (to register grievances)
attlassian_api_key = os.getenv("attlassian_api_key")
attlassian_user_name = os.getenv("attlassian_user_name")
attlassian_url = os.getenv("attlassian_url")
grievance_project_key = os.getenv("grievance_project_key")
grievance_type = os.getenv("grievance_type")
grievance_project_name = os.getenv("grievance_project_name")

# Azure AI Search connection & index details (to peform QnA from manuals)
ai_search_url = os.getenv("ai_search_url")  
ai_search_key = os.getenv("ai_search_key")
ai_index_name = os.getenv("ai_index_name")
ai_semantic_config = os.getenv("ai_semantic_config")

ai_assistant_organization_name = os.getenv("ai_assistant_organization_name")

# azure sql database connection details (lets users query their game status summary)
az_db_server = os.getenv("az_db_server")
az_db_database = os.getenv("az_db_database")
az_db_username = os.getenv("az_db_username")
az_db_password = os.getenv("az_db_password")