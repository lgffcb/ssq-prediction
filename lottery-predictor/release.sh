#!/bin/bash
# 双色球预测软件 - 一键 Release 脚本

echo "============================================================"
echo "🚀 双色球预测软件 - 一键 Release"
echo "============================================================"
echo ""

# 检查参数
VERSION=${1:-"v1.0.0"}

echo "📌 版本号：$VERSION"
echo ""

# 1. 检查 Git 状态
echo "1️⃣ 检查 Git 状态..."
cd /home/admin/openclaw/workspace/lottery-predictor

if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  有未提交的更改，请先提交"
    git status
    exit 1
fi
echo "  ✅ Git 状态正常"

# 2. 检查远程仓库
echo ""
echo "2️⃣ 检查远程仓库..."
REMOTE=$(git remote get-url origin 2>/dev/null)
if [ -z "$REMOTE" ]; then
    echo "❌ 未配置远程仓库"
    exit 1
fi
echo "  ✅ 远程仓库：$REMOTE"

# 3. 检查标签
echo ""
echo "3️⃣ 检查标签..."
if git rev-parse "$VERSION" >/dev/null 2>&1; then
    echo "⚠️  标签 $VERSION 已存在"
    read -p "是否删除并重新创建？(y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git tag -d "$VERSION"
        git push origin --delete "$VERSION" 2>/dev/null
    else
        exit 1
    fi
fi

# 4. 创建标签
echo ""
echo "4️⃣ 创建标签 $VERSION..."
git tag "$VERSION"
if [ $? -ne 0 ]; then
    echo "❌ 创建标签失败"
    exit 1
fi
echo "  ✅ 标签已创建"

# 5. 推送标签
echo ""
echo "5️⃣ 推送标签到 GitHub..."
git push origin "$VERSION"
if [ $? -ne 0 ]; then
    echo "❌ 推送标签失败"
    exit 1
fi
echo "  ✅ 标签已推送"

# 6. 显示构建信息
echo ""
echo "============================================================"
echo "✅ Release 已触发！"
echo "============================================================"
echo ""
echo "📊 构建信息:"
echo "  版本：$VERSION"
echo "  时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo "  仓库：$REMOTE"
echo ""
echo "🔗 相关链接:"
echo "  查看构建：https://github.com/lgffcb/excel-extractor/actions"
echo "  下载 Release: https://github.com/lgffcb/excel-extractor/releases"
echo ""
echo "⏱️  构建时间：约 5-10 分钟"
echo ""
echo "💡 提示:"
echo "  1. 访问 GitHub Actions 查看构建进度"
echo "  2. 构建完成后在 Releases 页面下载"
echo "  3. 下载文件：SSQ_Predictor_Windows.zip"
echo ""
