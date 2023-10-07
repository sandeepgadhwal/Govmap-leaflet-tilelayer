import geopandas as gpd
import numpy as np
from shapely.geometry import box
from argparse import ArgumentParser
from pathlib import Path

tiling_config = {
    "srs": "EPSG:2039",
    "res": [     
        793.751587503175,
        264.583862501058,
        132.291931250529,
        66.1459656252646,
        26.4583862501058,
        13.2291931250529,
        6.61459656252646,
        2.64583862501058,
        1.32291931250529,
        0.661459656252646,
        0.330729828126323,
        0.132291931250529,
        0.0661459656252646
    ],
    "tile_size": [256, 256],
    # "bbox": [-166037.584370664, 293562.885588639, 578501.404707314, 925389.149241166], ## Region around israel
    "bbox": [125435.5744279373320751, 377716.3830031852703542, 263880.0101924073533155, 797255.3193292325595394],
    "origin": [-5403700, 7116700]
}

def main(config, output_format):
    xmin, ymin, xmax, ymax = config['bbox']
    row_store = []
    geometries = []
    for zoom_level, res in enumerate(config['res']):
        print(f"--Generating tiles for zoom level: {zoom_level}/{len(config['res'])} | tiles count: {len(row_store)} ...")
        tile_size_res = config['tile_size'][0]*res
        row_offset = int((config['origin'][1]-ymax)//tile_size_res)
        col_offset = int((xmin-config['origin'][0])//tile_size_res)
        row_ymax = config['origin'][1]-row_offset*tile_size_res
        col_xmin = config['origin'][0]+col_offset*tile_size_res
        for row, tile_ymax in enumerate(np.arange(row_ymax, ymin, tile_size_res*-1)):
            _row = row+row_offset
            for col, tile_xmin in enumerate(np.arange(col_xmin, xmax, tile_size_res)):
                geometries.append(box(tile_xmin, tile_ymax-tile_size_res, tile_xmin+tile_size_res, tile_ymax))
                _col = col+col_offset
                row_hex = format(_row, 'x')
                col_hex = format(_col, 'x')
                layer = "M2023ORT3TS"
                ext = "jpg"
                url = f"https://cdn.govmap.gov.il/{layer}/L{str(zoom_level).zfill(2)}/R{row_hex.zfill(8)}/C{col_hex.zfill(8)}.{ext}"
                row_store.append({
                    "zoom_level": zoom_level,
                    "resolution": res,
                    "row": _row,
                    "col": _col,
                    "row_hex": row_hex,
                    "col_hex": col_hex,
                    "url": url,
                    # "xmin":tile_xmin,
                    # "xmax":tile_xmin+tile_size_res,
                    # "ymin":tile_ymax-tile_size_res,
                    # "ymax":tile_ymax
                })        
    #
    fp = Path(f"./tile_matrix.{output_format}").absolute()
    print(f"--Generated total {len(row_store)} tiles | Writing to disk now, path: {fp} ...")
    df = gpd.GeoDataFrame(row_store, geometry=geometries, crs=config['srs'])
    df.to_file(fp)
    print("All Done !")

if __name__=="__main__":
    parser = ArgumentParser()
    parser.add_argument('--output-format', type=str, default='geojson', required=False)
    parser.add_argument('--bbox', type=str, default="125435.5744279373320751,377716.3830031852703542,263880.0101924073533155,797255.3193292325595394", required=False)
    options = parser.parse_args()
    tiling_config['bbox'] = [float(x) for x in options.bbox.split(',')]
    main(tiling_config, options.output_format)
