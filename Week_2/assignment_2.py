'''
Interactive app for exploring Mars rover photos, allowing users to select a rover,
specify a date, and view photos with pagination and navigation options.
Author: Mandeep
Created: 2024-09-03
Updated: 2024-09-05
'''

# Imports
from requests import get
import json
from PIL import Image
from io import BytesIO
from menu import Menu
from dateutil.parser import parse

# Variables
API_KEY = "on6dPadJ66QW3WF8LVp2Bi5bgO4S8FoyS3kuTCJY"
url_rovers = f"https://api.nasa.gov/mars-photos/api/v1/rovers?api_key={API_KEY}"
all_rovers = get(url_rovers).json()

def display_photo(url):
    """Displays the photo found at url."""
    img_resp = get(url)
    img = Image.open(BytesIO(img_resp.content))
    img.show()
    img.close()


def choose_rover():
    """Menu to choose a rover and enter a date."""
    rover_options = []

    for rover in all_rovers['rovers']:
        rover_options.append((rover['name'], lambda name=rover['name']: prompt_date(name)))

    rover_options.append(("Exit", lambda: exit()))
    menu = Menu(options=rover_options, title="Choose a Mars Rover", prompt="Select a rover:")
    menu.open()

def prompt_date(name):
    """Prompt user for a date and fetch available photos."""
    try:
        date = input(f"Enter a date (YYYY-MM-DD) for {name}: ")

        if not parse(date):
            raise ValueError

        photos = fetch_photos(name, date)

        if not photos:
            raise FileNotFoundError

    except FileNotFoundError:
        if not photos:
            print(f"No photos found for {name} on {date}.")
            input("Press Enter to return to rover selection...")
            choose_rover()

    except ValueError:
        print("The date format is incorrect. Please enter the date in YYYY-MM-DD format.")
        input("Press Enter to return to rover selection...")
        choose_rover()

    except Exception as e:
        print(f"{e}, Something Happened, I guess!!!")

    if photos:
        paginate_photos(photos, name, date)


def fetch_photos(name, date):
    """Fetches photos for the selected rover and date."""
    rover_pics = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{name}/photos?earth_date={date}&api_key={API_KEY}"
    response_pics = get(rover_pics).json()

    if 'photos' not in response_pics or not response_pics['photos']:
        return []

    return response_pics['photos']


def paginate_photos(photos, name, date):
    """Paginate photos in batches of 10, with Next/Back options."""
    total_photos = len(photos)
    current_page = 0
    photos_per_page = 10

    def show_page():
        start = current_page * photos_per_page
        end = start + photos_per_page
        page_photos = photos[start : end]

        photos_options = []

        try:
            for i, photo in enumerate(page_photos, start=start):
                img_src = photo['img_src']

                if img_src.endswith("-BR.JPG"):
                    raise FileExistsError
                else:
                    photos_options.append((f"Photos {i + 1}", lambda url = photo['img_src']: display_photo(url), ))

        except FileExistsError:
            print(f"Images for {name} points to an article and can't be displayed.")

        photos_options.append(("Go Back", lambda: choose_rover()))
        photos_options.append(("Exit", lambda: exit()))

        # Add navigation options if applicable
        if current_page > 0:
            photos_options.append(("Back", lambda: navigate(-1)))
        if end < total_photos:
            photos_options.append(("Next", lambda: navigate(1)))

        # Display the menu
        photo_menu = Menu(options=photos_options, title=f"Photos for {name} on {date} (Page {current_page+1})", prompt="Choose a photo:", auto_clear=False)
        photo_menu.open()

    def navigate(direction):
        nonlocal current_page
        current_page += direction
        show_page()

    show_page()

# Main function to open the rover selection menu
def main():
    choose_rover()

# Run the app
if __name__ == "__main__":
    main()



