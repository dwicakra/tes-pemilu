import requests
import json
import os
from tqdm import tqdm


def fetch_and_save_district_data(selected_province, selected_district, base_dir):
    """
    Fetch data for the given district and save it as a JSON file.
    """
    url = f"https://sirekappilkada-obj-data.kpu.go.id/pilkada/hhcw/pkwkp/{selected_province}/{selected_district}.json"

    # Create output directory outside of the script folder
    output_dir = os.path.join(base_dir, "pkwkp", selected_province)
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Fetch data from the API
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Save data to a JSON file
        output_path = os.path.join(output_dir, f"{selected_district}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return data

    except requests.exceptions.RequestException as e:
        print(
            f"Error fetching data for province {selected_province}, district {selected_district}: {e}"
        )
        return None


def get_districts_for_province(selected_province, base_dir):
    """
    Get the list of districts for the given province.
    """
    try:
        # Read district data from the corresponding province file
        district_file = os.path.join(
            base_dir, "district", selected_province, f"{selected_province}.json"
        )
        with open(district_file, "r", encoding="utf-8") as f:
            districts = json.load(f)
        return districts
    except FileNotFoundError:
        print(f"No district file found for province {selected_province}")
        return []


def main():
    """
    Main function to fetch and save data for all districts in all provinces.
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

    # Create progress bar for provinces
    province_pbar = tqdm(provinces, desc="Processing provinces")

    # Loop through each province
    for province in province_pbar:
        selected_province = province["kode"]
        province_pbar.set_description(f"Processing province {selected_province}")

        # Get districts for this province
        districts = get_districts_for_province(selected_province, base_dir)

        # Create progress bar for districts within this province
        district_pbar = tqdm(
            districts, desc=f"Districts in {selected_province}", leave=False
        )

        # Process each district
        for district in district_pbar:
            selected_district = district["kode"]
            district_pbar.set_description(f"Processing district {selected_district}")

            result = fetch_and_save_district_data(
                selected_province, selected_district, base_dir
            )
            if result is None:
                continue


if __name__ == "__main__":
    main()
