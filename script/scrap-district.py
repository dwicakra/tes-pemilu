import requests
import json
import os


def fetch_and_save_province_data(selected_province, base_dir):
    """
    Fetch data for the given province and save it as a JSON file.
    """
    url = f"https://sirekappilkada-obj-data.kpu.go.id/wilayah/pilkada/pkwkp/{selected_province}.json"

    # Output directory di luar folder skrip Python
    output_dir = os.path.join(base_dir, "district", selected_province)
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Fetch data from API
        response = requests.get(url)
        response.raise_for_status()

        try:
            # Parse JSON response
            data = response.json()
        except json.JSONDecodeError:
            print(f"Error: Response is not valid JSON for province {selected_province}")
            return None

        # Save data to JSON file
        output_path = os.path.join(output_dir, f"{selected_province}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"Data saved to {output_path}")
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {selected_province}: {e}")
        return None


def main():
    """
    Main function to read province codes and fetch their data.
    """
    # Tentukan path untuk file JSON dan direktori output
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Lokasi skrip
    base_dir = os.path.abspath(
        os.path.join(script_dir, "..")
    )  # Lokasi di luar folder skrip
    province_file = os.path.join(script_dir, "province.json")

    # Validasi dan load province.json
    try:
        with open(province_file, "r", encoding="utf-8") as f:
            provinces = json.load(f)
    except FileNotFoundError:
        print(f"Error: {province_file} not found")
        return
    except json.JSONDecodeError:
        print("Error: province.json contains invalid JSON")
        return

    # Fetch dan simpan data untuk setiap provinsi
    for province in provinces:
        selected_province = province["kode"]
        print(f"Fetching data for province code: {selected_province}")
        result = fetch_and_save_province_data(selected_province, base_dir)
        if result is None:
            print(f"Skipping province {selected_province}")


if __name__ == "__main__":
    main()
