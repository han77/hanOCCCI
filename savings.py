'''
적금 계산기
한희정
2023.08.22

카카오26주적금 계산하기
-매주 1만원씩 증가
-이율 4.5%/년
=> 기간(p_weeks)에 대한 이자 계산 : 원금*이율*p_weeks/52주
-적금 입금 건별로 예치된 기간만큼 약정된 금리 적용후 합산하여 지급
-일반과세 : 소득세14%, 지방소득세 = 소득세의 10%
'''
#%%
import sys
from matplotlib import pyplot as plt
import numpy as np

def installment_savings(deposit):
    transfer=deposit
    transfers = []
    interest_rate_year = 0.07
    sum = 0
    sumlist = []
    total = 0

    for i in range(1,27):
        transfers.append(transfer)
        transfer+=deposit
    for i, transferx in zip(range(1,27), transfers):   
        print(i, transferx) 
        p_weeks = 27-i
        amount= transferx*interest_rate_year*p_weeks / 52
        print(i, ' weeks transfer=',transferx,', amount=', amount)
        sum += amount
        sumlist.append([amount,sum])
        total = total + transferx 
    
    return [total, sum, sumlist]

def draw_graph(list):
    plt.title('weekly amount')    
    plt.xlabel('week')
    plt.ylabel('money')
    xtick_range= range(1,27)
    xtick_label = xtick_range
    plt.xticks(xtick_range, xtick_label)
    # 새로운 리스트
    amount_list = [x[0] for x in list]
    cumamount_list = [x[1] for x in list]

    plt.plot(xtick_range, amount_list)
    plt.plot(xtick_range, cumamount_list)
    return


def main(argv):
    total, rate_sum, sumlist = installment_savings(10000)
    print(total, rate_sum)
    print(sumlist)
    draw_graph(sumlist)
    
if __name__ == "__main__":
    main(sys.argv[1:])

# %%
