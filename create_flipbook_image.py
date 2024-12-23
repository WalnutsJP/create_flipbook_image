#!/usr/bin/env python
#coding:utf-8

# ---------------------------------------------------------------------------
# 連番画像が保存されているフォルダからFlipbook画像を作成するスクリプト
# ---------------------------------------------------------------------------

import math
import os
import argparse
from PIL import Image

# 連番画像からFlipbook画像を作成
def create_flipbook_image(image_array, page_count_x=0, padding=(0,0)):
    # image_arrayが配列でない場合はエラー
    if type(image_array) is not list:
        return None
    # image_arrayの要素数が0の場合はエラー
    image_array_count = len(image_array)
    if image_array_count < 1:
        return None
    # X軸Y軸のページ数を計算
    if page_count_x < 1:
        page_count_x = int(math.ceil(math.sqrt(image_array_count)))
    page_count_y = image_array_count // page_count_x
    if image_array_count % page_count_x != 0:
        page_count_y += 1
    # 画像サイズを計算
    page_size = image_array[0].size
    image_size = (page_size[0] * page_count_x, page_size[1] * page_count_y)
    # 空の画像を作成
    image = Image.new('RGBA', image_size, (0,0,0,0))
    # 空の画像に各ページ画像をコピー
    for i in range(image_array_count):
        source_image = image_array[i]
        if padding[0] > 0 or padding[1] > 0:
            source_image = Image.new('RGBA', (page_size[0] + padding[0] * 2, page_size[1] + padding[1] * 2), (0,0,0,0))
            source_image.paste(image_array[i], (padding[0], padding[1]))
            source_image = source_image.resize(page_size, resample=Image.LANCZOS)
        image.paste(source_image, (page_size[0] * (i % page_count_x), page_size[1] * (i // page_count_x)))
    return image

# 指定ディレクトリ内のファイルリストを取得(サブディレクトリ内は含まれない)
def get_directory_file_list(dir, filter_extension=None, join_input_dir=True):
    # ファイルリストを取得
    directory_info = os.listdir(dir)
    files = [
        f for f in directory_info if os.path.isfile(os.path.join(dir, f))
    ]
    # filter_extensionが指定されている場合は指定拡張子のファイル以外をフィルタリング
    if filter_extension is not None:
        files = [
            f for f in files if os.path.splitext(f)[1].lower() == filter_extension.lower()
        ]
    # ディレクトリ名も含めて返す場合
    if join_input_dir:
        files = [os.path.join(dir, f) for f in files]
    return sorted(files)

def main():
    # 引数を取得
    parser = argparse.ArgumentParser(description="create_flipbook_image")
    parser.add_argument('-i', '--input_dir', type=str, default='./input')   # 入力元ディレクトリ
    parser.add_argument('-f', '--format', type=str, default='png')          # 入力元ファイル形式
    parser.add_argument('-o', '--output', type=str, default='./output.png') # 出力先ファイルパス
    parser.add_argument('-c', '--count_x', type=int, default=0)             # X軸のページ数
    parser.add_argument('-px', '--padding_x', type=int, default=0)          # X軸の各ページパディングサイズ
    parser.add_argument('-py', '--padding_y', type=int, default=0)          # Y軸の各ページパディングサイズ
    args = parser.parse_args()
    # 入力元ディレクトリ内の画像ファイルリストを取得
    filter_extension = None
    if args.format is not None:
        filter_extension = '.' + args.format
    image_path_list = get_directory_file_list(args.input_dir, filter_extension)
    image_list = []
    for image_path in image_path_list:
        image_list.append(Image.open(image_path))
    ext = os.path.splitext(args.output)[1].lower()
    # Flipbook画像として保存
    output_image = create_flipbook_image(image_list, args.count_x, (args.padding_x, args.padding_y))
    if output_image is not None:
        output_image.save(args.output)

if __name__ == "__main__":
    main()