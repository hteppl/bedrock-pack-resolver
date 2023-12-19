import json
import os

from PIL import Image


# Load the manifest JSON data
def get_manifest(path: str) -> json:
    with open(path + '/manifest.json', 'r') as file:
        return json.load(file)


def write_file(output_path: str, name: str, content: str) -> None:
    with open(os.path.join(output_path, name), 'w', encoding='utf-8') as file:
        file.write(content)


def create_markdown_table(glyph_data: dict) -> str:
    glyph = glyph_data['name']
    name = glyph.split('_')[1]
    table = '| Unicode | Hex | Image |\n| --------- | --------- | --------- |\n'
    
    for row in glyph_data['data']:
        char = f"\\u{name}{row['pos']}"
        let = bytes(char, 'utf-8').decode('unicode-escape')
        table += f"| {let} | {char} | ![]({row['img']}) |\n"
    
    return table


def update_version_patch(manifest: json) -> None:
    # Check if the object has the version key in hierarchy
    version = manifest.get('header', {}).get('version')
    if version:
        manifest['header']['version'][-1] = int(version[-1]) + 1
    else:
        raise ValueError('manifest.json does not contain the version')


def resolve_glyphs(data_path: str, output_path: str):
    result = []
    font_path = os.path.join(data_path, 'font')
    files = [f for f in os.listdir(font_path) if f.startswith('glyph') and f.endswith('.png')]
    
    for file in files:
        file_path = os.path.join(font_path, file)
        data = split_and_save_images(file_path, output_path)
        filename = os.path.splitext(os.path.basename(file))[0]
        result.append({'name': filename, 'data': data})
    
    return result


def split_and_save_images(input_path: str, output_path: str):
    result = []
    
    with Image.open(input_path) as img:
        basename = os.path.basename(input_path)
        filename = basename.split('.')[0]
        glyph = filename.split('_')[1]
        
        # Get the width and height
        width, height = img.size
        
        # Check the width and height
        if width != height or width % 128 != 0 or height % 128 != 0:
            return
        
        # Create output path, if not exists
        os.makedirs(output_path, exist_ok=True)
        side_size = int(width / 128 * 8)
        
        for j in range(0, height, side_size):
            for i in range(0, width, side_size):
                box = (i, j, i + side_size, j + side_size)
                tile = img.crop(box)
                
                if is_empty_tile(tile):
                    continue
                
                x = j // side_size
                y = i // side_size
                path = to_hex(x) + to_hex(y)
                
                file_name = f'{glyph}{path}.png'
                img_path = os.path.join(output_path, file_name)
                
                # Save the tile
                tile.save(img_path)
                
                # Add information to the result list
                result.append({'pos': path, 'img': img_path})
    
    return result


def to_hex(value: int) -> str:
    return hex(value)[2:].upper()


# Check if all pixels is empty
def is_empty_tile(tile):
    pixel_data = list(tile.getdata())
    return all(pixel[3] == 0 for pixel in pixel_data)


def main():
    data = resolve_glyphs('rp-anarchy-master', 'rp_data')
    
    for glyph in data:
        table = create_markdown_table(glyph)
        write_file('', f"{glyph['name']}.md", table)


if __name__ == '__main__':
    main()
