import streamlit as st
import pandas as pd

# 页面配置
st.set_page_config(page_title="风险点打标结果可视化工具", layout="wide")


def load_data(file):
    df = pd.read_excel(file)
    # 确保列名一致，去除空格
    df.columns = [c.strip() for c in df.columns]
    return df


st.title("🔍 风险点打标结果可视化工具")

# 1. 文件上传
uploaded_file = st.file_uploader("请上传 Excel 文件", type=["xlsx"])

if uploaded_file:
    df = load_data(uploaded_file)

    # --- 侧边栏：筛选控制 ---
    st.sidebar.header("筛选面板")

    # 一级风险点筛选
    l1_options = ["全部"] + list(df["一级风险点"].unique())
    selected_l1 = st.sidebar.selectbox("选择一级风险点", l1_options)

    # 根据一级风险点联动末级风险点
    if selected_l1 != "全部":
        filtered_df = df[df["一级风险点"] == selected_l1]
    else:
        filtered_df = df

    l_last_options = ["全部"] + list(filtered_df["末级风险点名称"].unique())
    selected_last = st.sidebar.selectbox("选择末级风险点名称", l_last_options)

    if selected_last != "全部":
        filtered_df = filtered_df[filtered_df["末级风险点名称"] == selected_last]

    # --- 分页逻辑 ---
    st.sidebar.markdown("---")
    batch_size = st.sidebar.slider("每页显示数量", 5, 50, 10)
    total_pages = (len(filtered_df) // batch_size) + (1 if len(filtered_df) % batch_size > 0 else 0)

    if total_pages > 0:
        current_page = st.sidebar.number_input(f"页码 (共 {total_pages} 页)", min_value=1, max_value=total_pages,
                                               step=1)

        # 计算当前页数据范围
        start_idx = (current_page - 1) * batch_size
        end_idx = start_idx + batch_size
        page_data = filtered_df.iloc[start_idx:end_idx]

        st.write(f"📊 当前筛选条件下共有 **{len(filtered_df)}** 条记录")

        # --- 数据展示区 ---
        # 使用容器网格展示，美化布局
        for _, row in page_data.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 3])

                with col1:
                    # 展示图片
                    if pd.notna(row['url']):
                        st.image(row['url'], caption="商品图", use_container_width=True)
                    else:
                        st.warning("无图片URL")

                with col2:
                    st.subheader(row['title'])
                    c_a, c_b = st.columns(2)
                    c_a.metric("一级风险点", row['一级风险点'])
                    c_b.metric("末级风险点", row['末级风险点名称'])
                    st.caption(f"原始链接: {row['url']}")

                st.divider()  # 分割线
    else:
        st.info("没有找到符合条件的数据，请调整筛选器。")

else:
    st.info("请在上方上传包含 title, url, 一级风险点, 末级风险点名称 列的 Excel 文件。")
