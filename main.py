import requests
import json

url = "https://api-v3.thaiwater.net/api/v1/thaiwater30/public/rain_24h"

def fetch_data():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        geojson = {"type": "FeatureCollection", "features": []}
        
        # ข้อมูลอยู่ในคีย์ 'data' ตามโครงสร้างที่คุณให้มา
        items = data.get('data', [])
        
        for item in items:
            # ดึงพิกัดจากภายในคีย์ 'station'
            station_info = item.get('station', {})
            lat = station_info.get('tele_station_lat')
            lon = station_info.get('tele_station_long')
            
            if lat is not None and lon is not None:
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [float(lon), float(lat)]
                    },
                    "properties": {
                        "station_name": station_info.get('tele_station_name', {}).get('th', 'Unknown'),
                        "rain_24h": item.get('rain_24h', 0),
                        "province": item.get('geocode', {}).get('province_name', {}).get('th', 'N/A'),
                        "datetime": item.get('rainfall_datetime', 'N/A')
                    }
                }
                geojson['features'].append(feature)
        
        with open('rainfall_24h.geojson', 'w', encoding='utf-8') as f:
            json.dump(geojson, f, ensure_ascii=False, indent=4)
        print(f"Success: Processed {len(geojson['features'])} stations.")
    else:
        print(f"Error: API status {response.status_code}")

if __name__ == "__main__":
    fetch_data()
