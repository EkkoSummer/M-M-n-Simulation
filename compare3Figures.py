"""
Problem4: Overlay the 3 figures
"""
import powerof2 as po2
import joinShortestQ as jsq
import URP as urp
import matplotlib.pyplot as plt

lamda = [7,8,9,9.5]

plt.figure("Result")


plt.subplot(2,2,1)
plt.title("powerof2")
for l in lamda:
    po2.culCcdf(po2.averageWait(l))

plt.ylabel('log(CCDF)')
plt.legend(labels = ["λ=7","λ=8","λ=9","λ=9.5"])
plt.ylim(-25,0)

plt.subplot(2,2,2)
plt.title("joinShortQ")
for l in lamda:
    jsq.culCcdf(jsq.averageWait(l))

plt.ylabel('log(CCDF)')
plt.legend(labels = ["λ=7","λ=8","λ=9","λ=9.5"])
plt.ylim(-25,0)

plt.subplot(2,2,3)
plt.title("uniform-random")
for l in lamda:
    urp.culCcdf(urp.averageWait(l))
plt.xlabel('Number of Coms')
plt.ylabel('log(CCDF)')
plt.legend(labels = ["λ=7","λ=8","λ=9","λ=9.5"])
plt.ylim(-25,0)

plt.subplot(2,2,4)
plt.title("synthesis")
for l in lamda:
    po2.culCcdf(po2.averageWait(l))
    jsq.culCcdf(jsq.averageWait(l))
    urp.culCcdf(urp.averageWait(l))

plt.xlabel('Number of Coms')
plt.ylabel('log(CCDF)')


plt.subplots_adjust(wspace =0.5, hspace =0.5)
plt.ylim(-25,0)
plt.show()