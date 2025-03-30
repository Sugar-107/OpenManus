这个文件内的内容定义了run_flow.py相关的内容
1.``` time.time() ```在 python中，是导入的模块(静态类) 可以直接使用，不必实例化
2.``` agents = { "manus": Manus(), }```  等价于
```java
Map<String, Agent> agents = new HashMap<>();
agents.put("manus", new Manus());
```
- {} 表示创建一个字典(dictionary)，类似于Java中的Map或HashMap
- "manus" 是字典中的键(key)，为字符串类型
- Manus() 是在调用Manus类的构造函数来创建一个Manus类的对象实例
- 整体来说，这段代码创建了一个字典，其中包含一个键值对，键是"manus"，值是Manus类的一个实例
