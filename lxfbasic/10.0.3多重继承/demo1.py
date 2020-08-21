"""
多重继承的例子
"""

#燃油骑车
class Gascar(object):
	def __init__(self,gastype,displacement,oil):
		self.gastype = gastype
		self.displacement = displacement
		self.oil = oil

	#计算续航里程
	def mileage1(self):
		if self.oil > 0:
			return 100*self.oil/9
		else:
			return 0

	#加油或走油方法
	def adjustoil(self, oilmass):
		if oilmass>0 and oilmass<=60:
			oil += oilmass
			if oil>60:#油箱加班
				oil=60
		if oilmass<0 and oilmass>=-60:
			oil-=oilmass
			if oil < 0:#油箱无油
				oil = 0


#电动汽车
class Electriccar(object):

	def __init__(self,batterytype,capacity,residual):
		self.batterytype = batterytype
		self.capacity = capacity
		self.residual = residual

	def mileage2(self):
		if self.residual>0:
			return 100*self.residual/25000
		else:
			return 0

	def adjustoil(self, power):
		if residual>0 and residual<=capacity:
			residual += power
			if residual>60:#充满了
				residual=60
		
		if residual<0 and residual>=-capacity:
			residual-=power
			if residual < 0:
				residual=0

#子类----混合动力汽车
class Hybrids(Gascar,Electriccar):
	def __init__(self,gastype,displacemenet,oil,batterytype,capacity,residual):
		super().__init__(gastype, displacemenet, oil)
		Electriccar.__init__(self, batterytype, capacity, residual)

	def endurance(self, oil, bat): #计算混合动力汽车的续航里程
		#self.oil=oil
		#self.residual=bat
		return self.mileage1() + self.mileage2()

if __name__ == '__main__':
	cl=Hybrids('汽油',1.8,43,'锂铁',18400,16020)
	print('能续航：{:.1f}'.format(cl.endurance(cl.oil, cl.residual)))
	cl.oil=55
	cl.residual=18400
	print('能续航：{:.1f}'.format(cl.endurance(cl.oil, cl.residual)))
