import requests
from lxml import html
import json
from urllib.parse import urlparse


xpath_mapping = {
    "mahoot-leather.ir": '//*[@id="productPrice38888"]/div/span[2]',
}

def extract_data(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc  # Extract the domain from the URL

    # Get the corresponding XPath for the domain
    xpath = xpath_mapping.get(domain)

    if not xpath:
        print(f"No XPath found for the domain: {domain}")
        return

    response = requests.get(url)
    
    if response.status_code != 200:  
        print(f"Error receiving page, status code: {response.status_code} for URL: {url}")
        return
    
    tree = html.fromstring(response.content)  # Parse the HTML page
    
    data = tree.xpath(xpath)
    
    if data:  # Check if data was extracted
        extracted_data = data[0].text_content().strip()  # Use text_content() to get the string
    else:
        extracted_data = "No data found with this XPath."
    
    return {"url": url, "extracted_data": extracted_data}

def extract_multiple_data(urls):
    results = []
    
    for url in urls:
        result = extract_data(url)
        if result:
            results.append(result)

    # Save all results to a JSON file
    with open('bahBah.json', 'w', encoding='utf-8') as f:  
        json.dump(results, f, ensure_ascii=False, indent=4)
    
    print("All data was successfully saved in the output.json file.")


urls = [
    "https://mahoot-leather.ir/smartwatch/apple-watch-4-40mm/Apple%20Watch-4-(40mm)-White-Wood",
]

extract_multiple_data(urls)
