import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# STEP 1: DATA PREPARATION (GENERATE MOCK DATA)
data = {
    'ProductID': ['P01', 'P02', 'P03', 'P04', 'P05', 'P06'],
    'ProductName': ['Galaxy S24 Ultra', 'Galaxy A55', 'Galaxy Watch 6', 'Neo QLED 8K TV', 'Bespoke Fridge',
                    'Galaxy S24 Ultra'],
    'SupplierName': ['tsmc ', 'MediaTek', 'Corning Inc', 'Samsung Display', 'Posco Steel', 'TSMC'],
    'CurrentStock': [50, 300, 200, 40, 20, np.nan],
    'ForecastQuantity': [330, 420, 0, 30, 40, -10],
    'UnitPrice': [1200, 400, 300, 2500, 1500, 1200],
    'LeadTimeDays': [20, 12, 10, 5, 15, 20]
}

df = pd.DataFrame(data)


# STEP 2: DATA PREPROCESSING (CLEAN DATA) clean_data(df) hoạt động như một "bộ lọc" để sửa toàn bộ các lỗi
def clean_data(df):
    # Tính giá trị trung bình ở giữa (median) của kho hàng để lấp vào chỗ trống np.nan
    df['CurrentStock'] = df['CurrentStock'].fillna(df['CurrentStock'].median())

    # Cắt bỏ khoảng trắng thừa và viết hoa tất cả tên nhà cung cấp
    df['SupplierName'] = df['SupplierName'].str.strip().str.upper()

    # Quét cột dự báo, nếu thấy số âm (-10) thì ép nó về 0
    df['ForecastQuantity'] = df['ForecastQuantity'].apply(lambda x: x if x >= 0 else 0)

    # Xóa dòng sản phẩm bị trùng lặp dựa trên mã ProductID
    df = df.drop_duplicates(subset=['ProductID'])

    return df


df_cleaned = clean_data(df)


# STEP 3: DATA ANALYSIS
def analyze_supply_risk(df):
    # Lấy Số tồn kho trừ đi Số dự báo bán ra.
    df['Supply_Gap'] = df['CurrentStock'] - df['ForecastQuantity']

    # Dùng hàm np.where của thư viện Numpy để kiểm tra: Nếu bị thiếu hàng (Gap < 0), nó sẽ lấy số lượng thiếu nhân với giá tiền (UnitPrice) để ra
    df['Revenue_Risk'] = np.where(df['Supply_Gap'] < 0, abs(df['Supply_Gap']) * df['UnitPrice'], 0)

    risk_summary = df[df['Supply_Gap'] < 0][
        ['ProductName', 'SupplierName', 'Supply_Gap', 'Revenue_Risk', 'LeadTimeDays']]

    return risk_summary.sort_values(by='Revenue_Risk', ascending=False)


risk_report = analyze_supply_risk(df_cleaned)

# In kết quả ra Terminal
print("--- SAMSUNG SUPPLY CHAIN RISK REPORT ---")
print(risk_report)

# STEP 4: DATA VISUALIZATION
plt.figure(figsize=(10, 6))

# Draw horizontal bar chart
plt.barh(risk_report['ProductName'], risk_report['Revenue_Risk'], color='#d9534f', edgecolor='black')

# Format the chart
plt.xlabel('Revenue Risk ($)', fontsize=12)
plt.ylabel('Product Name', fontsize=12)
plt.title('High-Risk Products by Potential Revenue Loss (Samsung Electronics)', fontsize=14, fontweight='bold')

# Invert Y-axis to show the highest risk product at the top
plt.gca().invert_yaxis()
plt.grid(axis='x', linestyle='--', alpha=0.7)

# Display the chart
plt.tight_layout()
plt.show()