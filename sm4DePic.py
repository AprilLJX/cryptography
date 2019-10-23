from PIL import Image,ImageDraw
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT

im = Image.open("pku.jpg")
width = im.size[0]
height = im.size[1]
im = im.convert('RGB')
im_byte_list = []
for x in range(width):
    for y in range(height):
        r, g, b = im.getpixel((x,y))
        im_byte_list.append(r)
        im_byte_list.append(g)
        im_byte_list.append(b)
im_byte_list = bytes(im_byte_list)

key = b'3l5butlj26hvv313'
iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
crypt_sm4 = CryptSM4()
#加密过程
crypt_sm4.set_key(key, SM4_ENCRYPT)
encryptRgb_ecb = crypt_sm4.crypt_ecb(im_byte_list)#ecb加密
encryptRgb_cbc = crypt_sm4.crypt_cbc(iv,im_byte_list) #  bytes类型


encryptRgbList_ecb=[]
for b in encryptRgb_ecb:
    encryptRgbList_ecb.append(b)

n1=len(encryptRgbList_ecb)
if n1%3==0:
    pass
elif n1%3==1:
    encryptRgbList_ecb.append(255)
    encryptRgbList_ecb.append(255)
elif n1%3==2:
    encryptRgbList_ecb.append(255)


#每三个数字作为一个rgb值存
list_ecb=[]
for i in range(0,len(encryptRgbList_ecb),3):
    list_ecb.append((encryptRgbList_ecb[i],encryptRgbList_ecb[i+1],encryptRgbList_ecb[i+2]))

#写出图片
encryptImage_ecb = Image.new('RGB',(width,height),(255,255,255))
drawImage_ecb = ImageDraw.Draw(encryptImage_ecb)

encrptImage_cbc = Image.new('RGB',(width,height),(255,255,255))
drawImage_cbc = ImageDraw.Draw(encrptImage_cbc)

i = 0
for x in range(width):
    for y in range(height):
        drawImage_ecb.point((x,y),fill = list_ecb[i])
        drawImage_cbc.point((x,y),fill = encryptRgb_cbc[i])
        i += 1

encryptImage_ecb.save('encrptPku_ecb.jpg','jpeg')
encrptImage_cbc.save('encrptPku_cbc.jpg','jpeg')






# pix = originImg.load()
# width = originImg.size[0]
# height = originImg.size[1]
#
# if os.path.exists("pku.txt"):
#     os.remove("pku.txt")
#
# file_write = open("pku.txt","w")
#
# for x in range(width):
#     for y in range(height):
#         r, g, b = pix[x, y]
#         print(r, g, b)
#         file_write.write(str(r)+',')
#         file_write.write(str(g)+',')
#         file_write.write(str(b)+',')
#         file_write.write("\n")






#
# # 将 图片的二进制内容 转成 真实图片
# with open("encrpt_pku.jpg","wb") as f:
#     f.write(encryptRgb)

# encryptRgbimg = Image.fromarray(encryptRgb.convert('RGB'))
# encryptRgbimg.save("encryPKU.jpg")


# crypt_sm4.set_key(key, SM4_DECRYPT)
# decryptImg_rgb = crypt_sm4.crypt_ecb(Image.open('encrypImgPku.rgba')) #  bytes类型
# print('解密成功')
# decryptImg = decryptImg_rgb.convert('RGB')
# decryptImg.save('decryptImgPku.jpg')
# print('完成加解密！')