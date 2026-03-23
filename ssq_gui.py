#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双色球预测软件 - GUI 界面
基于 tkinter 的图形用户界面
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import pandas as pd
import numpy as np
from datetime import datetime
import os
import sys

# 导入预测模块
from predictor import LotteryPredictor
from data_fetcher import DataFetcher


class LotteryPredictorGUI:
    """双色球预测软件 GUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎱 双色球预测软件 v1.0")
        self.root.geometry("1000x700")
        
        self.data = None
        self.predictor = None
        self.fetcher = DataFetcher()
        
        self.create_widgets()
        self.load_sample_data()
    
    def create_widgets(self):
        """创建界面组件"""
        
        # === 标题 ===
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(
            title_frame,
            text="🎱 双色球预测软件",
            font=("Microsoft YaHei UI", 20, "bold")
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame,
            text="基于伯努利、正态、泊松分布 + LSTM 深度学习",
            font=("Microsoft YaHei UI", 10)
        )
        subtitle_label.pack()
        
        # === 数据加载区域 ===
        data_frame = ttk.LabelFrame(self.root, text="📂 数据管理", padding="10")
        data_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # 数据状态
        self.status_var = tk.StringVar(value="未加载数据")
        status_label = ttk.Label(data_frame, textvariable=self.status_var)
        status_label.pack(side=tk.LEFT, padx=10)
        
        # 按钮
        btn_frame = ttk.Frame(data_frame)
        btn_frame.pack(side=tk.RIGHT)
        
        load_btn = ttk.Button(btn_frame, text="📂 加载数据", command=self.load_data)
        load_btn.pack(side=tk.LEFT, padx=5)
        
        update_btn = ttk.Button(btn_frame, text="🔄 更新数据", command=self.update_data)
        update_btn.pack(side=tk.LEFT, padx=5)
        
        sample_btn = ttk.Button(btn_frame, text="📊 示例数据", command=self.load_sample_data)
        sample_btn.pack(side=tk.LEFT, padx=5)
        
        # === 参数设置区域 ===
        param_frame = ttk.LabelFrame(self.root, text="⚙️ 预测参数", padding="10")
        param_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # 期数选择
        ttk.Label(param_frame, text="分析期数:").grid(row=0, column=0, padx=5, pady=5)
        
        self.period_var = tk.StringVar(value="30")
        period_combo = ttk.Combobox(param_frame, textvariable=self.period_var, width=10)
        period_combo['values'] = ('5', '7', '10', '30', '50', '100')
        period_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # 预测组数
        ttk.Label(param_frame, text="预测组数:").grid(row=0, column=2, padx=5, pady=5)
        
        self.groups_var = tk.StringVar(value="5")
        groups_spin = ttk.Spinbox(param_frame, textvariable=self.groups_var, 
                                   from_=1, to=20, width=10)
        groups_spin.grid(row=0, column=3, padx=5, pady=5)
        
        # LSTM 选项
        self.lstm_var = tk.BooleanVar(value=True)
        lstm_check = ttk.Checkbutton(param_frame, text="启用 LSTM 深度学习", 
                                      variable=self.lstm_var)
        lstm_check.grid(row=0, column=4, padx=20, pady=5)
        
        # 权重配置
        ttk.Label(param_frame, text="权重配置:").grid(row=1, column=0, padx=5, pady=5)
        
        self.weight_preset_var = tk.StringVar(value="均衡")
        weight_combo = ttk.Combobox(param_frame, textvariable=self.weight_preset_var, width=15)
        weight_combo['values'] = ('均衡', '偏重频率', '偏重遗漏', '偏重 LSTM')
        weight_combo.grid(row=1, column=1, padx=5, pady=5)
        weight_combo.bind('<<ComboboxSelected>>', self.on_weight_preset_change)
        
        # === 预测按钮 ===
        predict_frame = ttk.Frame(self.root, padding="10")
        predict_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.predict_btn = ttk.Button(
            predict_frame,
            text="🔮 开始预测",
            command=self.run_prediction,
            width=20
        )
        self.predict_btn.pack()
        
        # === 结果显示区域 ===
        result_frame = ttk.LabelFrame(self.root, text="📊 预测结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 结果文本框
        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            height=20,
            font=("Consolas", 11),
            wrap=tk.WORD
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # === 底部按钮 ===
        bottom_frame = ttk.Frame(self.root, padding="10")
        bottom_frame.pack(fill=tk.X, padx=20, pady=10)
        
        export_btn = ttk.Button(bottom_frame, text="💾 导出结果", command=self.export_results)
        export_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(bottom_frame, text="🗑️ 清空结果", command=self.clear_results)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # 版权信息
        copyright_label = ttk.Label(
            bottom_frame,
            text="© 2026 双色球预测软件 | 仅供娱乐参考",
            foreground="gray"
        )
        copyright_label.pack(side=tk.RIGHT)
    
    def load_sample_data(self):
        """加载示例数据"""
        try:
            self.log("📂 加载示例数据...")
            self.data = self.fetcher.fetch_from_api(source='mock')
            self.predictor = LotteryPredictor(self.data)
            self.status_var.set(f"✅ 已加载 {len(self.data)} 期示例数据")
            self.log(f"✅ 已加载 {len(self.data)} 期数据\n")
            self.log("最近 5 期开奖:\n")
            self.log(self.data.tail(5).to_string(index=False) + "\n\n")
        except Exception as e:
            messagebox.showerror("错误", f"加载数据失败:\n{e}")
    
    def load_data(self):
        """加载本地数据文件"""
        file_path = filedialog.askopenfilename(
            title="选择数据文件",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.data = self.fetcher.load_from_csv(file_path)
                if self.data is not None:
                    self.predictor = LotteryPredictor(self.data)
                    self.status_var.set(f"✅ 已加载 {len(self.data)} 期数据")
                    self.log(f"✅ 从 {file_path} 加载了 {len(self.data)} 期数据\n\n")
            except Exception as e:
                messagebox.showerror("错误", f"加载数据失败:\n{e}")
    
    def update_data(self):
        """更新数据"""
        try:
            self.log("🔄 正在更新数据...\n")
            self.data = self.fetcher.update_data('data/historical_data.csv', source='mock')
            self.predictor = LotteryPredictor(self.data)
            self.status_var.set(f"✅ 已更新到 {len(self.data)} 期")
            self.log(f"✅ 数据更新完成：共 {len(self.data)} 期\n\n")
        except Exception as e:
            messagebox.showerror("错误", f"更新数据失败:\n{e}")
    
    def get_weights(self) -> dict:
        """获取权重配置"""
        preset = self.weight_preset_var.get()
        
        if preset == '均衡':
            return {
                'frequency': 0.2,
                'hot_cold': 0.15,
                'missing': 0.15,
                'bernoulli': 0.15,
                'normal': 0.15,
                'lstm': 0.2
            }
        elif preset == '偏重频率':
            return {
                'frequency': 0.35,
                'hot_cold': 0.2,
                'missing': 0.1,
                'bernoulli': 0.15,
                'normal': 0.1,
                'lstm': 0.1
            }
        elif preset == '偏重遗漏':
            return {
                'frequency': 0.15,
                'hot_cold': 0.1,
                'missing': 0.35,
                'bernoulli': 0.15,
                'normal': 0.15,
                'lstm': 0.1
            }
        elif preset == '偏重 LSTM':
            return {
                'frequency': 0.15,
                'hot_cold': 0.1,
                'missing': 0.1,
                'bernoulli': 0.15,
                'normal': 0.1,
                'lstm': 0.4
            }
    
    def run_prediction(self):
        """运行预测"""
        if self.data is None:
            messagebox.showwarning("警告", "请先加载数据！")
            return
        
        self.predict_btn.config(state=tk.DISABLED)
        self.log("=" * 60 + "\n")
        self.log("🔮 开始预测...\n\n")
        
        try:
            # 获取参数
            n_groups = int(self.groups_var.get())
            weights = self.get_weights()
            use_lstm = self.lstm_var.get()
            
            if not use_lstm:
                weights['lstm'] = 0
                # 重新分配权重
                total = sum(weights.values())
                weights = {k: v/total for k, v in weights.items()}
            
            # 运行预测
            self.log("📊 正在分析历史数据...\n")
            self.root.update()
            
            self.log("🤖 训练模型...\n")
            self.root.update()
            
            predictions = self.predictor.generate_multiple_predictions(
                n=n_groups,
                weights=weights
            )
            
            # 显示结果
            self.log("\n" + "=" * 60 + "\n")
            self.log(f"📋 预测结果（共 {n_groups} 组）\n")
            self.log("=" * 60 + "\n\n")
            
            for pred in predictions:
                reds = pred['red_balls']
                blue = pred['blue_ball']
                self.log(f"第{pred['group']:02d}组:\n")
                self.log(f"  红球：{' '.join(f'{r:02d}' for r in reds)}\n")
                self.log(f"  蓝球：{blue:02d}\n")
                self.log(f"  和值：{pred['sum']:3d} | AC 指数：{pred['ac_index']}\n\n")
            
            self.log("=" * 60 + "\n")
            self.log("⚠️  免责声明：本软件仅供娱乐和统计研究，不保证中奖！\n")
            self.log("=" * 60 + "\n")
            
        except Exception as e:
            messagebox.showerror("错误", f"预测失败:\n{e}")
            self.log(f"❌ 错误：{e}\n")
        
        finally:
            self.predict_btn.config(state=tk.NORMAL)
    
    def export_results(self):
        """导出结果"""
        file_path = filedialog.asksaveasfilename(
            title="保存预测结果",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.result_text.get("1.0", tk.END))
                messagebox.showinfo("成功", f"结果已保存到:\n{file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败:\n{e}")
    
    def clear_results(self):
        """清空结果"""
        self.result_text.delete("1.0", tk.END)
    
    def log(self, message: str):
        """输出日志"""
        self.result_text.insert(tk.END, message)
        self.result_text.see(tk.END)
    
    def on_weight_preset_change(self, event):
        """权重预设改变"""
        preset = self.weight_preset_var.get()
        self.log(f"\n⚙️  权重配置：{preset}\n\n")


def main():
    """主函数"""
    root = tk.Tk()
    
    # 设置样式
    style = ttk.Style()
    style.theme_use('clam')
    
    app = LotteryPredictorGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
