# -*- coding: utf-8 -*-
"""AIProject_DataPreprocessing.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fOG1ixys5sj11nfTqN-8_oztKuLeeYIq
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

!apt-get -qq install fonts-nanum
import matplotlib.font_manager as fm
import matplotlib as mpl

fontpath = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
fm.fontManager.addfont(fontpath)
mpl.rc('font', family='NanumGothic')
mpl.rcParams['axes.unicode_minus'] = False
#from sklearn.model_selection import train_test_split

from google.colab import drive
drive.mount('/content/drive')

data = pd.read_csv('/content/drive/MyDrive/data_2024_3.csv', encoding='euc-kr')

# Shuffle the data
data = data.sample(frac=1).reset_index(drop=True)

print(data.head())


# Define split ratios
#train_ratio = 0.7
#validation_ratio = 0.15
#test_ratio = 0.15

# Split the data into training, validation, and testing sets
#train_data, temp_data = train_test_split(data, test_size=(1 - train_ratio))
#val_data, test_data = train_test_split(temp_data, test_size=test_ratio/(test_ratio + validation_ratio))

# Save the splits to CSV files if needed
#train_data.to_csv("train_data.csv", index=False)
#val_data.to_csv("val_data.csv", index=False)
#test_data.to_csv("test_data.csv", index=False)

data.dropna(subset=["관측시간", "관측지점"], inplace=True)

# 관측시간을 datetime 타입으로 변환
data["관측시간"] = pd.to_datetime(data["관측시간"])

data[["관측지점", "관측지점세부"]] = data["관측지점"].str.split('_', expand=True)

columns_to_fill = ["관측최대풍속"]
columns_to_fill = ["관측최대풍속", "(AVOC)관측최대풍속", "(BVOC)관측최대풍속"]

for column in columns_to_fill:
    data[column] = data.groupby(["관측시간", "관측지점"])[column].transform(
        lambda x: x.fillna(x.mean())
    )

    # 그래도 남아있는 결측치는 관측지점으로 채우기
    data[column] = data.groupby('관측지점')[column].transform(
        lambda x: x.fillna(x.mean())
    )

    # 그래도 남아있는 결측치는 관측시간으로 채우기
    data[column] = data.groupby('관측시간')[column].transform(
        lambda x: x.fillna(x.mean())
    )

    # 여전히 남아있는 결측치는 전체 평균으로 채우기
    overall_mean = data[column].mean()
    data[column].fillna(overall_mean, inplace=True)

    # 결측치 처리 전 결측치 확인
if data.isnull().values.any():
    print("데이터프레임에 결측치가 있습니다.")
else:
    print("데이터프레임에 결측치가 없습니다.")

# 각 열의 결측치 수 확인
missing_values = data.isnull().sum()
print("각 열의 결측치 수:")
print(missing_values)

data.sort_values(by="관측시간", inplace=True)
data = data.drop(columns=['관측지점', '관측지점세부'])
data = data.drop(columns=['(AVOC)관측온도', '(AVOC)관측습도', '(AVOC)관측기압', '(AVOC)관측풍속', '(AVOC)관측풍향', '(AVOC)관측최대풍속', '(AVOC)관측미세먼지', '(AVOC)관측초미세먼지', '(AVOC)관측극초미세먼지', '(AVOC)배관관측온도', '(BVOC)관측온도', '(BVOC)관측습도', '(BVOC)관측기압', '(BVOC)관측풍속', '(BVOC)관측풍향', '(BVOC)관측최대풍속', '(BVOC)관측미세먼지', '(BVOC)관측초미세먼지', '(BVOC)관측극초미세먼지' ])

columns_to_visualize = [col for col in data.columns if col != '관측시간']
data[columns_to_visualize].hist(bins=15, figsize=(15, 10))
plt.show()

# Plot boxplots
plt.figure(figsize=(15, 10))
sns.boxplot(data=data)
plt.xticks(rotation=90)
plt.show()

# Compute the correlation matrix
corr = data[columns_to_visualize].corr()

# Generate a heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm')
plt.show()

sns.pairplot(data, vars=columns_to_visualize, hue='관측미세먼지')
plt.show()

features = [col for col in columns_to_visualize if col not in ['관측미세먼지', '관측초미세먼지']]
target_vars = ['관측미세먼지', '관측초미세먼지']

for feature in features:
    for target in target_vars:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=data[feature], y=data[target])
        plt.title(f'Scatter plot between {feature} and {target}')
        plt.xlabel(feature)
        plt.ylabel(target)
        plt.legend()
        plt.show()