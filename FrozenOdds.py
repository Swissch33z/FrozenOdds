import requests
import pyfiglet
from InquirerPy import inquirer
import csv
import os
import datetime

# Set up API key and endpoint
API_KEY = '8cee9511b1812e80f772588fc7bc77bd'  # Replace with the correct API key
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


# Function to calculate arbitrage opportunities
def calculate_arbitrage(matches):
    arbitrage_opportunities = []

    for match in matches:
        if 'home_team' not in match or 'away_team' not in match:
            continue

        home_team = match['home_team']
        away_team = match['away_team']

        # Store the odds from different bookmakers
        odds_dict = {}
        for bookmaker in match['bookmakers']:
            try:
                odds = bookmaker['markets'][0]['outcomes']
                home_odds = odds[0]['price']
                away_odds = odds[1]['price']
                odds_dict[bookmaker['title']] = (home_odds, away_odds)
            except (KeyError, IndexError):
                continue

        # Check for arbitrage opportunities between different bookmakers
        bookmakers = list(odds_dict.keys())
        for i in range(len(bookmakers)):
            for j in range(i + 1, len(bookmakers)):
                book1 = bookmakers[i]
                book2 = bookmakers[j]
                odds1 = odds_dict[book1]
                odds2 = odds_dict[book2]

                # Check if there's an arbitrage opportunity
                if odds1[0] > 1 / odds2[1] and odds2[0] > 1 / odds1[1]:
                    arbitrage_opportunities.append({
                        'match': f"{home_team} vs {away_team}",
                        'bookmakers': (book1, book2),
                        'odds': (odds1[0], odds2[1])
                    })

    return arbitrage_opportunities


# Function to display and/or save fetched odds in a cleaner format
def display_and_save_odds(data, sport, region):
    if not data:
        print("No data found!")
        return

    print(f"\nDisplaying odds for {sport} in the {region} region:\n")
    csv_data = [["Home Team", "Away Team", "Commence Time", "Bookmaker", "Odds (Home)", "Odds (Away)"]]

    for match in data:
        if 'home_team' not in match or 'away_team' not in match:
            print(f"Skipping match without teams: {match}")
            continue

        home_team = match['home_team']
        away_team = match['away_team']
        commence_time = match['commence_time']

        print(f"Match: {home_team} vs {away_team}")
        print(f"Commence Time: {commence_time}\n")

        for bookmaker in match['bookmakers']:
            bookmaker_name = bookmaker['title']
            try:
                odds = bookmaker['markets'][0]['outcomes']
                home_team_odds = odds[0]['price']
                away_team_odds = odds[1]['price']

                print(f"Bookmaker: {bookmaker_name}")
                print(f"{home_team}: {home_team_odds}, {away_team}: {away_team_odds}\n")

                # Add the odds to the csv data list
                csv_data.append([home_team, away_team, commence_time, bookmaker_name, home_team_odds, away_team_odds])

            except (KeyError, IndexError) as e:
                print(f"Error processing odds for {home_team} vs {away_team}: {str(e)}")

    # Check for arbitrage opportunities
    arbitrage_opportunities = calculate_arbitrage(data)
    if arbitrage_opportunities:
        print("\nArbitrage Opportunities Found:")
        for opportunity in arbitrage_opportunities:
            print(
                f"{opportunity['match']} - Bookmakers: {opportunity['bookmakers'][0]} and {opportunity['bookmakers'][1]} with odds {opportunity['odds'][0]} and {opportunity['odds'][1]}")
    else:
        print("No arbitrage opportunities found.")

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


