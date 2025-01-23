from bs4 import BeautifulSoup
import requests
import csv


gpu = input("Enter the Name of the GPU: ")
url = f"https://www.newegg.com/p/pl?Order=1&SrchInDesc={gpu}&N=100007709"


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


print("Sending request...")
result = requests.get(url, headers=headers)
print(f"Status Code: {result.status_code}")

# Parse HTML content
doc = BeautifulSoup(result.text, "html.parser")


gpu_containers = doc.find_all(class_="item-cell")
print(f"Found {len(gpu_containers)} GPU containers")



for index, gpu in enumerate(gpu_containers):
    try:
        # GPU name
        gpu_name_tag = gpu.find(class_="item-title")
        if gpu_name_tag:
            gpu_name = gpu_name_tag.text.strip()
        else:
            gpu_name = "N/A"

        # GPU price
        price_current_tag = gpu.find(class_="price-current")
        if price_current_tag and price_current_tag.strong:
            gpu_price = price_current_tag.strong.text.strip()
        else:
            gpu_price = "N/A"

        # affichge GPU name and price
        print(f"GPU Name: {gpu_name}")
        print(f"GPU Price: ${gpu_price}")
        print("-" * 30)  # for readability
    except Exception as e:
        print(f"Error extracting data: {e}")
        continue




# Save data in a CSV file
with open("gpu_data.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["GPU Name", "GPU Price"])  # Write header
    for gpu in gpu_containers:
        try:
            gpu_name = gpu.find(class_="item-title").text.strip()
            gpu_price = gpu.find(class_="price-current").strong.text.strip()
            writer.writerow([gpu_name, gpu_price])
        except AttributeError:
            continue



