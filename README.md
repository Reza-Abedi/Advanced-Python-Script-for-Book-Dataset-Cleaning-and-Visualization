This Python script is designed to thoroughly clean and enhance a dataset containing information about books. The cleaning process addresses multiple aspects, including the date of publication, place of publication, title, and author names. Various techniques, such as regular expressions, string manipulation, and data imputation, are employed to ensure the accuracy and consistency of the dataset.

The script begins by loading the dataset from an Excel file and dropping unnecessary columns. It then proceeds to clean the date of publication by extracting valid four-digit years and handling cases where the date is embedded in the place of publication. The place of publication is standardized, with special attention given to locations like London, Oxford, and Newcastle-upon-Tyne. Non-ASCII characters are removed from the place names, and inconsistent formatting is corrected.

Title cleaning involves extracting author names from the titles using regular expressions, providing additional information to fill missing author names. The title itself undergoes formatting adjustments, such as capitalization and removal of unnecessary characters.

The final step involves cleaning and formatting author names, dropping unnecessary columns, and saving the cleaned dataset to an Excel file.

The script also offers interactive data visualization options. Users can choose to generate graphs displaying the number of publications over the years, the number of books per author in a horizontal bar chart, or the number of books per city in another horizontal bar chart. The interactive nature allows users to explore and analyze specific aspects of the dataset dynamically.

This comprehensive script serves as a powerful tool for data cleaning, ensuring data quality, and provides an interactive platform for exploring and visualizing key aspects of the book dataset. The cleaned dataset is then ready for further analysis or integration into larger projects.


--->Technical Details

** Data Loading and Cleanup:
Loads the dataset from an Excel file (books.xlsx).
Removes unnecessary columns like 'Edition Statement,' 'Corporate Author,' and others.
Cleans the 'Date of Publication' column using regular expressions to extract valid four-digit years. Handles cases where the date is found in the 'Place of Publication.'

** Place of Publication Standardization:
Standardizes the 'Place of Publication,' focusing on locations like London, Oxford, and Newcastle-upon-Tyne.
Removes non-ASCII characters and corrects inconsistent formatting.

** Title and Author Cleaning:
Extracts author names from titles using regular expressions and provides additional information to fill missing author names.
Standardizes title formatting, capitalization, and removes unnecessary characters.

** Final Cleaning Steps:
Formats and cleans author names, handling variations in data.
Drops unnecessary columns and saves the cleaned dataset to an Excel file (book_cleaned.xlsx).

**Interactive Data Visualization:

Offers an interactive menu for users to choose visualization options.
Generates a line plot showing the number of publications over the years.
Creates a horizontal bar chart illustrating the number of books per author.
Provides a horizontal bar chart displaying the number of books per city.

**User Interaction:
Utilizes a continuous loop for user interaction, allowing them to explore different visualization options.
Ensures a dynamic and user-friendly experience for exploring and understanding the dataset.
This script is a comprehensive tool for data scientists and analysts working with book datasets. Its advanced cleaning techniques and interactive visualizations make it valuable for exploring patterns and trends within the data.
