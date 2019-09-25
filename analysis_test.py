
from datetime import datetime
import calendar
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import missingno as msno
import seaborn as sns


# 显示所有列的字段，便于打印时直观观看
pd.set_option('display.max_columns', None)
# 初始化
sns.set()
# 从数据包中读取要处理的数据
Datas = pd.read_csv('bike.csv')


# 查看、检查数据
print('Datas.shape:\n {} \n'.format(Datas.shape))      # 查看行数和列数
print('Datas.head(3):\n {} \n'.format(Datas.head(3)))    # 查看DataFrame对象的前n行
print('Datas.dtypes:\n {} \n'.format(Datas.dtypes))     # 查看各数据类型

# 提取“date”
Datas["date"] = Datas.datetime.apply(lambda x: x.split()[0])
# 提取"hour"
Datas["hour"] = Datas.datetime.apply(lambda x: x.split()[1].split(":")[0])
dateString = Datas.datetime[1].split()[0]
# 提取"weekday"
Datas["weekday"] = Datas.date.apply(
    lambda dateString: calendar.day_name[datetime.strptime(dateString, "%Y-%m-%d").weekday()])
# 提取"month"
Datas["month"] = Datas.date.apply(
    lambda dateString: calendar.month_name[datetime.strptime(dateString, "%Y-%m-%d").month])
print('Datas.head(3):\n {} \n'.format(Datas.head(3)))    # 查看DataFrame对象的前n行

# 季节映射处理
Datas["season_label"] = Datas.season.map(
    {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})
# 天气映射处理
Datas["weather_label"] = Datas.weather.map(
    {1: "sunny", 2: "cloudy", 3: "rainly", 4: "bad-day"})
# 是否是节假日映射处理
Datas["holiday_map"] = Datas["holiday"].map({0: "non-holiday", 1: "hoiday"})
print('Datas.head(3):\n {} \n'.format(Datas.head(3)))    # 查看DataFrame对象的前n行


def msno_deal():
    # 可视化查询缺失值
    msno.matrix(Datas, figsize=(20, 10))


# msno_deal()


def season_hour():
    """
    func: 判断不同季节情况下24小时内的数据情况
    """
    sns.FacetGrid(
        data=Datas,
        height=15,
        aspect=1.5). map(
        sns.pointplot,
        'hour',
        'count',
        'season_label',
        palette="deep",
        ci=None)
    plt.show()

# season_hour()


def weather_day():
    """
    func: 判断不同季节情况下每一星期内的数据情况
    """
    sns.FacetGrid(
        data=Datas,
        height=10,
        aspect=1.5). map(
        sns.pointplot,
        'date',
        'count',
        'weather_label',
        palette="deep",
        ci=None)
    plt.show()

# weather_day()


def weekday_hour():
    """
    func: 判断一星期中每天的24小时内的骑行规律
    """
    sns.FacetGrid(
        data=Datas,
        height=10,
        aspect=1.5).map(
        sns.pointplot,
        'hour',
        'count',
        'weekday',
        palette='deep',
        ci=None
    )
    plt.show()


# weekday_hour()


def month_registered():
    """
    func: 判断每个月的注册人数
    """
    sns.FacetGrid(
        data=Datas,
        height=10,
        aspect=1.5).map(
        sns.pointplot,
        'month',
        'registered',
        kind='line',
        ci=None
    )
    plt.show()


# month_registered()


def hour_registered():
    """
    func: 判断24小时内哪一时间段的注册人数多
    """
    sns.FacetGrid(
        data=Datas,
        height=10,
        aspect=1.5).map(
        sns.pointplot,
        'hour',
        'registered',
        kind='line',
        ci=None
    )
    plt.show()


# hour_registered()


def humidity_temp_count():
    """
    func：分析湿度、温度对单车使用次数的影响，并区分出节假日判定
    """
    # 设定温度和湿度离散化
    Datas["humidity_band"] = pd.cut(Datas['humidity'], 6)
    Datas["temp_band"] = pd.cut(Datas["temp"], 6)
    # 对假期字段映射处理
    Datas["holiday_map"] = Datas["holiday"].map(
        {0: "non-holiday", 1: "hoiday"})
    sns.FacetGrid(
        data=Datas,
        row="humidity_band",
        size=5,
        aspect=2). map(
        sns.barplot,
        'temp_band',
        'count',
        'holiday_map',
        palette='deep',
        ci=None).add_legend()
    plt.show()


# humidity_temp_count()


def boxplot_img():
    """
    func:用箱体图分析
    """
    # 设置绘图格式和画布大小
    fig, axes = plt.subplots(nrows=1, ncols=2)
    fig.set_size_inches(14, 5)
    # 添加第1个子图，租车人数季节分布的箱线图
    sns.boxplot(data=Datas, y="count", x="season", orient="v", ax=axes[0])
    # 添加第2个子图，租车人数时间分布的箱线图
    sns.boxplot(data=Datas, y="count", x="hour", orient="v", ax=axes[1])
    # 设置图坐标轴和标题
    axes[0].set(xlabel='Season', ylabel='Count', title="Box Plot On Count Across Season")
    axes[1].set(xlabel='Hour Of The Day', ylabel='Count', title="Box Plot On Count Across Hour Of The Day")
    plt.show()

# boxplot_img()

def all_factors():
    """
    func:分析各因素对共享单车使用的影响
    """
    correlation = Datas[["count", "temp", "atemp",  "humidity", "windspeed", "casual", "registered"]].corr()
    mask = np.array(correlation)
    mask[np.tril_indices_from(mask)] = False
    fig, ax = plt.subplots()
    fig.set_size_inches(15, 8)
    sns.heatmap(correlation, mask=mask, vmax=1.0, square=True, annot=True)
    plt.show()


all_factors()