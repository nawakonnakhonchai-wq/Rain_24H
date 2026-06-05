import requests
import json

# URL API
url = "https://api-v3.thaiwater.net/api/v1/thaiwater30/public/rain_24h"

def fetch_data():
    response = requests.get(url)
    data = response.json()
    
    # สร้างโครงสร้าง GeoJSON
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    
    # ดึงค่า data ออกมา (ถ้า API ส่งมาในรูปแบบ {'data': [...]})
    items = data.get('data', [])
    
    for item in items:
        # ตรวจสอบว่ามี lat/long หรือไม่
        if item.get('lat') and item.get('long'):
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(item['long']), float(item['lat'])]
                },
                "properties": {
                    "station_name": item.get('station_name', 'Unknown'),
                    "rain_24h": item.get('rain_24h', 0),
                    "province": item.get('province_name', 'N/A')
                }
            }
            geojson['features'].append(feature)
    
    # บันทึกไฟล์
    with open('rainfall_24h.geojson', 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    fetch_data()
