## How it works

#### `ocr.py`
 - The hand cropped table gets uploaded to the Google Cloud Vision API. This returns a list of "words" that are parts of the numbers.
 - Those words and their position in the photo are then saved to a json file

#### `parse.py`
 - The json file gets loaded.
 - The locations of the rows and columns get detected.
 - Every word gets put in the correct row and column. Since multiple words can make up a number, some also get combined.
 - Characters that are known to cause issues get replaced with the correct ones. (Ex: S => 5)
 - Sometimes the `E` and signs don't get detected, so there is some correction done based on the formatting and known number of decimals places. (If that fails => mark red)
 - All numbers get cast to float (or marked red).
 - Columns get checked if they are in strictly ascending or descending order. Outliers get marked red.
 - Everything gets saved to an excel table.
 
## Running it

 1. Go to the Google Cloud Console and create a project with Cloud Vision enabled. Then download the key file and add it to your environment variables
 2. Crop one table (half a page) including column names and save it to a JPEG
 3. Edit `ocr.py` to open that JPEG
 4. Run `python ocr.py`
 5. Optionally edit `parse.py` to take in a differently named JSON file or change the Excel file name
 6. Run `python parse.py`