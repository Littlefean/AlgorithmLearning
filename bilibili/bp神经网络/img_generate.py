"""
图片生成器，根据一个图片，生成多个图片，用于快速生成训练集
注意：要求图片是png，并且统一大小28*28

1. 大小整体缩放
2. 上下左右略微平移
3. 左右略微旋转
4. 横向左右梯形拉扯
5. 纵向上下拉扯
"""
from typing import List

from PIL import Image, ImageChops


def img_to_pillow(path: str) -> Image.Image:
    """
    将图片转化成PIL图片放在内存中
    :param path:
    :return:
    """
    return Image.open(path, )


def get_rotate_img_list(original_img: Image.Image) -> List[Image.Image]:
    """
    输入一个内存中的图片，返回一个经过略微旋转后的很多图片组成的列表
    :param original_img:
    :return:
    """
    res = []
    for i in range(-3, 4):
        rotated_image = original_img.rotate(i)
        new_image = Image.new("RGB", rotated_image.size, "black")
        paste_position = (
            (original_img.width - rotated_image.width) // 2,
            (original_img.height - rotated_image.height) // 2
        )
        new_image.paste(rotated_image, paste_position)
        res.append(new_image)
    return res


def get_scaled_img_list(original_img: Image.Image) -> List[Image.Image]:
    """
    返回经过整体缩放后的图片列表
    :param original_img:
    :return:
    """
    res = []
    for i in range(-2, 3):
        rate = 1 + i / 10
        scaled_size = tuple(int(dim * rate) for dim in original_img.size)

        # 进行缩放
        scaled_img = original_img.resize(scaled_size)
        new_img = Image.new("RGB", original_img.size, "black")
        paste_position = (
            (original_img.width - scaled_img.width) // 2,
            (original_img.height - scaled_img.height) // 2
        )
        new_img.paste(scaled_img, paste_position)
        res.append(new_img)
    return res


def get_translated_img_list(original_img: Image.Image) -> List[Image.Image]:
    """
    返回经过上下略微平移n个像素后的图片列表
    :param original_img:
    :return:
    """
    res = []
    for y in range(-1, 2):
        for x in range(-1, 2):
            # 进行平移
            translated_img = ImageChops.offset(original_img, x, y)

            # 创建新图像并在新图像上粘贴平移后的图片
            new_img = Image.new("RGB", original_img.size, "black")
            paste_position = (
                (original_img.width - translated_img.width) // 2,
                (original_img.height - translated_img.height) // 2
            )
            new_img.paste(translated_img, paste_position)
            res.append(new_img)
    return res


def get_sheared_img_list(original_img: Image.Image) -> List[Image.Image]:
    """
    返回经过梯形拉扯后的图片列表
    :param original_img:
    :return:
    """
    # 0.1, 0.2
    res = []
    for x in range(-1, 2):
        shear_matrix = (1, x / 10, 0, 0, 1, 0)
        sheared_image = original_img.transform(original_img.size, Image.AFFINE, shear_matrix)
        new_img = Image.new("RGB", original_img.size, "black")
        paste_position = (
            (original_img.width - sheared_image.width) // 2,
            (original_img.height - sheared_image.height) // 2
        )

        new_img.paste(sheared_image, paste_position)
        res.append(new_img)
    return res


def get_img_list(original_img: Image.Image) -> List[Image.Image]:
    """
    根据一张原始的图片，生成非常多的经过略微变化的图片
    :param original_img:
    :return:
    """
    # 旋转
    res = get_rotate_img_list(original_img)
    # 拉扯
    res = [res_img for img in res for res_img in get_sheared_img_list(img)]
    # 缩放
    res = [res_img for img in res for res_img in get_scaled_img_list(img)]
    # 平移
    res = [res_img for img in res for res_img in get_translated_img_list(img)]
    return res


def main():
    """
    运行main函数后，将会根据imgs文件夹的in文件夹生成out文件夹并保存
    :return:
    """
    original_img = img_to_pillow('imgs/in/2/0.png')
    # # 旋转
    arr1 = get_rotate_img_list(original_img)
    # # 拉扯
    arr1 = [res_img for img in arr1 for res_img in get_sheared_img_list(img)]
    # # 缩放
    arr1 = [res_img for img in arr1 for res_img in get_scaled_img_list(img)]
    # # 平移
    arr1 = [res_img for img in arr1 for res_img in get_translated_img_list(img)]
    print(len(arr1))
    for i, img, in enumerate(arr1):
        img.save(f'imgs/out/2/{i}.png')
    pass


if __name__ == '__main__':
    main()
