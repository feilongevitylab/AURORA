# GitHub 推送指令

## 快速推送步骤

由于需要输入个人访问令牌，请在终端中手动执行以下命令：

### 步骤 1: 确保在正确的目录
```bash
cd /Users/jialianzhang/Desktop/aurora
```

### 步骤 2: 执行推送命令
```bash
git push -u origin main
```

### 步骤 3: 输入凭据

当提示时，输入：

**Username**: `feilongevitylab`

**Password**: [粘贴你的 GitHub 个人访问令牌]

> **注意**: 这里输入的是**个人访问令牌**，不是 GitHub 密码！

### 如何创建个人访问令牌

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 给令牌起个名字（如 "AURORA Project"）
4. 选择过期时间
5. 勾选权限：至少选择 `repo` 权限
6. 点击 "Generate token"
7. **立即复制令牌**（只显示一次）

---

## 替代方法：使用 SSH

如果你想避免每次输入令牌，可以使用 SSH：

### 配置 SSH（首次设置）

```bash
# 1. 生成 SSH 密钥（如果还没有）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 2. 查看公钥
cat ~/.ssh/id_ed25519.pub

# 3. 将公钥添加到 GitHub:
#    访问 https://github.com/settings/keys
#    点击 "New SSH key"，粘贴公钥

# 4. 更改远程仓库为 SSH 地址
cd /Users/jialianzhang/Desktop/aurora
git remote set-url origin git@github.com:feilongevitylab/AURORA.git

# 5. 推送
git push -u origin main
```

---

## 当前状态

✅ Git 仓库已初始化  
✅ 远程仓库已配置  
✅ 所有文件已提交（33个文件）  
✅ 包含 mock_hrv_data.csv  
⏳ 等待推送到 GitHub  

**提交信息**: 
- Commit 1: Initial commit: AURORA monorepo (32 files)
- Commit 2: Add Git push guide (1 file)

**总文件数**: 33 个文件  
**代码行数**: 11,535 行  

---

执行推送后，访问 https://github.com/feilongevitylab/AURORA 查看你的代码！

