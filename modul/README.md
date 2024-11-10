# Web Scraper Project

This project is an advanced, asynchronous web scraping tool written in Python. It is designed to fetch data from a list of URLs based on predefined XPath expressions, normalize the data, and export the results to JSON files. The scraper can handle multiple domains and provides detailed error reporting for failed scrapes.

---

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Error Handling](#error-handling)
- [Output Files](#output-files)
- [Future Improvements](#future-improvements)

---

## Features
- **Asynchronous Processing**: Efficiently handles multiple URLs at once.
- **XPath-based Data Extraction**: Uses custom XPath expressions for data extraction from HTML.
- **Normalization Pipeline**: Standardizes extracted data with various normalizers.
- **Error Logging and Handling**: Logs errors for failed URLs, such as missing XPath data or empty results.
- **Flexible Configuration**: Easily customizable for various domains by updating the `xpath_data.json` file.

---

## Technologies Used
- **Python 3.x**
- **Asyncio**: For managing asynchronous tasks.
- **Pathlib**: For handling file paths across platforms.
- **JSON**: For data storage and configuration.
- **Custom Normalization Modules**: Includes `EmptyNormalizer`, `StripNormalizer`, `CurrencyNormalizer`, and `PCNormalizer`.

---

## Project Structure

- **`scrapper` class**: Manages the scraping process, using the fetcher, XPath repo, and normalizers.
- **Modules**:
  - **`fetcher`**: Retrieves HTML content from each URL.
  - **`JsonWebRepo`**: Handles the JSON file containing the XPath expressions for each target domain.
  - **`JsonExporter`**: Exports JSON data for successful and failed scrapes.
  - **`Normalizers`**:
    - **`EmptyNormalizer`**: Filters out empty values.
    - **`StripNormalizer`**: Trims whitespace.
    - **`CurrencyNormalizer`**: Standardizes currency formats.
    - **`PCNormalizer`**: Converts specific values (e.g., percentages) into a standardized format.
  
---

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd web-scraper
