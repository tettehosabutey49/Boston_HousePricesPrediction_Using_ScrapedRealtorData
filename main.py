import os
import re
import csv

def extract_properties(html_content):
    # This regex pattern matches the RealEstateListing JSON objects
    pattern = r'\{"@type":\["RealEstateListing"\].*?"mainEntity":\{.*?\}\}'
    matches = re.findall(pattern, html_content)
    
    properties = []
    
    for match in matches:
        try:
            # Extract key fields using regex
            name = re.search(r'"name":"(.*?)"', match).group(1)
            price = re.search(r'"price":"(.*?)"', match).group(1)
            url = re.search(r'"url":"(.*?)"', match).group(1)
            image = re.search(r'"image":"(.*?)"', match).group(1)
            
            # Extract mainEntity fields
            bedrooms = re.search(r'"numberOfBedrooms":(\d+)', match)
            bedrooms = bedrooms.group(1) if bedrooms else ''
            
            sqft = re.search(r'"value":(\d+)', match)
            sqft = sqft.group(1) if sqft else ''
            
            address = re.search(r'"streetAddress":"(.*?)"', match)
            address = address.group(1) if address else ''
            
            city = re.search(r'"addressLocality":"(.*?)"', match)
            city = city.group(1) if city else ''
            
            state = re.search(r'"addressRegion":"(.*?)"', match)
            state = state.group(1) if state else ''
            
            zip_code = re.search(r'"postalCode":"(.*?)"', match)
            zip_code = zip_code.group(1) if zip_code else ''
            
            properties.append({
                'name': name,
                'price': price,
                'url': url,
                'image': image,
                'bedrooms': bedrooms,
                'sqft': sqft,
                'address': address,
                'city': city,
                'state': state,
                'zip': zip_code
            })
            
        except Exception as e:
            print(f"Error processing match: {e}")
            continue
    
    return properties

def process_folder(folder_path):
    all_properties = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.html'):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    html_content = file.read()
                    properties = extract_properties(html_content)
                    if properties:
                        print(f"Found {len(properties)} properties in {filename}")
                        all_properties.extend(properties)
                    else:
                        print(f"No properties found in {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    return all_properties

def save_to_csv(properties, output_file):
    if not properties:
        print("No properties found to save.")
        return
    
    fieldnames = [
        'name', 'price', 'url', 'image',
        'bedrooms', 'sqft', 'address', 
        'city', 'state', 'zip'
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(properties)
    
    print(f"Successfully saved {len(properties)} properties to {output_file}")

if __name__ == '__main__':
    input_folder = 'alldata'
    output_file = 'properties_regex.csv'
    
    if not os.path.exists(input_folder):
        print(f"Error: Folder '{input_folder}' does not exist.")
    else:
        properties = process_folder(input_folder)
        save_to_csv(properties, output_file)