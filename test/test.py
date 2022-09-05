from sources.chaojiying import Chaojiying_Client

chaojiying = Chaojiying_Client('yunzinan', 'shen66029', '937825')
im = open('a.jpg', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
print(chaojiying.PostPic(im, 1902))
