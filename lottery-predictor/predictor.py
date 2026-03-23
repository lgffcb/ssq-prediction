#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双色球预测软件 - 统计分析模块
整合多种概率分布：伯努利、正态、指数、二项、泊松、LSTM
"""

import numpy as np
import pandas as pd
from scipy import stats
from collections import Counter
from typing import List, Tuple, Dict
import warnings
warnings.filterwarnings('ignore')


class StatisticalAnalyzer:
    """统计分析器 - 整合多种概率分布"""
    
    def __init__(self, historical_data: pd.DataFrame):
        """
        初始化分析器
        
        Args:
            historical_data: 历史开奖数据 DataFrame
                           包含列：red1, red2, red3, red4, red5, red6, blue
        """
        self.data = historical_data
        self.red_columns = ['red1', 'red2', 'red3', 'red4', 'red5', 'red6']
        
    def analyze_by_period(self, periods: List[int] = [5, 7, 10, 30, 50]) -> Dict:
        """
        按不同周期分析数据
        
        Args:
            periods: 周期列表，如 [5, 7, 10, 30, 50]
            
        Returns:
            各周期的分析结果
        """
        results = {}
        for period in periods:
            if len(self.data) >= period:
                period_data = self.data.tail(period)
                results[f'period_{period}'] = self._analyze_period(period_data, period)
        return results
    
    def _analyze_period(self, data: pd.DataFrame, period: int) -> Dict:
        """分析单个周期的数据"""
        analysis = {
            'period': period,
            'red_ball_freq': self._analyze_red_frequency(data),
            'blue_ball_freq': self._analyze_blue_frequency(data),
            'hot_cold': self._analyze_hot_cold(data),
            'missing': self._analyze_missing(data),
            'sum_stats': self._analyze_sum_statistics(data),
            'ac_index': self._analyze_ac_index(data),
            'span_stats': self._analyze_span(data)
        }
        return analysis
    
    def _analyze_red_frequency(self, data: pd.DataFrame) -> Dict:
        """分析红球频率"""
        all_reds = []
        for col in self.red_columns:
            all_reds.extend(data[col].dropna().astype(int).tolist())
        
        freq = Counter(all_reds)
        total = len(all_reds)
        
        return {
            'frequency': freq,
            'probability': {k: v/total for k, v in freq.items()},
            'most_common': freq.most_common(10),
            'least_common': freq.most_common()[:-11:-1] if len(freq) > 10 else freq.most_common()
        }
    
    def _analyze_blue_frequency(self, data: pd.DataFrame) -> Dict:
        """分析蓝球频率"""
        blues = data['blue'].dropna().astype(int).tolist()
        freq = Counter(blues)
        total = len(blues)
        
        return {
            'frequency': freq,
            'probability': {k: v/total for k, v in freq.items()},
            'most_common': freq.most_common(5),
            'least_common': freq.most_common()[:-6:-1] if len(freq) > 5 else freq.most_common()
        }
    
    def _analyze_hot_cold(self, data: pd.DataFrame) -> Dict:
        """分析冷热号"""
        all_reds = []
        for col in self.red_columns:
            all_reds.extend(data[col].dropna().astype(int).tolist())
        
        freq = Counter(all_reds)
        avg_freq = sum(freq.values()) / len(freq) if freq else 0
        
        hot = [k for k, v in freq.items() if v > avg_freq * 1.2]
        cold = [k for k, v in freq.items() if v < avg_freq * 0.8]
        
        return {
            'hot_numbers': sorted(hot),
            'cold_numbers': sorted(cold),
            'average_frequency': avg_freq
        }
    
    def _analyze_missing(self, data: pd.DataFrame) -> Dict:
        """分析遗漏值"""
        all_reds = []
        for col in self.red_columns:
            all_reds.extend(data[col].dropna().astype(int).tolist())
        
        # 计算每个号码的当前遗漏
        current_missing = {}
        for num in range(1, 34):
            count = 0
            for idx in range(len(self.data)-1, -1, -1):
                row = self.data.iloc[idx]
                if num in row[self.red_columns].values:
                    break
                count += 1
            current_missing[num] = count
        
        return {
            'current_missing': current_missing,
            'max_missing': max(current_missing.items(), key=lambda x: x[1]),
            'min_missing': min(current_missing.items(), key=lambda x: x[1])
        }
    
    def _analyze_sum_statistics(self, data: pd.DataFrame) -> Dict:
        """分析和值统计"""
        sums = data[self.red_columns].sum(axis=1)
        
        return {
            'mean': sums.mean(),
            'std': sums.std(),
            'min': sums.min(),
            'max': sums.max(),
            'recent_trend': sums.tail(5).mean() if len(sums) >= 5 else sums.mean()
        }
    
    def _analyze_ac_index(self, data: pd.DataFrame) -> Dict:
        """分析 AC 指数（数字复杂程度）"""
        def calc_ac(row):
            nums = sorted(row[self.red_columns].dropna().astype(int).tolist())
            if len(nums) < 6:
                return 0
            diffs = []
            for i in range(len(nums)):
                for j in range(i+1, len(nums)):
                    diffs.append(nums[j] - nums[i])
            unique_diffs = len(set(diffs))
            return unique_diffs - 5  # AC = 不同差值数 - (红球数 - 1)
        
        ac_values = data.apply(calc_ac, axis=1)
        return {
            'mean': ac_values.mean(),
            'std': ac_values.std(),
            'recent': ac_values.tail(5).tolist() if len(ac_values) >= 5 else ac_values.tolist()
        }
    
    def _analyze_span(self, data: pd.DataFrame) -> Dict:
        """分析跨度（最大 - 最小）"""
        def calc_span(row):
            nums = row[self.red_columns].dropna().astype(int).tolist()
            return max(nums) - min(nums) if nums else 0
        
        spans = data.apply(calc_span, axis=1)
        return {
            'mean': spans.mean(),
            'std': spans.std(),
            'recent': spans.tail(5).tolist() if len(spans) >= 5 else spans.tolist()
        }


class ProbabilityDistributions:
    """概率分布分析"""
    
    def __init__(self, historical_data: pd.DataFrame):
        self.data = historical_data
        self.red_columns = ['red1', 'red2', 'red3', 'red4', 'red5', 'red6']
    
    def bernoulli_analysis(self, target_number: int) -> Dict:
        """
        伯努利分布分析 - 分析特定号码出现/不出现的概率
        
        Args:
            target_number: 目标号码（1-33）
            
        Returns:
            伯努利分布参数
        """
        appearances = []
        for _, row in self.data.iterrows():
            appeared = 1 if target_number in row[self.red_columns].values else 0
            appearances.append(appeared)
        
        p = np.mean(appearances)  # 成功概率
        
        # 伯努利分布参数
        bernoulli = stats.bernoulli(p)
        
        # 计算连续出现的概率
        consecutive = self._count_consecutive(appearances)
        
        return {
            'number': target_number,
            'probability': p,
            'expected_value': bernoulli.mean(),
            'variance': bernoulli.var(),
            'consecutive_appearances': consecutive,
            'next_appearance_prob': p  # 下一次出现的概率
        }
    
    def _count_consecutive(self, appearances: List[int]) -> List[int]:
        """计算连续出现次数"""
        consecutive = []
        count = 0
        for app in appearances:
            if app == 1:
                count += 1
            else:
                if count > 0:
                    consecutive.append(count)
                count = 0
        if count > 0:
            consecutive.append(count)
        return consecutive if consecutive else [0]
    
    def normal_distribution_analysis(self) -> Dict:
        """
        正态分布分析 - 分析和值的正态分布特性
        
        Returns:
            正态分布参数
        """
        sums = self.data[self.red_columns].sum(axis=1)
        
        mu, sigma = stats.norm.fit(sums)
        
        # 拟合优度检验
        ks_stat, p_value = stats.kstest(sums, 'norm', args=(mu, sigma))
        
        # 预测下期和值范围（95% 置信区间）
        ci_lower, ci_upper = stats.norm.interval(0.95, loc=mu, scale=sigma)
        
        return {
            'mean': mu,
            'std': sigma,
            'ks_statistic': ks_stat,
            'p_value': p_value,
            'is_normal': p_value > 0.05,
            'confidence_interval_95': (ci_lower, ci_upper),
            'predicted_sum_range': (int(ci_lower), int(ci_upper))
        }
    
    def exponential_distribution_analysis(self) -> Dict:
        """
        指数分布分析 - 分析遗漏值的分布
        
        Returns:
            指数分布参数
        """
        # 计算每个号码的遗漏值
        missing_data = []
        for num in range(1, 34):
            count = 0
            for idx in range(len(self.data)-1, -1, -1):
                row = self.data.iloc[idx]
                if num in row[self.red_columns].values:
                    break
                count += 1
            missing_data.append(count)
        
        # 拟合指数分布
        loc, scale = stats.expon.fit(missing_data)
        
        return {
            'location': loc,
            'scale': scale,
            'mean_missing': np.mean(missing_data),
            'predicted_missing': int(scale)  # 预期遗漏值
        }
    
    def binomial_distribution_analysis(self, n_periods: int = 10) -> Dict:
        """
        二项分布分析 - 分析 n 期内号码出现次数
        
        Args:
            n_periods: 期数 n
            
        Returns:
            二项分布参数
        """
        # 计算每个号码在 n 期内的出现次数
        appearance_counts = []
        for num in range(1, 34):
            count = 0
            for idx in range(min(n_periods, len(self.data))):
                row = self.data.iloc[-(idx+1)]
                if num in row[self.red_columns].values:
                    count += 1
            appearance_counts.append(count)
        
        # 二项分布参数估计
        n = n_periods
        p = np.mean(appearance_counts) / n
        
        binom = stats.binom(n, p)
        
        # 计算最可能的出现次数（mode）
        most_likely = int(np.round(binom.mean()))  # 用均值近似
        
        return {
            'n': n,
            'p': p,
            'expected_appearances': binom.mean(),
            'variance': binom.var(),
            'most_likely_count': most_likely,
            'distribution': {k: binom.pmf(k) for k in range(n+1)}
        }
    
    def poisson_distribution_analysis(self) -> Dict:
        """
        泊松分布分析 - 分析号码出现频率
        
        Returns:
            泊松分布参数
        """
        # 计算每个号码的平均出现率
        all_reds = []
        for col in self.red_columns:
            all_reds.extend(self.data[col].dropna().astype(int).tolist())
        
        total_draws = len(self.data)
        freq = Counter(all_reds)
        
        # 泊松分布参数 lambda
        lambda_ = np.mean(list(freq.values())) / total_draws * 6  # 每期 6 个红球
        
        poisson = stats.poisson(lambda_)
        
        return {
            'lambda': lambda_,
            'expected_frequency': poisson.mean(),
            'variance': poisson.var(),
            'probabilities': {k: poisson.pmf(k) for k in range(10)}
        }


class LSTMPredictor:
    """LSTM 深度学习预测"""
    
    def __init__(self, historical_data: pd.DataFrame, sequence_length: int = 10):
        """
        初始化 LSTM 预测器
        
        Args:
            historical_data: 历史数据
            sequence_length: 序列长度（用多少期预测）
        """
        self.data = historical_data
        self.sequence_length = sequence_length
        self.red_columns = ['red1', 'red2', 'red3', 'red4', 'red5', 'red6']
        self.model = None
        self.scalers = {}
        
    def prepare_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        准备 LSTM 训练数据
        
        Returns:
            X: 输入序列, y: 目标值
        """
        # 为每个红球位置准备数据
        X_list = []
        y_list = []
        
        for i in range(len(self.data) - self.sequence_length):
            # 获取序列数据
            sequence = self.data.iloc[i:i+self.sequence_length][self.red_columns].values
            X_list.append(sequence.flatten())
            
            # 目标值：下一期的红球
            next_draw = self.data.iloc[i+self.sequence_length][self.red_columns].values
            y_list.append(next_draw)
        
        return np.array(X_list), np.array(y_list)
    
    def build_model(self, input_shape: int, output_shape: int = 6):
        """
        构建 LSTM 模型
        
        Args:
            input_shape: 输入形状
            output_shape: 输出形状（默认 6 个红球）
        """
        try:
            from tensorflow.keras.models import Sequential
            from tensorflow.keras.layers import LSTM, Dense, Dropout
            from tensorflow.keras.optimizers import Adam
            
            model = Sequential([
                LSTM(128, return_sequences=True, input_shape=(self.sequence_length, 6)),
                Dropout(0.2),
                LSTM(64, return_sequences=True),
                Dropout(0.2),
                LSTM(32),
                Dropout(0.2),
                Dense(64, activation='relu'),
                Dense(output_shape, activation='linear')
            ])
            
            model.compile(
                optimizer=Adam(learning_rate=0.001),
                loss='mse',
                metrics=['mae']
            )
            
            self.model = model
            return True
            
        except ImportError:
            print("⚠️  TensorFlow 未安装，跳过 LSTM 预测")
            return False
    
    def train(self, epochs: int = 50, batch_size: int = 32, validation_split: float = 0.2):
        """
        训练模型
        
        Args:
            epochs: 训练轮数
            batch_size: 批次大小
            validation_split: 验证集比例
        """
        if self.model is None:
            X, y = self.prepare_data()
            X = X.reshape((X.shape[0], self.sequence_length, 6))
            
            if not self.build_model(X.shape[1]):
                return None
        
        X, y = self.prepare_data()
        X = X.reshape((X.shape[0], self.sequence_length, 6))
        
        history = self.model.fit(
            X, y,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            verbose=0
        )
        
        return history
    
    def predict(self) -> np.ndarray:
        """
        预测下一期号码
        
        Returns:
            预测的红球号码
        """
        if self.model is None:
            return None
        
        # 使用最近的数据进行预测
        recent_data = self.data.tail(self.sequence_length)[self.red_columns].values
        recent_data = recent_data.reshape((1, self.sequence_length, 6))
        
        prediction = self.model.predict(recent_data, verbose=0)
        
        return prediction[0]


class LotteryPredictor:
    """双色球预测主类"""
    
    def __init__(self, historical_data: pd.DataFrame):
        """
        初始化预测器
        
        Args:
            historical_data: 历史开奖数据
        """
        self.data = historical_data
        self.stat_analyzer = StatisticalAnalyzer(historical_data)
        self.prob_dist = ProbabilityDistributions(historical_data)
        self.lstm = LSTMPredictor(historical_data)
        
    def comprehensive_analysis(self) -> Dict:
        """
        综合分析
        
        Returns:
            包含所有分析结果的字典
        """
        print("📊 正在进行综合分析...")
        
        results = {
            'period_analysis': self.stat_analyzer.analyze_by_period([5, 7, 10, 30, 50]),
            'bernoulli': self._analyze_all_bernoulli(),
            'normal': self.prob_dist.normal_distribution_analysis(),
            'exponential': self.prob_dist.exponential_distribution_analysis(),
            'binomial': self.prob_dist.binomial_distribution_analysis(),
            'poisson': self.prob_dist.poisson_distribution_analysis()
        }
        
        # LSTM 预测
        print("🤖 训练 LSTM 模型...")
        try:
            history = self.lstm.train(epochs=30, batch_size=16, validation_split=0.2)
            lstm_pred = self.lstm.predict()
            results['lstm_prediction'] = lstm_pred.tolist() if lstm_pred is not None else None
        except Exception as e:
            print(f"⚠️  LSTM 训练失败：{e}")
            results['lstm_prediction'] = None
        
        return results
    
    def _analyze_all_bernoulli(self) -> Dict:
        """分析所有号码的伯努利分布"""
        results = {}
        for num in range(1, 34):
            results[num] = self.prob_dist.bernoulli_analysis(num)
        return results
    
    def generate_prediction(self, weights: Dict[str, float] = None) -> Tuple[List[int], int]:
        """
        生成预测号码
        
        Args:
            weights: 各方法的权重
                {
                    'frequency': 0.2,      # 频率分析
                    'hot_cold': 0.15,      # 冷热号
                    'missing': 0.15,       # 遗漏分析
                    'bernoulli': 0.15,     # 伯努利分布
                    'normal': 0.15,        # 正态分布
                    'lstm': 0.2            # LSTM 预测
                }
        
        Returns:
            (红球列表，蓝球)
        """
        if weights is None:
            weights = {
                'frequency': 0.2,
                'hot_cold': 0.15,
                'missing': 0.15,
                'bernoulli': 0.15,
                'normal': 0.15,
                'lstm': 0.2
            }
        
        # 计算每个红球的综合得分
        red_scores = self._calculate_red_scores(weights)
        
        # 选择得分最高的 6 个红球
        sorted_reds = sorted(red_scores.items(), key=lambda x: x[1], reverse=True)
        predicted_reds = sorted([item[0] for item in sorted_reds[:6]])
        
        # 预测蓝球
        predicted_blue = self._predict_blue()
        
        return predicted_reds, predicted_blue
    
    def _calculate_red_scores(self, weights: Dict[str, float]) -> Dict[int, float]:
        """计算每个红球的综合得分"""
        scores = {num: 0.0 for num in range(1, 34)}
        
        # 1. 频率分析得分
        period_data = self.stat_analyzer.analyze_by_period([30])
        if 'period_30' in period_data:
            freq_prob = period_data['period_30']['red_ball_freq']['probability']
            for num in range(1, 34):
                scores[num] += weights['frequency'] * freq_prob.get(num, 0)
        
        # 2. 冷热号得分（热号得分高）
        hot_cold = period_data.get('period_30', {}).get('hot_cold', {})
        hot_numbers = hot_cold.get('hot_numbers', [])
        for num in hot_numbers:
            scores[num] += weights['hot_cold'] * 0.5
        
        # 3. 遗漏分析得分（遗漏适中的号码）
        missing = period_data.get('period_30', {}).get('missing', {}).get('current_missing', {})
        avg_missing = np.mean(list(missing.values())) if missing else 5
        for num, miss in missing.items():
            # 遗漏值接近平均值的得分高
            deviation = abs(miss - avg_missing)
            scores[num] += weights['missing'] * (1 / (1 + deviation))
        
        # 4. 伯努利分布得分
        bernoulli = self.prob_dist.bernoulli_analysis(1)  # 示例
        for num in range(1, 34):
            bern_result = self.prob_dist.bernoulli_analysis(num)
            scores[num] += weights['bernoulli'] * bern_result['probability']
        
        # 5. 正态分布得分（和值范围内的号码）
        normal = self.prob_dist.normal_distribution_analysis()
        sum_range = normal['predicted_sum_range']
        # 简化：给中间范围的号码加分
        for num in range(8, 26):  # 中间区域
            scores[num] += weights['normal'] * 0.3
        
        # 6. LSTM 预测得分
        lstm_pred = self.lstm.predict()
        if lstm_pred is not None:
            for i, pred_val in enumerate(lstm_pred):
                pred_num = int(round(pred_val))
                if 1 <= pred_num <= 33:
                    scores[pred_num] += weights['lstm'] * 0.5
        
        return scores
    
    def _predict_blue(self) -> int:
        """预测蓝球"""
        blues = self.data['blue'].dropna().astype(int).tolist()
        
        # 频率分析
        freq = Counter(blues)
        most_common = freq.most_common(3)
        
        # 简单策略：从最常见的 3 个中随机选
        candidates = [item[0] for item in most_common]
        return np.random.choice(candidates) if candidates else np.random.randint(1, 17)
    
    def generate_multiple_predictions(self, n: int = 5, 
                                       weights: Dict[str, float] = None) -> List[Dict]:
        """
        生成多组预测号码
        
        Args:
            n: 生成组数
            weights: 权重配置
            
        Returns:
            预测号码列表
        """
        predictions = []
        for i in range(n):
            reds, blue = self.generate_prediction(weights)
            predictions.append({
                'group': i + 1,
                'red_balls': reds,
                'blue_ball': blue,
                'sum': sum(reds),
                'ac_index': self._calc_ac_index(reds)
            })
        return predictions
    
    def _calc_ac_index(self, reds: List[int]) -> int:
        """计算 AC 指数"""
        diffs = []
        for i in range(len(reds)):
            for j in range(i+1, len(reds)):
                diffs.append(reds[j] - reds[i])
        return len(set(diffs)) - 5


def load_historical_data(file_path: str = None) -> pd.DataFrame:
    """
    加载历史数据
    
    Args:
        file_path: 数据文件路径（CSV 格式）
        
    Returns:
        DataFrame 包含历史开奖数据
    """
    if file_path and os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        # 生成模拟数据用于测试
        np.random.seed(42)
        n_draws = 100
        data = []
        for _ in range(n_draws):
            reds = sorted(np.random.choice(33, 6, replace=False) + 1)
            blue = np.random.randint(1, 17)
            data.append([*reds, blue])
        
        df = pd.DataFrame(data, columns=['red1', 'red2', 'red3', 'red4', 'red5', 'red6', 'blue'])
    
    return df


if __name__ == '__main__':
    import os
    
    print("=" * 60)
    print("🎱 双色球预测软件 v1.0")
    print("=" * 60)
    
    # 加载数据
    print("\n📂 加载历史数据...")
    data = load_historical_data()
    print(f"✅ 已加载 {len(data)} 期开奖数据")
    
    # 创建预测器
    predictor = LotteryPredictor(data)
    
    # 综合分析
    print("\n" + "=" * 60)
    results = predictor.comprehensive_analysis()
    
    # 生成预测
    print("\n" + "=" * 60)
    print("🔮 生成预测号码...")
    print("=" * 60)
    
    predictions = predictor.generate_multiple_predictions(n=5)
    
    for pred in predictions:
        reds = pred['red_balls']
        blue = pred['blue_ball']
        print(f"\n第{pred['group']}组:")
        print(f"  红球：{' '.join(f'{r:02d}' for r in reds)}")
        print(f"  蓝球：{blue:02d}")
        print(f"  和值：{pred['sum']} | AC 指数：{pred['ac_index']}")
    
    print("\n" + "=" * 60)
    print("⚠️  免责声明：本软件仅供娱乐和统计研究，不保证中奖！")
    print("=" * 60)
