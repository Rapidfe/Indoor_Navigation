from PIL import Image

def makeCoord(ss):
    thresh = 190
    initial_h = 0
    initial_w = 0
    h_div = 18
    w_div = 18
    chkdiv = 4
    chk = 0
    coord = []

    input = ss
    ima = Image.open(input)     # 파일open
    (h, w) = ima.size
    h_add = h / h_div  # 높이/칸수 (=한칸의 높이)
    w_add = w / w_div  # 너비/칸수 (=한칸의 너비)
    h_divadd = h_add / 3  # 한 칸 안에서 h_divadd * w_divadd 영역 안에 있는 chkdiv*chkdiv 개의 픽셀을 확인할거임
    w_divadd = w_add / 3
    ima = ima.convert("L")      # grayscale로 변환
    pil_im = ima.point(lambda p: p > thresh and 255)    # thresh값보다 큰거는 다 흰색(255)으로 : 흑백으로 이진화 하는거

    pil_im = pil_im.convert('1')    # 흑백으로 변환
    # pil_im2 = pil_im.convert('RGB')

    ## 각 칸의 색깔 판단하기
    for i in range(h_div):
        tmp = []
        for j in range(w_div):
            start_h = initial_h + i*h_add + h_divadd
            start_w = initial_w + j*w_add + w_divadd
            for k in range(chkdiv):   # 한 칸 안에서 chkdiv*chkdiv 개 픽셀 확인
                for l in range(chkdiv):
                    row = start_h + k*h_divadd/(chkdiv-1)
                    col = start_w + l*w_divadd/(chkdiv-1)
                    if pil_im.getpixel((col, row)) < thresh:   # thresh값보다 작으면(더 어두우면) chk + 1
                        chk = chk + 1
                    # pil_im2.putpixel((int(col),int(row)), (255,0,0))
            if chk < chkdiv*chkdiv/2:       # chk가 확인한 픽셀 개수의 절반 미만이면(검정 픽셀이 더 적다는뜻) 흰색으로 판단하고 결과값에 추가 (흰색=경로)
                tmp.append(j)
            chk = 0
        # if len(tmp)==0:
        #     tmp.append('empty')
        coord.append(tmp)
    # sav_name2 = 'result_' + input + '2.png'
    # pil_im2.save(sav_name2)

    # for i in range(len(coord)):
    #    print(coord[i])
    return coord

# sav_name = 'result_' + input + '.png'
# pil_im.save(sav_name)

# makeCoord('map1.png')
