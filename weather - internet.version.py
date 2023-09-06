import requests
from twilio.rest import Client

# Define the API URL
api_url = "API_URL"

# Define the query parameters
params = {
    "location": "42.963795,-85.670006",
    "fields": "temperature,precipitationType",  # Include precipitation data
    "timesteps": "1h",
    "units": "imperial",
    "apikey": "YOURAPIKEY",
}

# Make the GET request to the API
response = requests.get(api_url, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Check if the "data" key exists in the response
    if "data" in data:
        # Extract temperature and precipitation data
        temperature = data["data"]["timelines"][0]["intervals"][0]["values"][
            "temperature"
        ]
        precipitationType = data["data"]["timelines"][0]["intervals"][0]["values"][
            "precipitationType"
        ]

        # Define a function to generate clothing advice based on temperature and precipitation
        def generate_clothing_advice(temperature, precipitation):
            if temperature < 50:
                return "It's cold. Wear a warm coat, gloves, and a hat."
            elif 50 <= temperature < 70:
                if precipitation > 0.1:
                    return "It's mild with precipitation. Wear a raincoat or carry an umbrella."
                else:
                    return "It's mild. A light jacket and jeans should be fine."
            else:
                if precipitation > 0.1:
                    return "It's warm with precipitation. Wear light layers and carry an umbrella."
                else:
                    return "It's warm. Shorts and a t-shirt will be comfortable."

        # Generate clothing advice based on temperature and precipitation
        advice = generate_clothing_advice(temperature, precipitationType)

        # Send a text message using Twilio (replace with your SMS provider)
        account_sid = "YOUR_ACCOUNT_SID"
        auth_token = "YOUR_ACCOUNT_TOKEN"
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            to="19892930837", from_="18883398512", body=advice
        )

        print(f"Sent SMS: {message.sid}")
    else:
        print("No 'data' key found in the API response.")
else:
    print(f"Error: HTTP {response.status_code} - {response.reason}")
    print(response.text)  # Print the response for inspection
