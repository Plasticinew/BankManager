from query import Bank
#bank类的接口示例
bank = Bank('test','2161815')
#添加支行信息
bank.newBank('下北泽支行', '下北泽', 43962800)
bank.newBank('合肥支行', '合肥', 1919810)
bank.newBank('济南支行', '济南', 114514)
#获取按资产顺序排序的银行列表
print(bank.getBankOrderByProperty())
#银行资产修改
bank.changeBankProperty('济南支行', -514)
#获取列表函数可选参数name、city、propertylow（下界）和propertyhigh（上界）
print(bank.getBankOrderByCity(city='济南',propertylow=1000,propertyhigh=1000000))
#根据name（primary key）删除支行
bank.delBank('济南支行')
print(bank.getBankOrderByName())