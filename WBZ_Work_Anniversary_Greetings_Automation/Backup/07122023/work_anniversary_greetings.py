import msal
import httpx

# Define your Microsoft Graph API credentials
client_id = "your_client_id"
client_secret = "your_client_secret"
tenant_id = "your_tenant_id"

# Define the scope for the Graph API (in this case, Mail.Send)
scopes = ["https://graph.microsoft.com/.default"]

# Define the user's email address
user_email = "achyutam.mehta@wonderbotz.com"

# Microsoft Graph API endpoint for sending emails
graph_api_endpoint = "https://graph.microsoft.com/v1.0/me/sendMail"

# MSAL Confidential Client Application
confidential_client = msal.ConfidentialClientApplication(
    client_id, authority=f"https://login.microsoftonline.com/{tenant_id}",
    client_credential=client_secret
)

# Acquire a token for the Graph API
token_response = confidential_client.acquire_token_for_client(scopes=scopes)

# Check if the token was acquired successfully
if "access_token" in token_response:
    access_token = token_response["access_token"]

    # Create an HTTPX client for making requests
    client = httpx.AsyncClient()

    # Define the email message
    email_message = {
        "subject": "API meet",
        "body": {
            "contentType": "HTML",
            "content": "The new cafeteria is open. Successful...!!!"
        },
        "toRecipients": [
            {
                "emailAddress": {
                    "address": user_email
                }
            }
        ]
    }

    # Send the email using the Microsoft Graph API
    response = await client.post(graph_api_endpoint,
                                 headers={"Authorization": f"Bearer {access_token}"},
                                 json={"message": email_message})

    # Check if the email was sent successfully
    if response.status_code == 202:
        print("Email sent successfully!")
    else:
        print(f"Failed to send email. Status code: {response.status_code}")
else:
    print("Failed to acquire access token.")

# Close the HTTPX client
await client.aclose()
