import requests
import json
import os
from tqdm import tqdm


def fetch_and_save_district_data(selected_province, selected_district, base_dir):
    """
    Fetch and save data for a specific district.
    """
    url = f"https://sirekappilkada-obj-data.kpu.go.id/pilkada/hhcw/pkwkk/{selected_province}/{selected_district}.json"

    # Output directory di luar folder skrip Python
    output_dir = os.path.join(base_dir, "pkwkk", selected_province)
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Fetch data from API
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Save data to JSON file
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
    Get the list of districts for a given province.
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
    # Tentukan direktori dasar
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Lokasi skrip
    base_dir = os.path.abspath(os.path.join(script_dir, ".."))  # Di luar folder skrip
    province_file = os.path.join(script_dir, "province.json")

    # Validasi keberadaan province.json
    try:
        with open(province_file, "r", encoding="utf-8") as f:
            provinces = json.load(f)
    except FileNotFoundError:
        print(f"Error: {province_file} not found")
        return
    except json.JSONDecodeError:
        print("Error: province.json contains invalid JSON")
        return

    # Progress bar untuk provinsi
    province_pbar = tqdm(provinces, desc="Processing provinces")

    # Loop melalui setiap provinsi
    for province in province_pbar:
        selected_province = province["kode"]
        province_pbar.set_description(f"Processing province {selected_province}")

        # Dapatkan daftar distrik untuk provinsi ini
        districts = get_districts_for_province(selected_province, base_dir)

        # Progress bar untuk distrik dalam provinsi ini
        district_pbar = tqdm(
            districts, desc=f"Districts in {selected_province}", leave=False
        )

        # Proses setiap distrik
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
