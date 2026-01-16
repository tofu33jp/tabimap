import geopandas as gpd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shapely.geometry import box

app = FastAPI()

# CORS設定（JSからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# データの読み込みとインデックス作成
print("Loading GeoJSON...")
gdf = gpd.read_file("points.geojson")
# 地理インデックス(Spatial Index)を作成して検索を爆速にする
spatial_index = gdf.sindex

@app.get("/points")
def get_points(west: float, south: float, east: float, north: float):
    # 現在の表示範囲の矩形を作成
    bbox = box(west, south, east, north)
    
    # 範囲内に含まれるインデックスを抽出
    possible_matches_index = list(spatial_index.intersection(bbox.bounds))
    subset = gdf.iloc[possible_matches_index]
    
    # さらに正確にフィルタリング（境界線上の判定）
    precise_matches = subset[subset.intersects(bbox)]
    
    # GeoJSON形式で返す
    return precise_matches.to_json()

if __name__ == "__main__":
    # import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    pass
