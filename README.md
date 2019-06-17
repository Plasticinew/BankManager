# BankManager

### 接口
* Bank接口类
    ```python
    #获取按名称排序的支行信息，返回一个二维list
    getBankOrderByName(
        #支行名，默认为空
        name='',
        #城市，默认为空
        city='',
        #最低资产，默认为0
        propertylow=0,
        #最高资产，默认为100000000
        propertyhigh=1000000000,
        #默认从小到大排序
        smallfirst=True)

    #获取按城市排序的支行信息，返回一个二维list
    getBankOrderByCity(
        name='',
        city='',
        propertylow=0,
        propertyhigh=1000000000,
        smallfirst=True)

    #获取按资产排序的支行信息，返回一个二维list
    getBankOrderByProperty(
        name='',
        city='',
        propertylow=0,
        propertyhigh=1000000000,
        smallfirst=True)

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