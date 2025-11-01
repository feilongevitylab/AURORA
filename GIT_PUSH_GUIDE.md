# Git 推送指南

项目已经成功提交到本地仓库（32个文件，11450行代码）。现在需要推送到 GitHub。

## 已完成的步骤

✅ Git 仓库已初始化  
✅ 远程仓库已添加：https://github.com/feilongevitylab/AURORA.git  
✅ 所有文件已提交（包括 mock_hrv_data.csv）  
✅ 分支已设置为 main  

## 推送方法

### 方法 1: 使用 GitHub CLI（推荐）

如果已安装 GitHub CLI：

```bash
cd /Users/jialianzhang/Desktop/aurora
gh auth login
git push -u origin main
```

### 方法 2: 使用 SSH（推荐用于频繁推送）

1. 生成 SSH 密钥（如果还没有）：
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

2. 将 SSH 公钥添加到 GitHub

3. 更改远程仓库 URL：
```bash
cd /Users/jialianzhang/Desktop/aurora
git remote set-url origin git@github.com:feilongevitylab/AURORA.git
git push -u origin main
```

### 方法 3: 使用个人访问令牌（Personal Access Token）

1. 在 GitHub 上创建个人访问令牌：
   - 访问：https://github.com/settings/tokens
   - 点击 "Generate new token (classic)"
   - 选择权限：至少勾选 `repo` 权限
   - 复制生成的令牌

2. 推送时使用令牌：
```bash
cd /Users/jialianzhang/Desktop/aurora
git push -u origin main
# Username: feilongevitylab
# Password: [粘贴你的个人访问令牌]
```

### 方法 4: 使用 GitHub Desktop

如果安装了 GitHub Desktop：
1. 在 GitHub Desktop 中打开此仓库
2. 点击 "Push origin" 按钮

## 验证推送

推送成功后，访问 https://github.com/feilongevitylab/AURORA 确认文件已上传。

## 已提交的文件列表

- ✅ 后端代码（FastAPI + Agents）
- ✅ 前端代码（React + Tailwind）
- ✅ 共享模块（schemas + utils）
- ✅ Mock HRV 数据文件（mock_hrv_data.csv）
- ✅ 数据结构和API文档
- ✅ 配置文件（requirements.txt, package.json等）
- ✅ README 和 SETUP 文档

## 注意事项

- 已配置 .gitignore，排除了：
  - venv/ (Python虚拟环境)
  - node_modules/ (Node.js依赖)
  - __pycache__/ (Python缓存)
  - .env (环境变量文件)

- Mock 数据文件（mock_hrv_data.csv）已包含在提交中 ✅

