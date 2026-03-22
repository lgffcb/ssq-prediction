#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Review Analyzer - 评论分析工具
使用情感分析来评价评论
"""

import sys
from textblob import TextBlob

def analyze_sentiment(text):
    """分析情感"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    if polarity > 0.1:
        sentiment = "正面 😊"
    elif polarity < -0.1:
        sentiment = "负面 😞"
    else:
        sentiment = "中性 😐"
    
    return {
        'sentiment': sentiment,
        'polarity': polarity,
        'subjectivity': subjectivity
    }

def analyze_reviews(reviews):
    """批量分析评论"""
    results = []
    for review in reviews:
        result = analyze_sentiment(review)
        results.append(result)
    
    # 统计
    positive = sum(1 for r in results if '正面' in r['sentiment'])
    negative = sum(1 for r in results if '负面' in r['sentiment'])
    neutral = sum(1 for r in results if '中性' in r['sentiment'])
    
    print(f"📊 评论分析结果")
    print(f"   总数：{len(reviews)}")
    print(f"   正面：{positive} ({positive/len(reviews)*100:.1f}%)")
    print(f"   负面：{negative} ({negative/len(reviews)*100:.1f}%)")
    print(f"   中性：{neutral} ({neutral/len(reviews)*100:.1f}%)")
    
    return results

def main():
    if len(sys.argv) < 2:
        print("Review Analyzer - 评论分析工具")
        print("\n用法:")
        print("  python reviewanalyzer.py \"评论内容\"")
        print("  python reviewanalyzer.py \"评论 1\" \"评论 2\" ...")
        sys.exit(1)
    
    reviews = sys.argv[1:]
    
    if len(reviews) == 1:
        result = analyze_sentiment(reviews[0])
        print(f"📝 评论：{reviews[0][:100]}...")
        print(f"   情感：{result['sentiment']}")
        print(f"   极性：{result['polarity']:.2f}")
        print(f"   主观性：{result['subjectivity']:.2f}")
    else:
        analyze_reviews(reviews)

if __name__ == '__main__':
    main()
