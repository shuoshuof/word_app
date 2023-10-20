# 

## 单词数据存储
+ excel储存
+ 以单词为 主码
### 存储属性
#### date
导入日期
#### acc
使用EWMA更新
$$
    acc_{t} = \beta*acc_{t-1} + (1-\beta)*acc'
$$
其中$acc'$为本次回答是否正确，取值为0或1。
$\beta$ 的取值由考虑前n次回答确定：
$$
    \beta = \exp^{(\frac{-1}{n})}
$$
需要对$acc_t$进行矫正：
$$
    acc_t' = \frac{acc_t}{1-\beta^t}
$$
#### review_date  
#### test_num
## 单词导入
+ 输入
+ csv导入

## 阅读训练
+ 显示单词
+ 按键显示中文
+ 确认正误

