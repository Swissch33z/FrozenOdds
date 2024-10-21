import requests
import pyfiglet
from InquirerPy import inquirer
import csv
import os
import datetime

# Set up API key and endpoint
API_KEY = 'your_api_key'  # Replace with the correct API key
BASE_URL = 'https://api.the-odds-api.com/v4/sports/'

# Banner display using pyfiglet
def display_banner():
    banner = pyfiglet.figlet_format("Odds Scraper")
    print(banner)
    print("Welcome to the Betting Odds Scraper!\n")

# Function to get user choices using InquirerPy for the menu
def get_user_choices():
    sports = {
        "Soccer (EPL)": "soccer_epl",
        "Basketball (NBA)": "basketball_nba",
        "Tennis": "tennis"
    }

    regions = ["us", "uk", "eu", "au"]  # Add more regions as needed

    # Sport selection
    sport_choice = inquirer.select(
        message="Select a sport:",
        choices=list(sports.keys())
    ).execute()

    # Region selection
    region_choice = inquirer.select(
        message="Select a region:",
        choices=regions
    ).execute()

    return sports[sport_choice], region_choice

# Function to fetch odds data from the OddsAPI
def fetch_odds(sport, region):
    url = f'{BASE_URL}{sport}/odds'
    params = {
        'apiKey': API_KEY,
        'regions': region,
        'markets': 'h2h',  # Head-to-head odds
        'oddsFormat': 'decimal'  # Choose between decimal, American, etc.
    }
    
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching odds data: {response.status_code}, {response.text}")
        return None

# Function to display and/or save fetched odds
def display_and_save_odds(data, sport, region):
    if not data:
        print("No data found!")
        return

    print(f"\nDisplaying odds for {sport} in the {region} region:\n")
    # Create a list to store CSV data if needed
    csv_data = [["Team 1", "Team 2", "Bookmaker", "Odds Team 1", "Odds Team 2"]]

    for match in data:
        teams = match['teams']
        for bookmaker in match['bookmakers']:
            odds = bookmaker['markets'][0]['outcomes']
            team1_odds = odds[0]['price']
            team2_odds = odds[1]['price']

            print(f"Match: {teams[0]} vs {teams[1]}")
            print(f"Bookmaker: {bookmaker['title']}")
            print(f"{teams[0]}: {team1_odds}, {teams[1]}: {team2_odds}\n")

            # Add the odds to the csv data list
            csv_data.append([teams[0], teams[1], bookmaker['title'], team1_odds, team2_odds])

    # Ask user if they want to save the data to a CSV file
    save_choice = inquirer.confirm(message="Do you want to save the odds data to a CSV file?", default=True).execute()
    
    if save_choice:
        save_to_csv(csv_data)

# Function to save data to CSV
def save_to_csv(data):
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"odds_data_{timestamp}.csv"
    filepath = os.path.join(os.getcwd(), filename)

    # Write data to CSV
    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print(f"Data saved to {filepath}")

# Main function to run the entire process
def main():
    display_banner()  # Display the banner
    sport, region = get_user_choices()  # Get user input from the menu
    print(f"\nFetching odds for {sport} in the {region} region...\n")
    data = fetch_odds(sport, region)  # Fetch the odds from the API
    display_and_save_odds(data, sport, region)  # Display and save the odds data

if __name__ == "__main__":
    main()
