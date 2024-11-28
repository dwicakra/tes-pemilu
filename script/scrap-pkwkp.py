import requests
import json
import os


def fetch_and_save_province_data(selected_province, base_dir):
    """
    Fetch data for the selected province and save it as a JSON file.
    """
    url = f"https://sirekappilkada-obj-data.kpu.go.id/pilkada/hhcw/pkwkp/{selected_province}.json"

    # Create output directory outside of the script folder
    output_dir = os.path.join(base_dir, "pkwkp", selected_province)
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Fetch data from the API
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Save data to a JSON file
        output_path = os.path.join(output_dir, f"{selected_province}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"Data saved to {output_path}")
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for province {selected_province}: {e}")
        return None


def main():
    """
    Main function to fetch and save data for all provinces.
    """
    # Determine the base directory outside the script folder
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Location of the script
    base_dir = os.path.abspath(
        os.path.join(script_dir, "..")
    )  # Parent folder (outside the script folder)
    province_file = os.path.join(script_dir, "province.json")

    # Validate the existence of province.json
    try:
        with open(province_file, "r", encoding="utf-8") as f:
            provinces = json.load(f)
    except FileNotFoundError:
        print(f"Error: {province_file} not found")
        return
    except json.JSONDecodeError:
        print("Error: province.json contains invalid JSON")
        return

    # Loop through each province and fetch data
    for province in provinces:
        selected_province = province["kode"]
        print(f"Fetching data for province code: {selected_province}")
        result = fetch_and_save_province_data(selected_province, base_dir)
        if result is None:
            print(f"Skipping province {selected_province}")
            continue


if __name__ == "__main__":
    main()
