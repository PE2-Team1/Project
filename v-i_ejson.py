# 파싱 및 matplotlib가져오기
import xml.etree.ElementTree as et
import matplotlib.pyplot as plt
t = et.parse('./HY202103_D07_(0,0)_LION1_DCM_LMZC.xml')
#root = t.getroot()

# v와 i 가져오기
v = t.find('.//IVMeasurement[1]/Voltage').text
i = t.find('.//IVMeasurement[1]/Current').text

# v와 i 리스트로 가져오기
vl = [float(v.strip()) for v in v.split(',')]
il = [abs(float(i.strip())) for i in i.split(',')]

# 시각화
plt.figure(figsize=(10, 6))
plt.plot(vl, il, marker='o', linestyle='-')
plt.yscale('log')
plt.xlabel('Voltage (V)')
plt.ylabel('Current (A)')
plt.title('IV Curve')
plt.grid(True) # 보조선을 생성
#plt.yscale('symlog')  #y축 스케일을 'symlog'로 변경하여 작은 값들도 표시될 수 있도록 함
plt.show()
plt.s
[]