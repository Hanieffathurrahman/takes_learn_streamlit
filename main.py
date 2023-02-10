import pandas as pd 
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide"
)

@st.cache
def get_data_from_excel():
    
    data_frame = pd.read_excel(
        io = 'supermarkt_sales.xlsx',
        engine = 'openpyxl',
        sheet_name = 'Sales',
        skiprows = 3,
        usecols = 'B:R',
        nrows = 1000,
    )
    # add hour column to dataframe
    data_frame["hour"]  = pd.to_datetime(data_frame["Time"],format="%H:%M:%S").dt.hour
    return data_frame
data_frame = get_data_from_excel()

#--- sidebar ---
st.sidebar.header("please filter here: ")
 
city = st.sidebar.multiselect(
    "select the city: ",
    options=data_frame['City'].unique(),
    default=data_frame['City'].unique()
)

customer_type = st.sidebar.multiselect(
    "select the Customer type: ",
    options=data_frame['Customer_type'].unique(),
    default=data_frame['Customer_type'].unique()
)

gender = st.sidebar.multiselect(
    "select the gender: ",
    options=data_frame['Gender'].unique(),
    default=data_frame['Gender'].unique()
)

df_selection = data_frame.query(
    "City == @city & Customer_type== @customer_type & Gender == @gender"
)

# ----mainpage----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")
#st.dataframe(df_selection)

#top KPI,s
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean())
star_rating = ":star:" * int(round(average_rating,0))
average_sale_by_transaction =round(df_selection["Total"].mean(),2) 
 
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales :")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating :")
    st.subheader(f"{average_rating}{star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction :")
    st.subheader(f"US ${average_sale_by_transaction}")
st.markdown("----")

#sales by product line [bar chart]
sales_by_product_line=(
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)
# barchart
fig_product_sales = px.bar(
    sales_by_product_line,
    x = "Total",
    y = sales_by_product_line.index,
    orientation = "h",
    title= "<b>Sales by Product line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white"
)
fig_product_sales.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis =(dict(showgrid=False))
)
#st.plotly_chart(fig_product_sales)

#sales by hour bar chart
sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x = sales_by_hour.index,
    y = "Total",
    title = "<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template= "plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False))
)
#st.plotly_chart(fig_hourly_sales)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales,use_container_width=True)
right_column.plotly_chart(fig_product_sales,use_container_width=True)

#hide streamlit style
hide_st_style = """
                <style>
                #MainMenu{visibility:hidden;}
                footer{visibility:hidden;}
                header{visibility:hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)



#all reference i'm leran from : https://www.youtube.com/watch?v=Sb0A9i6d320&list=PLHgX2IExbFovFg4DI0_b3EWyIGk-oGRzq and i'm revernce to him