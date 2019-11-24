class dsheet():
  def __init__(self,data,col_name=''):
    self.name=''
    self.ds=[]
    self.colname=col_name
    self.__setds(data,col_name)
    
  def __setds(self,data,col_name):#不建议从外部调用
    dic={}
    dic_li=[]
    if type(data) != list: #data必须为列表，否则创建失败，返回空值
      print('data shoud be list')
      return None
    else:
      for i in range(len(data)):
        dic={'row':i}
        dic_li.append(dic)
    maxlen=1
    for ea in data:
      if type(ea)==list: #data可以是二维列表，当是二维列表时，生成多个字段
        if len(ea)>maxlen:
          maxlen=len(ea)
    for i in range(len(dic_li)):
      for ci in range(maxlen):
        if type(data[i])==list:
          try:
            col = col_name[ci]
          except:
            col ='' #获取字段名失败时，将字段名相应的设置为空，确保字段列表不完成，仍然可以生成数据表
          try:
            coldata = data[i][ci] #获取某一个数据单元值失败时，将数据单元值设置为None,确保二维列表元素不完整时仍然可以生成数据表。
          except:
            coldata = None
          dic={col:coldata}
          dic_li[i].update(dic)
        else:
          try:
            col = col_name[ci]
          except:
           col =None
          dic={col:data[i]}
          dic_li[i].update(dic)
    self.ds = dic_li
    self.__updatecol() #生成数据表后，检查字段名，更新字段名
    
  def __updatecol(self):
    if len(self.ds) == 0:
      print('ds is empty, can not update column')
    else:
      collist = []
      for ea in self.ds[0].keys():
        collist.append(ea)
    self.colname=collist
        
    
  def addcol(self,name,data):
    dic={}
    if type(data) != list:
      for i in range(len(self.ds)):
        dic={name:data}
        self.ds[i].update(dic)
    else:
      for i in range(len(self.ds)):
        try:
          dic_data = data[i]
        except:
          dic_data = None
        dic={name:dic_data}
        self.ds[i].update(dic)
    self.__updatecol()
    return self
    
  def addrow(self,data):
    dic={}
    n=len(self.ds)
    dic['row']=n
    if type(data) != list:
      for i in range(1,len(self.colname)):
        dic[i]=data
    else:
      for i in range(1,len(self.colname)):
        try:
          dic_value = data[i-1]
        except:
          dic_value=None
        dic[self.colname[i]]=dic_value
    self.ds.append(dic)
    return self
    
  def show(self,row,col=''):
    row_range = ''
    row_num=0
    col_num=0
    return_li=[]
    return_info = 'row number showed:'+str(row_num)+', col number showed:'+str(col_num)
    if col!='':
      if type(col)==list:
        for ea in col:
          if ea not in self.colname:
            print('%s not in colname list'%ea)
            return return_info
      else:
        print('colname should be list, not %s'%(type(col)))
        return return_info
        
    col_range= len(self.colname)
    if row == ':':
      if col =='':
        col_num=len(self.colname)
        head = ','.join(self.colname)
        col=self.colname
        print(head)
      else:
        col2=col.copy()
        col_num=len(col)
        head=','.join(col2)
        print(head)
      for ea in self.ds:
        data=''
        for ek in ea.keys():
          if ek in col:
            dvalue=ea[ek]
            data += str(dvalue)+','
        data=data[:-1]
        row_num += 1
        print(data)
    else:
      row_range=row.split(':')
      row_start = int(row_range[0])
      row_end = int(row_range[1])
      if row_start >=row_end:
        print('start of row should be smaller than end of row')
        return None
      else:
        if col=='':
          col_num=len(self.colname)
          head = ','.join(self.colname)
          col=self.colname
          print(head)
        else:
          col_num=len(col)
          col2=col.copy()
          head=','.join(col2)
          print(col2)
          print(head)
        for n in range(row_start,row_end):
          data = ''
          for dkey in col:
            data += str(self.ds[n][dkey])+','
          data=data[:-1]
          row_num+=1
          print(data)
    return_info = 'row number showed:'+str(row_num)+', col number showed:'+str(col_num)
    return return_info
      
  def loc(self,row,col=''):
    row_range = ''
    row_num=0
    col_num=0
    return_li=[]
    return_info = 'row number showed:'+str(row_num)+', col number showed:'+str(col_num)
    if col!='': #如果字段名的范围是部分,检查传入的字段名
      if type(col)==list:
        for ea in col:
          if ea not in self.colname: #发现有字段名在数据表不存在，返回None
            print('%s not in colname list'%ea)
            print(return_info)
            return None
      else: #如果字段名不为空，又不是列表，提示错误返回None.
        print('colname should be list, not %s'%(type(col)))
        print(return_info)
        return None
    if row == ':':
    #行的范围是全部时，确定字段范围，返回对应字典键的值，并将它存于一个新的列表里
      if col =='':
        col=self.colname
      for ea in self.ds:
        dic_loc={}
        for ek in ea.keys():
          if ek in col:
            dvalue=ea[ek]
            dic_loc[ek]=dvalue
        return_li.append(dic_loc)

    else:
    #行的范围是部分，先选择行的范围，再确定字段范围，返回对应字典键的值，
    #并将它存于一个新的列表里
      row_range=row.split(':')
      row_start = int(row_range[0])
      row_end = int(row_range[1])
      if row_start >=row_end:
        print('start of row should be smaller than end of row')
        return None
      else:
        if col=='':
          col=self.colname
        for n in range(row_start,row_end):
          data = ''
          dic_loc={}
          for ek in col:
            dic_dsn=self.ds[n]
            dvalue = dic_dsn[ek]
            dic_loc[ek]=dvalue
          return_li.append(dic_loc)
    new_data=[]
    new_col=[]
    for ec in return_li[0].keys():
      new_col.append(ec)
    for ed in return_li:
      new_value=[]
      for ek in ed:
        new_value.append(ed[ek])
      new_data.append(new_value)
    new_ds = dsheet(new_data,new_col)
    return new_ds
    
if __name__=='__main__':
  l1=['beijing','shanghai','guangzhou','shenzhen']
  ds1 = dsheet(l1,['city'])
  l2=[1,2,3,4]
  ds1=ds1.addcol('rank',l2)
  l4=['chengdu','5']
  ds1=ds1.addrow(l4)
  l5=[2400,2900,2100,2200,1200]
  ds1=ds1.addcol('GDP',l5)
  ds2=ds1.loc('1:3',['city','GDP'])
  ds2.show(':')
  print('\n')
  ds1.show(":")
