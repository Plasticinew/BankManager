# BankManager

### 接口
* Bank接口类
    ```python
    #获取支行信息，返回一个二维list
    getBank(
        #支行名，默认为空
        name='',
        #城市，默认为空
        city='',
        #最低资产，默认为0
        propertylow=0,
        #最高资产，默认为100000000
        propertyhigh=1000000000,
        #默认从小到大排序
        smallfirst=True,
        #默认按BankName属性排序
        orderby='BankName'    
    )

    #增加一个新的支行，参数不能为空
    newBank(name, city, property)

    #根据支行名称检索，修改已有支行名称，参数不能为空
    setBankName(oldname, newname)

    #根据支行名称检索，修改已有支行城市，参数不能为空
    setBankCity(name, newcity)

    #根据支行名称检索，修改已有支行的资产，参数不能为空
    #参数change为增加/减少量，如-114
    changeBankProperty(name, change)

    #根据支行名称删除支行
    delBank(name)

    ```
    使用例：
    ```python
    from query import Bank
    #bank类的接口示例
    #生成bank对象时输入要访问数据库的用户名密码
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
    print(bank.getBank(city='济南',propertylow=1000, propertyhigh=1000000, orderby='City'))
    #根据name（primary key）删除支行
    bank.delBank('济南支行')
    print(bank.getBank())
    ```

