# encoding: utf-8

'''
用 Python 抓取公号文章保存成 PDF

此功能是用于保存公众号中的Cookie的，方便下一个程序直接获取Cookie来批量抓取公众号的文章，并且声称PDF文件

https://mp.weixin.qq.com/s?__biz=MzI4NDY5Mjc1Mg==&mid=2247491090&idx=2&sn=cf4ea8ad6ac00ccb74279dcc5ee17c74&chksm=ebf6c66ddc814f7b78cef0e264380db7eb2ccbf268e7956966471f5a4f2e972571aad7b91902&mpshare=1&scene=1&srcid=&sharer_sharetime=1585322453517&sharer_shareid=ce1c9240f8bf63dd6856d9d376f3f906&key=bda765778963d29df77f64a216dd934594a64e5fc44c0b9368d35e0ed25b49b8ec44923f135fe7fc0072fc0a6af84bf45512afa313951bb5c9738367ed8d7231013c48b1a090f530e17dc86c400c2aa2&ascene=1&uin=ODY4Mjc0OTA3&devicetype=Windows+10&version=62080079&lang=zh_CN&exportkey=A0FUI4IGP408X3DU80gdeBc%3D&pass_ticket=R8eW3QKhIGY1uVGjVKuBNck4GMeVBuhJXkkga3xaFdQ1MCnaorh1iMQ7NgiCPc47
'''

import json

# 从浏览器中复制出来的 Cookie 字符串

cookie_str = "RK=oaxwQ7stGf; ptcz=ad84e1971281eab1583cef31afa94474d95961755833707f84fed7915b6d51e1; pgv_pvi=5445289984; pgv_pvid=4054943580; eas_sid=B1s5j7B7V3k359L1m5L868e2r4; ied_qq=o0172577882; o_cookie=172577882; pac_uid=1_172577882; ua_id=RVeKkXsi0xXnW1V5AAAAAI-FZQhmlxLTXdi1TFQgdEs=; mm_lang=zh_CN; tvfe_boss_uuid=036885a797275534; qb_guid=8132233fa86b46afbb104dbbc2941a66; Q-H5-GUID=8132233fa86b46afbb104dbbc2941a66; NetType=; noticeLoginFlag=1; openid2ticket_oiAzF1Nz6wTeOkpm2K9T-0WDzwMU=dqjdps6inUJFwQ0jmpOtYTWMY8wS95xkbIWQrTt9hqM=; ts_uid=122802222; openid2ticket_oT6Rr0XLxOtToUVZXI-SHmkULXuI=fxzOwJYTxIf69Gky4Muw7sh0TI5FgxgPuDbXg6b/B1E=; uin=o0172577882; skey=@wLubBFDsH; pgv_info=ssid=s8635621064; rewardsn=; wxtokenkey=777; wxuin=868274907; devicetype=Windows10; version=62080079; lang=zh_CN; pass_ticket=R8eW3QKhIGY1uVGjVKuBNck4GMeVBuhJXkkga3xaFdQ1MCnaorh1iMQ7NgiCPc47; wap_sid2=CNulg54DElxWVzVRd0lzb1d4YmRJMEZMa0hubWh0Z3hsb1BXZ3FrUmk3dGJaTEJ4a2U2amdRY1JtazU0WHpzRUJpX28tdlVZQ0V3TGNzUzhNUHBLYk9mVzJXMklreDhFQUFBfjCW25f0BTgNQAE=; pgv_si=s5434076160; uuid=40719235cd057b422e406d2d737071a3; ticket=d9816f55f8c80a6aa087e10f1a6555ad62804ef8; ticket_id=gh_2ffd0c732a5c; cert=DeA23jbZV71A66bJWqw3BAB7rRQqmEzF; remember_acct=11624523%40qq.com; rand_info=CAESIDQMdIloOciIflsvrQoqBToFQkqg42W4oDD9lzXbhSL6; slave_bizuin=3544694598; data_bizuin=3538696004; bizuin=3544694598; data_ticket=JzyWpW58qqIagmmICKCTReT2gp7z7DjIjgmy9DexJHLTpxrV2L7986FtoNpawBFr; slave_sid=TjYydGpWUDE5OUFfeHp4RFo0YVdKbmsxQWNjbXVBWHl4MjcxTWZpdTZPSFJBblZoX2ZfRDU5R3dKNlliV3NNb25HSGVpck02akc5ZjhKVm81RmRqTFk3aW40bTViM3RFVWhWVkFTTVd0N3dWSUlDekhWQUhYSWxpbFNwRHNGNmF4c2JDS3JRQUpsalJKazFT; slave_user=gh_2ffd0c732a5c; xid=1f0816bb29f49c1515cce76c4089edf3; openid2ticket_oRDfs0qbnl97I5FfwiLD86NfcsQo=npCnLJfQHsBmWUmtQW+54O551wu1oAqjcubBnwe/by8="

cookie = {}
# 遍历 cookie 信息
for cookies in cookie_str.split("; "):
    cookie_item = cookies.split("=")
    cookie[cookie_item[0]] = cookie_item[1]

# 将Cookie写入到本地文件保存
with open('cookie.txt', 'w') as file:
    # 写入文件
    file.write(json.dumps(cookie))
