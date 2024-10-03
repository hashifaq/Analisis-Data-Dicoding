import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Load data
top_cities_df = pd.read_csv('top_cities.csv')
avg_review_score_df = pd.read_csv('avg_review_score_per_category.csv')
best_selling_region_df = pd.read_csv('best_selling_region.csv')
seller_performance_df = pd.read_csv('seller_performance.csv')

# rename the 'order_id' column to 'total_sales'
def create_top_cities_new_df(df):
    df.rename(columns={
        "order_id": "total_sales"
    }, inplace=True)
    return df

top_cities_new_df = create_top_cities_new_df(top_cities_df)

# Title header
st.title("E-Commerce Dashboard")

# Tingkat Penjualan Berdasarkan Kota
st.header("Performa Penjualan Berdasarkan Kota")
num_cities = top_cities_new_df['customer_city'].nunique()
num_cities_to_show = st.number_input('Masukkan jumlah kota teratas:', min_value=1, max_value=num_cities, value=10)
filtered_top_cities = top_cities_new_df.sort_values(by='total_sales', ascending=False).head(num_cities_to_show)
st.bar_chart(filtered_top_cities, x='customer_city', y='total_sales')


# Rating Berdasarkan Kategori Produk
st.header("Tingkat Rating Berdasarkan Kategori Produk")
num_categories = avg_review_score_df['product_category_name'].nunique()
num_categories_to_show = st.number_input('Masukkan jumlah kategori teratas:', min_value=1, max_value=num_categories, value=10)
filtered_review_score = avg_review_score_df.sort_values(by='review_score', ascending=False).head(num_categories_to_show)
st.bar_chart(filtered_review_score, x='product_category_name', y='review_score')


# 5 Kategori produk dengan rating terbaik dan terendah
top_5_categories = avg_review_score_df.sort_values(by='review_score', ascending=False).head(5)
bottom_5_categories = avg_review_score_df.sort_values(by='review_score', ascending=True).head(5)

col1, col2 = st.columns(2)
with col1:
    st.subheader("5 Kategori Produk dengan Rating Terbaik")
    st.bar_chart(top_5_categories.sort_values(by='review_score', ascending=True), x='product_category_name', y='review_score')

with col2:
    st.subheader("5 Kategori Produk dengan Rating Terendah")
    st.bar_chart(bottom_5_categories.sort_values(by='review_score', ascending=False), x='product_category_name', y='review_score')


# Kinerja Seller
st.header("Kinerja Penjual Berdasarkan Kota")
num_sellers = seller_performance_df['seller_id'].nunique()
num_sellers_to_show = st.number_input('Masukkan jumlah penjual teratas:', min_value=1, max_value=num_sellers, value=10)
filtered_seller_performance = seller_performance_df.sort_values(by='total_sales', ascending=False).head(num_sellers_to_show)
st.bar_chart(filtered_seller_performance, x='seller_id', y='total_sales')


# 10 Seller dengan performa terbaik berdasarkan kota
selected_seller_city = st.selectbox(
    'Pilih Kota Penjual:',
    options=seller_performance_df['seller_city'].unique(),
    index=0
)

filtered_seller_performance = seller_performance_df[seller_performance_df['seller_city'] == selected_seller_city]
top_10_sellers = filtered_seller_performance.sort_values(by='total_sales', ascending=False).head(10)
st.subheader(f"Top 10 Penjual di {selected_seller_city}")
st.bar_chart(top_10_sellers, x='seller_id', y='total_sales')
