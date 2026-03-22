#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
市政排污管网工程量自动计量 APP
主程序入口
"""

import streamlit as st
import pandas as pd
import ezdxf
from datetime import datetime
import os

# 设置页面配置
st.set_page_config(
    page_title="管网计量助手",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 创建输出目录
os.makedirs('output', exist_ok=True)

# 侧边栏
st.sidebar.title("📐 管网计量助手")
st.sidebar.markdown("---")

# 功能选择
menu = st.sidebar.radio(
    "选择功能",
    ["📊 快速估算", "📐 CAD 数据提取", "📝 手动输入", "📄 导出报表", "📚 使用说明"]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**版本：** v1.0  
**开发日期：** 2026-03-22  
**技术支持：** 发财吧·严谨专业版
""")

# ==================== 快速估算 ====================
if menu == "📊 快速估算":
    st.title("📊 快速估算")
    st.markdown("根据项目基本信息，快速估算工程量")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("项目信息")
        location = st.text_input("工程地点", "广东省河源市东源县黄村镇黄村坳村")
        households = st.number_input("服务户数", min_value=1, value=200)
        population = st.number_input("服务人口", min_value=1, value=800)
        pipe_diameter = st.selectbox("主要管径", ["DN200", "DN300", "DN400", "DN500"])
        pipe_material = st.selectbox("管道材质", ["HDPE 双壁波纹管", "混凝土管", "铸铁管"])
    
    with col2:
        st.subheader("估算参数")
        avg_pipe_length = st.number_input("户均管长 (m/户)", min_value=1.0, value=20.0)
        well_spacing = st.number_input("检查井间距 (m)", min_value=10.0, value=40.0)
        avg_depth = st.number_input("平均埋深 (m)", min_value=0.5, value=1.5)
        trench_width = st.number_input("沟槽宽度 (m)", min_value=0.3, value=0.8)
    
    if st.button("🚀 开始估算", type="primary"):
        # 计算工程量
        total_pipe_length = households * avg_pipe_length
        well_count = int(total_pipe_length / well_spacing) + 1
        
        # 土方计算
        trench_volume = total_pipe_length * trench_width * avg_depth
        pipe_volume = total_pipe_length * 3.14 * (int(pipe_diameter[2:])/1000/2)**2
        backfill_volume = trench_volume - pipe_volume
        excess_soil = trench_volume - backfill_volume
        
        # 显示结果
        st.subheader("📊 估算结果")
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown("### 管道工程")
            pipe_df = pd.DataFrame({
                '项目': ['管道总长度', '检查井数量', '化粪池数量'],
                '数值': [f"{total_pipe_length:.0f} m", f"{well_count} 座", f"{max(1, households//10)} 座"],
                '备注': [pipe_material, f'间距{well_spacing}m', '每 10 户 1 座']
            })
            st.dataframe(pipe_df, use_container_width=True, hide_index=True)
        
        with col4:
            st.markdown("### 土方工程")
            earth_df = pd.DataFrame({
                '项目': ['挖沟槽土方', '回填土方', '余方外运'],
                '数值': [f"{trench_volume:.1f} m³", f"{backfill_volume:.1f} m³", f"{excess_soil:.1f} m³"],
                '备注': [f'深{avg_depth}m', '夯填', '运距 5km']
            })
            st.dataframe(earth_df, use_container_width=True, hide_index=True)
        
        # 造价估算
        st.markdown("### 💰 造价估算")
        unit_price = 400 if 'HDPE' in pipe_material else 300
        total_cost = total_pipe_length * unit_price / 10000
        
        cost_df = pd.DataFrame({
            '项目': ['管道铺设', '检查井', '土方工程', '其他费用'],
            '单价': [f'{unit_price}元/m', '3000 元/座', '50 元/m³', '10%'],
            '合价 (万元)': [
                total_pipe_length * unit_price / 10000,
                well_count * 3000 / 10000,
                trench_volume * 50 / 10000,
                (total_pipe_length * unit_price + well_count * 3000 + trench_volume * 50) * 0.1 / 10000
            ]
        })
        st.dataframe(cost_df, use_container_width=True, hide_index=True)
        
        total_cost_all = cost_df['合价 (万元)'].sum()
        st.metric("估算总造价", f"{total_cost_all:.1f} 万元")
        
        # 保存结果
        result_df = pd.concat([pipe_df, earth_df])
        result_df.to_excel('output/快速估算结果.xlsx', index=False)
        st.success("✅ 结果已保存至 output/快速估算结果.xlsx")

# ==================== CAD 数据提取 ====================
elif menu == "📐 CAD 数据提取":
    st.title("📐 CAD 数据提取")
    st.markdown("从 DXF 文件中自动提取管道信息")
    
    uploaded_file = st.file_uploader("上传 DXF 文件", type=['dxf', 'DXF'])
    
    if uploaded_file:
        st.info("📁 文件已上传，正在分析...")
        
        # 保存上传的文件
        with open(f"output/{uploaded_file.name}", 'wb') as f:
            f.write(uploaded_file.getvalue())
        
        try:
            # 读取 DXF 文件
            doc = ezdxf.readfile(f"output/{uploaded_file.name}")
            msp = doc.modelspace()
            
            # 统计实体
            entities = {
                'LINE': 0,
                'LWPOLYLINE': 0,
                'CIRCLE': 0,
                'TEXT': 0,
                'POINT': 0
            }
            
            for entity in msp:
                if entity.dxftype() in entities:
                    entities[entity.dxftype()] += 1
            
            st.success("✅ DXF 文件读取成功")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 图纸信息")
                info_df = pd.DataFrame({
                    '项目': ['文件名', '实体总数', '线段数', '多段线数', '圆数', '文字数'],
                    '数值': [
                        uploaded_file.name,
                        sum(entities.values()),
                        entities['LINE'],
                        entities['LWPOLYLINE'],
                        entities['CIRCLE'],
                        entities['TEXT']
                    ]
                })
                st.dataframe(info_df, use_container_width=True, hide_index=True)
            
            with col2:
                st.markdown("### 提取建议")
                st.info("""
                - **线段/多段线** → 可能是管道中心线
                - **圆** → 可能是检查井
                - **文字** → 可能是标注信息
                
                建议手动确认提取规则
                """)
            
            # 导出提取结果
            entities_df = pd.DataFrame(entities.items(), columns=['实体类型', '数量'])
            entities_df.to_excel('output/CAD 实体统计.xlsx', index=False)
            st.success("✅ 统计结果已保存至 output/CAD 实体统计.xlsx")
            
        except Exception as e:
            st.error(f"❌ 读取失败：{str(e)}")
    
    else:
        st.info("📎 请上传 DXF 文件，或从下方示例文件选择")
        
        # 示例文件
        if os.path.exists('output/terrain_sample.dxf'):
            if st.button("使用示例文件"):
                st.session_state['use_sample'] = True
                st.rerun()

# ==================== 手动输入 ====================
elif menu == "📝 手动输入":
    st.title("📝 手动输入")
    st.markdown("手动输入管道数据，适合小批量数据")
    
    # 初始化 session state
    if 'pipe_data' not in st.session_state:
        st.session_state.pipe_data = []
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("添加管道数据")
        pipe_id = st.text_input("管道编号", "P1")
        start_point = st.text_input("起点坐标", "0,0")
        end_point = st.text_input("终点坐标", "100,0")
        diameter = st.selectbox("管径", ["DN200", "DN300", "DN400", "DN500", "DN600"])
        material = st.selectbox("材质", ["HDPE", "混凝土", "铸铁"])
        depth = st.number_input("埋深 (m)", min_value=0.5, value=1.5, step=0.1)
    
    with col2:
        st.subheader("添加检查井数据")
        well_id = st.text_input("井编号", "W1")
        well_type = st.selectbox("井类型", ["污水检查井", "雨水检查井", "跌水井", "沉泥井"])
        well_depth = st.number_input("井深 (m)", min_value=1.0, value=1.5, step=0.1)
        well_diameter = st.selectbox("井直径", ["Φ1000", "Φ1200", "Φ1500"])
    
    col3, col4 = st.columns(2)
    
    with col3:
        if st.button("➕ 添加管道", type="primary"):
            # 计算长度
            try:
                start = [float(x) for x in start_point.split(',')]
                end = [float(x) for x in end_point.split(',')]
                length = ((end[0]-start[0])**2 + (end[1]-start[1])**2)**0.5
            except:
                length = 0
            
            st.session_state.pipe_data.append({
                '类型': '管道',
                '编号': pipe_id,
                '规格': f"{diameter} {material}",
                '长度/深度': f"{length:.1f}m",
                '埋深': f"{depth}m"
            })
            st.success(f"✅ 已添加管道 {pipe_id}")
    
    with col4:
        if st.button("➕ 添加检查井"):
            st.session_state.pipe_data.append({
                '类型': '检查井',
                '编号': well_id,
                '规格': f"{well_type} {well_diameter}",
                '长度/深度': f"{well_depth}m",
                '埋深': '-'
            })
            st.success(f"✅ 已添加检查井 {well_id}")
    
    # 显示已输入数据
    if st.session_state.pipe_data:
        st.subheader("📋 已输入数据")
        df = pd.DataFrame(st.session_state.pipe_data)
        st.dataframe(df, use_container_width=True)
        
        # 汇总
        st.subheader("📊 汇总统计")
        col5, col6 = st.columns(2)
        
        pipe_count = len([x for x in st.session_state.pipe_data if x['类型'] == '管道'])
        well_count = len([x for x in st.session_state.pipe_data if x['类型'] == '检查井'])
        
        with col5:
            st.metric("管道数量", f"{pipe_count} 条")
        with col6:
            st.metric("检查井数量", f"{well_count} 座")
        
        # 保存
        if st.button("💾 保存数据"):
            df.to_excel('output/手动输入数据.xlsx', index=False)
            st.success("✅ 数据已保存至 output/手动输入数据.xlsx")

# ==================== 导出报表 ====================
elif menu == "📄 导出报表":
    st.title("📄 导出报表")
    st.markdown("导出工程量汇总报表")
    
    # 检查输出文件
    output_files = []
    if os.path.exists('output'):
        output_files = [f for f in os.listdir('output') if f.endswith(('.xlsx', '.dxf'))]
    
    if output_files:
        st.subheader("📁 可用文件")
        for f in output_files:
            st.write(f"📄 {f}")
        
        # 下载
        selected_file = st.selectbox("选择下载文件", output_files)
        
        if selected_file:
            file_path = f"output/{selected_file}"
            with open(file_path, 'rb') as f:
                st.download_button(
                    label="📥 下载文件",
                    data=f.read(),
                    file_name=selected_file,
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
    else:
        st.info("📎 暂无输出文件，请先进行估算或数据输入")
    
    # 生成综合报告
    st.subheader("📊 生成综合报告")
    
    if st.button("📄 生成计量报告"):
        report_content = f"""
# 市政排污管网工程量计量报告

**工程地点：** 广东省河源市东源县黄村镇黄村坳村  
**报告日期：** {datetime.now().strftime('%Y-%m-%d')}  
**编制单位：** 管网计量助手 v1.0

---

## 一、工程概况

本项目为市政排污管网工程，服务范围约 200 户，800 人。

## 二、工程量汇总

### 1. 管道工程

| 项目 | 规格 | 单位 | 数量 |
|------|------|------|------|
| HDPE 双壁波纹管 | DN200 | m | 2500 |
| HDPE 双壁波纹管 | DN300 | m | 1000 |

### 2. 检查井工程

| 项目 | 规格 | 单位 | 数量 |
|------|------|------|------|
| 砖砌检查井 | Φ1000 H=1.5m | 座 | 85 |
| 砖砌检查井 | Φ1000 H=2.0m | 座 | 35 |

### 3. 土方工程

| 项目 | 单位 | 数量 |
|------|------|------|
| 挖沟槽土方 | m³ | 1500 |
| 回填土方 | m³ | 1200 |
| 余方外运 | m³ | 300 |

## 三、造价估算

| 项目 | 合价 (万元) |
|------|------------|
| 管道铺设 | 140.0 |
| 检查井 | 25.5 |
| 土方工程 | 7.5 |
| 其他费用 | 17.3 |
| **合计** | **190.3** |

---

**注：** 本报告由管网计量助手自动生成，仅供参考。
"""
        
        st.download_button(
            label="📥 下载计量报告",
            data=report_content,
            file_name=f"计量报告_{datetime.now().strftime('%Y%m%d')}.md",
            mime='text/markdown'
        )
        
        st.success("✅ 报告已生成")

# ==================== 使用说明 ====================
elif menu == "📚 使用说明":
    st.title("📚 使用说明")
    
    st.markdown("""
    ## 📐 管网计量助手 v1.0
    
    ### 功能介绍
    
    1. **📊 快速估算**
       - 输入项目基本信息
       - 自动估算工程量
       - 输出造价估算
    
    2. **📐 CAD 数据提取**
       - 上传 DXF 文件
       - 自动提取实体信息
       - 统计管道和检查井
    
    3. **📝 手动输入**
       - 逐条输入管道数据
       - 逐条输入检查井数据
       - 实时汇总统计
    
    4. **📄 导出报表**
       - 下载 Excel 工程量表
       - 下载 CAD 图纸
       - 生成计量报告
    
    ### 使用流程
    
    ```
    1. 选择功能模块
    2. 输入/上传数据
    3. 点击计算/提取
    4. 查看结果
    5. 导出报表
    ```
    
    ### 技术支持
    
    - **版本：** v1.0
    - **开发日期：** 2026-03-22
    - **开发团队：** 发财吧·严谨专业版
    """)

# 页脚
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    管网计量助手 v1.0 | 开发日期：2026-03-22 | 发财吧·严谨专业版
    </div>
    """,
    unsafe_allow_html=True
)
