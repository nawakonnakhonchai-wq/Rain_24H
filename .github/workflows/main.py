import requests
import json

# URL จาก สสน.
url = "https://api-v3.thaiwater.net/api/v1/thaiwater30/public/rain_24h"

# ดึงข้อมูล
response = requests.get(url)
data = response.json()

# โครงสร้าง GeoJSON
geojson = {
    "type": "FeatureCollection",
    "features": []
}

# วนลูปข้อมูลเพื่อแปลงเป็น Feature
# (หมายเหตุ: ปรับคีย์ 'data' ตามโครงสร้าง JSON จริงที่ API ตอบกลับมา)
for item in data['data']:
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [float(item['long']), float(item['lat'])]
        },
        "properties": {
            "station_name": item['station_name'],
            "rain_24h": item['rain_24h'],
            "province": item.get('province', 'N/A')
        }
    }
    geojson['features'].append(feature)

# บันทึกเป็นไฟล์ .geojson
with open('rainfall_24h.geojson', 'w', encoding='utf-8') as f:
    json.dump(geojson, f, ensure_ascii=False, indent=4)

print("สร้างไฟล์ rainfall_24h.geojson เรียบร้อยแล้ว!")
