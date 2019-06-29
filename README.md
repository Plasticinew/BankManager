# BankManager

### 接口
* Bank接口
    ```python
    #获取支行信息，返回一个二维list
    getBank(
        #session
        session=''
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
    newBank(session, name, city, property)

    #根据支行名称检索，修改已有支行对应属性，参数不能为空
    setBank(session, name, new, attribute)

    #根据支行名称删除支行
    delBank(session, name)

    ```
    使用例：
    ```python
    from query import Bank
    #bank类的接口示例
    engine = db.create_engine('mysql+mysqlconnector://root:2161815@localhost:3306/test')
    DBSession = sessionmaker(bind=engine)
    Session = DBSession()
    #添加支行信息
    try:
        newBank(Session, '下北泽支行', '下北泽', 43962800)
        newBank(Session, '合肥支行', '合肥', 1919810)
    except Exception as e:
        print(e)
    newBank(Session, '济南支行', '济南', 114514)
    Session.commit()
    #获取按资产顺序排序的银行列表
    print(getBank(Session, orderby='Property'))
    #银行资产修改
    setBank(Session,'济南支行', 11400, 'Property')
    Session.commit()
    #获取列表函数可选参数name、city、propertylow（下界）和propertyhigh（上界）
    print(getBank(Session,city='济南',propertylow=1000,propertyhigh=1000000,orderby='City'))
    #根据name（primary key）删除支行
    delBank(Session, '济南支行')
    print(getBank(Session))
    ```

