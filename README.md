
# ❄️ FrozenOdds Scraper

FrozenOdds Scraper is a streamlined, easy-to-use tool that allows users to fetch live betting odds from various sports betting sites using available APIs. This tool provides a clean interface with menu options for users to easily select a sport, region, and get real-time betting odds in a user-friendly format. Designed to be robust and user-friendly, it offers an intuitive experience for both beginners and experienced users alike.

## 🧊 Features
- **Sports Betting Odds Scraper**: Fetches live odds for a variety of sports and matches.
- **Multiple Regions Support**: Allows scraping of odds for different regions.
- **API Integration**: Utilizes official APIs from betting sites for reliable and legal scraping.
- **Easy-to-Use Menu**: Offers a clean, text-based menu for easy navigation.
- **Error Handling**: Includes error messages and validations to ensure smooth operation.
- **Customizable**: Simple to configure for scraping additional sports, regions, or betting sites.
- **Banner Title**: Fun, welcoming banner design when the tool starts up.

## 📦 Installation

To get started with the FrozenOdds Scraper, follow these steps:

### Prerequisites:
- Python 3.x
- API key from a supported betting API provider (e.g., OddsAPI)

### Clone the Repository:
```bash
git clone https://github.com/Swissch33z/FrozenOdds.git
cd frozenodds-scraper
```

### Install Dependencies:
Install the required Python libraries using pip:
```bash
pip install -r requirements.txt
```

### Set Up Your API Key:
You'll need to obtain an API key from the betting site or API provider you're scraping data from. For example, with OddsAPI:
1. Sign up at OddsAPI.
2. Get your API key after registering.
3. Add your API key to the `.env` file (create it if it doesn't exist):
```bash
API_KEY=your_api_key_here
```

### Requirements File (`requirements.txt`):
```txt
requests==2.28.1
python-dotenv==0.21.0
tabulate==0.9.0  # For pretty printing results
```

*Optional*:
For scraping additional sites without APIs, you may need tools like Selenium or BeautifulSoup.

## ⚙️ Usage

### Running the Scraper
Simply run the Python script to start the FrozenOdds Scraper:
```bash
python FrozenOdds.py
```

### Welcome Screen:
When you start the tool, you will see a welcome banner like this:

```markdown
  ___      _     _       ____
 / _ \  __| | __| |___  / ___|  ___ _ __ __ _ _ __   ___ _ __
| | | |/ _` |/ _` / __| \___ \ / __| '__/ _` | '_ \ / _ \ '__|
| |_| | (_| | (_| \__ \  ___) | (__| | | (_| | |_) |  __/ |
 \___/ \__,_|\__,_|___/ |____/ \___|_|  \__,_| .__/ \___|_|
                                             |_|

Welcome to the Betting Odds Scraper!
```

### Menu:
You will be prompted to select a sport and region to fetch the odds:
```bash
Select a sport: Soccer (EPL)
Select a region: UK
```
After you select your options, the tool will fetch the latest betting odds:
```makefile
Fetching odds for soccer_epl in the uk region...

Match: Arsenal vs Chelsea
Arsenal: 2.10
Chelsea: 3.50
```

### Command-Line Options:
In addition to the interactive menu, you can pass arguments via the command line for quick scraping:
```bash
python frozenodds_scraper.py --sport soccer_epl --region uk
```

### Error Handling:
The tool gracefully handles common errors such as invalid inputs, missing API keys, and API request issues, providing user-friendly error messages like:
```javascript
Error: Invalid sport or region selected.
```

## 📁 Project Structure

```bash
frozenodds-scraper/
│
├── frozenodds_scraper.py        # Main script for scraping and running the menu
├── requirements.txt             # Python dependencies
├── README.md                    # Detailed project documentation
├── .env                         # API key file (not included in Git)
├── LICENSE                      # License information
```

## 🛠️ Configuration

You can easily configure the tool to scrape additional sports or regions by editing the `sports_config.json` file (or similar config structure):

```json
{
    "sports": {
        "soccer_epl": {
            "name": "Soccer (EPL)",
            "region": ["uk", "us", "eu"]
        },
        "basketball_nba": {
            "name": "Basketball (NBA)",
            "region": ["us", "ca"]
        }
    }
}
```

To add a new sport or region, just update this JSON file with the appropriate API-supported endpoints.

## 🛡️ Legal and Ethical Use

Please ensure that you are using this tool in compliance with all applicable laws and the terms of service of the websites and APIs you are scraping data from. Always check with the betting site to confirm that scraping is allowed and legal.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙌 Contributions

Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to contribute.

