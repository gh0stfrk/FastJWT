from discord_webhook import DiscordWebhook, DiscordEmbed

class CreateMessage:
    def __init__(self, title, description, scope_of_work, deadline, compensation, resources):
        self.title = title
        self.description = description
        self.scope_of_work = scope_of_work
        self.deadline = deadline
        self.compensation = compensation
        self.resources = resources
        
    def create_embed(self):
        embed = DiscordEmbed(title="Project Title", description=self.title)
        embed.add_embed_field(name="Description", value=self.description, inline=False)
        embed.add_embed_field(name="Scope of Work", value=self.scope_of_work, inline=False)
        embed.add_embed_field(name="Deadline", value=self.deadline, inline=False)
        embed.set_timestamp()
        embed.add_embed_field(name="Compensation", value=self.compensation, inline=False)
        embed.add_embed_field(name="Resources", value=self.resources, inline=False)
        return embed
    
    def send(self, url):
        webhook = DiscordWebhook(url=url)
        embed = self.create_embed()
        webhook.add_embed(embed)
        response = webhook.execute()
        return response
 
 
if __name__ == "__main__":
    title = "Business Data Extraction and Transformation via API + Streamlit dashboard"
    description = """This project involves setting up API calls to the DataForSEO API to retrieve Google Maps data based on specific categories. The data will then be filtered and transformed to include only essential information like name, website URL, and category. The final solution will enable exporting this data directly into Google Sheets using gspread or as a CSV file. It is necessary
    """
    scope_of_work = """API Integration: Establish secure and efficient API calls to DataForSEO to retrieve Google Maps data based on provided criteria (e.g., categories).
    Data Filtering and Transformation: Implement logic to filter through the retrieved data and extract necessary details (name, website URL, category).
    Export Functionality: Develop functionality to export the processed data into Google Sheets and as a CSV file, ensuring compatibility and ease of use.
    User Interface: Design a simple and intuitive interface to specify criteria, preview data and select location to export.
    Expected Deliverables:

    Source code repository with the implemented solution.
    Google Sheets integration or CSV download functionality.
    User-friendly interface for operating the solution."""
    deadline = "27/02/2024"
    compensation = "$40 USD (Rs. 3.3k)"
    resources = """
    DataForSEO API Documentation: https://docs.dataforseo.com/v3/databases/business_listings/
    Access credentials for the DataForSEO API will be provided upon project initiation.
    Guide to Google Sheets API for integration purposes
    https://docs.gspread.org/en/latest/oauth2.html#for-end-users-using-oauth-client-id
    """

    message = CreateMessage(title, description, scope_of_work, deadline, compensation, resources)
    message.send(url="https://discord.com/api/webhooks/1214543877562703972/0KZjD9mDn7Yx5ZzVLDdzy_lBUZE0npMXPf8jfkDJXwOOS-CThEPH2eYury391TegDx75")