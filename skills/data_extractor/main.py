#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据自动提取汇总 APP
支持多格式数据导入、智能提取、自动汇总
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
import ezdxf

# 设置页面配置
st.set_page_config(
    page_title="数据提取汇总助手",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 创建目录
os.makedirs('skills/data_extractor/output', exist_ok=True)
os.makedirs('skills/data_extractor/data', exist_ok=True)

# 侧边栏
st.sidebar.title("📊 数据提取汇总助手")
st.sidebar.markdown("---")

# 功能选择
menu = st.sidebar.radio(
    "选择功能",
    ["📂 文件导入", "📊 数据预览", "🔧 数据处理", "📈 汇总分析", "📄 导出报表"]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**版本：** v1.0  
**开发日期：** 2026-03-22  
**支持格式：** Excel/CSV/DXF/JSON
""")

# ==================== 文件导入 ====================
if menu == "📂 文件导入":
    st.title("📂 文件导入")
    st.markdown("支持多种格式数据文件导入")
    
    # 文件上传
    uploaded_files = st.file_uploader(
        "上传数据文件",
        type=['xlsx', 'xls', 'csv', 'json', 'dxf', 'txt'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.success(f"✅ 已上传 {len(uploaded_files)} 个文件")
        
        # 显示文件列表
        st.subheader("📁 文件列表")
        file_info = []
        for f in uploaded_files:
            file_info.append({
                '文件名': f.name,
                '大小': f'{f.size/1024:.1f} KB',
                '类型': f.name.split('.')[-1].upper()
            })
        
        file_df = pd.DataFrame(file_info)
        st.dataframe(file_df, use_container_width=True, hide_index=True)
        
        # 保存上传的文件
        saved_files = []
        for f in uploaded_files:
            save_path = f"skills/data_extractor/data/{f.name}"
            with open(save_path, 'wb') as save_f:
                save_f.write(f.getvalue())
            saved_files.append(save_path)
        
        st.session_state['uploaded_files'] = saved_files
        st.success(f"✅ 文件已保存至 skills/data_extractor/data/")
        
        # 自动识别并预览
        if st.button("🔍 自动识别并预览"):
            st.subheader("📊 数据预览")
            
            for f in uploaded_files:
                st.markdown(f"### 📄 {f.name}")
                
                try:
                    if f.name.endswith(('.xlsx', '.xls')):
                        df = pd.read_excel(f)
                        st.write(f"**行数：** {len(df)} | **列数：** {len(df.columns)}")
                        st.dataframe(df.head(), use_container_width=True)
                    
                    elif f.name.endswith('.csv'):
                        df = pd.read_csv(f)
                        st.write(f"**行数：** {len(df)} | **列数：** {len(df.columns)}")
                        st.dataframe(df.head(), use_container_width=True)
                    
                    elif f.name.endswith('.json'):
                        df = pd.read_json(f)
                        st.write(f"**行数：** {len(df)} | **列数：** {len(df.columns)}")
                        st.dataframe(df.head(), use_container_width=True)
                    
                    elif f.name.endswith('.dxf'):
                        # 保存后读取
                        save_path = f"skills/data_extractor/data/{f.name}"
                        doc = ezdxf.readfile(save_path)
                        msp = doc.modelspace()
                        
                        entities = {}
                        for entity in msp:
                            etype = entity.dxftype()
                            entities[etype] = entities.get(etype, 0) + 1
                        
                        st.write(f"**实体总数：** {sum(entities.values())}")
                        entity_df = pd.DataFrame(list(entities.items()), columns=['实体类型', '数量'])
                        st.dataframe(entity_df, use_container_width=True, hide_index=True)
                    
                    elif f.name.endswith('.txt'):
                        with open(f, 'r', encoding='utf-8') as txt_f:
                            lines = txt_f.readlines()
                        st.write(f"**行数：** {len(lines)}")
                        st.text(''.join(lines[:20]))
                    
                except Exception as e:
                    st.error(f"❌ 读取失败：{str(e)}")
    
    else:
        st.info("📎 请上传数据文件，支持 Excel/CSV/JSON/DXF/TXT 格式")
        
        # 示例文件
        st.subheader("📋 示例数据")
        st.code("""
# Excel 示例
| 管径 | 材质 | 长度 (m) | 数量 |
|------|------|---------|------|
| DN200 | HDPE | 100 | 50 |
| DN300 | HDPE | 150 | 30 |

# CSV 示例
井类型，井深，数量
污水检查井，1.5,20
污水检查井，2.0,15
        """)

# ==================== 数据预览 ====================
elif menu == "📊 数据预览":
    st.title("📊 数据预览")
    st.markdown("查看已导入数据的详细信息")
    
    # 检查是否有上传的文件
    if 'uploaded_files' not in st.session_state:
        st.info("📎 请先在【文件导入】页面上传文件")
    else:
        files = st.session_state['uploaded_files']
        st.write(f"已导入 {len(files)} 个文件")
        
        # 选择文件
        selected_file = st.selectbox("选择文件", files)
        
        if selected_file:
            try:
                # 读取并显示
                if selected_file.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(selected_file)
                    st.write(f"**行数：** {len(df)} | **列数：** {len(df.columns)}")
                    st.dataframe(df, use_container_width=True)
                
                elif selected_file.endswith('.csv'):
                    df = pd.read_csv(selected_file)
                    st.write(f"**行数：** {len(df)} | **列数：** {len(df.columns)}")
                    st.dataframe(df, use_container_width=True)
                
                elif selected_file.endswith('.json'):
                    df = pd.read_json(selected_file)
                    st.write(f"**行数：** {len(df)} | **列数：** {len(df.columns)}")
                    st.dataframe(df, use_container_width=True)
                
                # 统计信息
                st.subheader("📊 数据统计")
                if df.select_dtypes(include=['number']).shape[1] > 0:
                    st.write("数值列统计：")
                    st.dataframe(df.describe(), use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ 读取失败：{str(e)}")

# ==================== 数据处理 ====================
elif menu == "🔧 数据处理":
    st.title("🔧 数据处理")
    st.markdown("对数据进行清洗、转换、合并等操作")
    
    # 检查是否有上传的文件
    if 'uploaded_files' not in st.session_state:
        st.info("📎 请先在【文件导入】页面上传文件")
    else:
        files = st.session_state['uploaded_files']
        
        # 选择要处理的文件
        selected_files = st.multiselect("选择文件", files)
        
        if selected_files:
            st.subheader("🔧 处理选项")
            
            col1, col2 = st.columns(2)
            
            with col1:
                merge_files = st.checkbox("📎 合并多个文件", value=False)
                remove_duplicates = st.checkbox("🗑️ 删除重复值", value=True)
                fill_na = st.checkbox("🔢 填充空值", value=True)
            
            with col2:
                add_index = st.checkbox("📝 添加序号", value=True)
                sort_by = st.selectbox("排序字段", ["无"] + list(pd.read_excel(selected_files[0]).columns if selected_files[0].endswith('.xlsx') else []))
            
            if st.button("🚀 开始处理", type="primary"):
                try:
                    # 读取数据
                    dfs = []
                    for f in selected_files:
                        if f.endswith(('.xlsx', '.xls')):
                            dfs.append(pd.read_excel(f))
                        elif f.endswith('.csv'):
                            dfs.append(pd.read_csv(f))
                        elif f.endswith('.json'):
                            dfs.append(pd.read_json(f))
                    
                    # 合并
                    if merge_files and len(dfs) > 1:
                        df_merged = pd.concat(dfs, ignore_index=True)
                        st.success(f"✅ 已合并 {len(dfs)} 个文件，共 {len(df_merged)} 行")
                    else:
                        df_merged = dfs[0] if dfs else pd.DataFrame()
                    
                    # 删除重复
                    if remove_duplicates:
                        before = len(df_merged)
                        df_merged = df_merged.drop_duplicates()
                        after = len(df_merged)
                        st.info(f"🗑️ 删除 {before - after} 条重复记录")
                    
                    # 填充空值
                    if fill_na:
                        df_merged = df_merged.fillna(0)
                        st.info("🔢 空值已填充为 0")
                    
                    # 添加序号
                    if add_index:
                        df_merged.insert(0, '序号', range(1, len(df_merged) + 1))
                    
                    # 排序
                    if sort_by != "无" and sort_by in df_merged.columns:
                        df_merged = df_merged.sort_values(by=sort_by)
                    
                    # 显示结果
                    st.subheader("📊 处理结果")
                    st.dataframe(df_merged.head(), use_container_width=True)
                    st.write(f"总行数：{len(df_merged)}")
                    
                    # 保存
                    st.session_state['processed_data'] = df_merged
                    
                    if st.button("💾 保存结果"):
                        output_path = "skills/data_extractor/output/处理结果.xlsx"
                        df_merged.to_excel(output_path, index=False)
                        st.success(f"✅ 已保存至 {output_path}")
                
                except Exception as e:
                    st.error(f"❌ 处理失败：{str(e)}")

# ==================== 汇总分析 ====================
elif menu == "📈 汇总分析":
    st.title("📈 汇总分析")
    st.markdown("对数据进行分类汇总和统计分析")
    
    # 检查是否有处理过的数据
    if 'processed_data' not in st.session_state:
        st.info("📎 请先在【数据处理】页面处理数据")
    else:
        df = st.session_state['processed_data']
        
        st.subheader("📊 数据概览")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("总行数", len(df))
        with col2:
            st.metric("总列数", len(df.columns))
        with col3:
            st.metric("数值列", df.select_dtypes(include=['number']).shape[1])
        
        # 选择汇总字段
        st.subheader("📈 汇总设置")
        
        col4, col5 = st.columns(2)
        
        with col4:
            group_by = st.multiselect("分组字段", df.columns.tolist())
        
        with col5:
            agg_columns = st.multiselect("汇总字段", df.select_dtypes(include=['number']).columns.tolist())
        
        if st.button("🔍 开始汇总"):
            if group_by and agg_columns:
                try:
                    # 分组汇总
                    summary = df.groupby(group_by)[agg_columns].sum().reset_index()
                    
                    st.subheader("📊 汇总结果")
                    st.dataframe(summary, use_container_width=True)
                    
                    # 保存
                    st.session_state['summary_data'] = summary
                    
                    if st.button("💾 保存汇总"):
                        output_path = "skills/data_extractor/output/汇总结果.xlsx"
                        summary.to_excel(output_path, index=False)
                        st.success(f"✅ 已保存至 {output_path}")
                    
                    # 可视化
                    if len(agg_columns) > 0 and len(summary) > 0:
                        st.subheader("📊 可视化")
                        chart_type = st.selectbox("图表类型", ["柱状图", "饼图", "折线图"])
                        
                        if chart_type == "柱状图":
                            st.bar_chart(summary.set_index(group_by[0] if group_by else 0)[agg_columns])
                        elif chart_type == "饼图":
                            st.write("饼图需要选择单个汇总字段")
                        elif chart_type == "折线图":
                            st.line_chart(summary.set_index(group_by[0] if group_by else 0)[agg_columns])
                
                except Exception as e:
                    st.error(f"❌ 汇总失败：{str(e)}")
            else:
                st.warning("⚠️ 请选择分组字段和汇总字段")

# ==================== 导出报表 ====================
elif menu == "📄 导出报表":
    st.title("📄 导出报表")
    st.markdown("导出处理结果和汇总报表")
    
    # 检查输出目录
    output_dir = "skills/data_extractor/output"
    if os.path.exists(output_dir):
        output_files = os.listdir(output_dir)
        
        if output_files:
            st.subheader("📁 可用文件")
            for f in output_files:
                st.write(f"📄 {f}")
            
            # 下载
            selected_file = st.selectbox("选择下载文件", output_files)
            
            if selected_file:
                file_path = f"{output_dir}/{selected_file}"
                with open(file_path, 'rb') as f:
                    st.download_button(
                        label="📥 下载文件",
                        data=f.read(),
                        file_name=selected_file,
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
        else:
            st.info("📎 暂无输出文件")
    else:
        st.info("📎 暂无输出文件")
    
    # 生成综合报告
    st.subheader("📊 生成综合报告")
    
    if st.button("📄 生成分析报告"):
        report_content = f"""
# 数据自动提取汇总报告

**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**数据来源：** 用户上传文件  
**处理工具：** 数据提取汇总助手 v1.0

---

## 一、数据概览

- 总文件数：{len(st.session_state.get('uploaded_files', []))}
- 总行数：{len(st.session_state.get('processed_data', pd.DataFrame()))}
- 总列数：{len(st.session_state.get('processed_data', pd.DataFrame()).columns) if 'processed_data' in st.session_state else 0}

## 二、处理过程

1. 文件导入
2. 数据预览
3. 数据清洗
4. 汇总分析

## 三、汇总结果

详见附带的 Excel 文件。

## 四、说明

本报告由数据提取汇总助手自动生成，仅供参考。

---

**技术支持：** 发财吧·严谨专业版
"""
        
        st.download_button(
            label="📥 下载分析报告",
            data=report_content,
            file_name=f"数据分析报告_{datetime.now().strftime('%Y%m%d')}.md",
            mime='text/markdown'
        )
        
        st.success("✅ 报告已生成")

# 页脚
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    数据提取汇总助手 v1.0 | 开发日期：2026-03-22 | 发财吧·严谨专业版
    </div>
    """,
    unsafe_allow_html=True
)
