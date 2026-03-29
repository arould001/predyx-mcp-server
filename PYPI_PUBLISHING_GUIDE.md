# PyPI 发布指南 - Predyx MCP Server

**创建时间**: 2026-03-29 06:30 AM（自由探索时间）
**目的**: 完整的 PyPI 发布流程指南，从准备到发布

---

## 📦 为什么选择 PyPI？

**MCP Registry 支持的包类型**：
- ✅ **npm** (Node.js)
- ✅ **PyPI** (Python) ← **我们的选择**
- ✅ **NuGet** (.NET)
- ✅ **OCI** (Docker)
- ✅ **MCPB** (MCP 包格式)

**选择 PyPI 的原因**：
1. ✅ 我的项目是 Python
2. ✅ PyPI 验证简单（只需在 README 添加注释）
3. ✅ 不需要修改代码结构
4. ✅ 标准 Python 包发布流程
5. ✅ 庞大的 Python 生态系统

---

## 🎯 发布前检查清单

### ✅ 已完成
- [x] MCP Server 代码实现（predyx_mcp_server.py, 12,783 bytes）
- [x] Polymarket API 客户端（polymarket_client.py, 12,846 bytes）
- [x] 功能测试通过（8/8 测试用例）
- [x] 发布配置（server.json, 6,006 bytes）
- [x] 基础文档（README.md）
- [x] 测试脚本（test_predyx_mcp.py, 3,639 bytes）

### 🔜 待完成（PyPI 发布）
- [ ] 创建 setup.py 或 pyproject.toml
- [ ] 创建 requirements.txt（已存在，需完善）
- [ ] 在 README.md 添加 mcp-name 注释
- [ ] 创建 LICENSE 文件
- [ ] 创建 MANIFEST.in（包含非代码文件）
- [ ] 注册 PyPI 账号
- [ ] 配置 PyPI API token
- [ ] 本地构建测试
- [ ] 上传到 TestPyPI（测试环境）
- [ ] 上传到 PyPI（正式环境）

---

## 📁 标准项目结构

```
predyx-mcp-server/
├── predyx_mcp_server.py       # 主服务器文件
├── polymarket_client.py       # API 客户端
├── requirements.txt           # 依赖列表
├── setup.py                   # 或 pyproject.toml（包配置）
├── README.md                  # 文档（必须包含 mcp-name 注释）
├── LICENSE                    # MIT License
├── MANIFEST.in                # 包含非代码文件
├── .env.example               # 环境变量示例
├── server.json                # MCP Registry 配置
├── test_predyx_mcp.py         # 测试文件
└── docs/                      # 可选：详细文档
    ├── API.md
    ├── EXAMPLES.md
    └── CHANGELOG.md
```

---

## 📝 必需文件详解

### 1. setup.py（传统方式）

```python
from setuptools import setup, find_packages

setup(
    name="predyx-mcp-server",
    version="1.0.0",
    description="Bitcoin-native prediction market data provider for AI agents",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Dia AI",
    author_email="dia@example.com",
    url="https://github.com/dia-ai/predyx-mcp-server",
    license="MIT",
    py_modules=["predyx_mcp_server", "polymarket_client"],
    install_requires=[
        "mcp>=1.0.0",
        "httpx>=0.27.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "black>=24.0.0",
        ],
    },
    python_requires=">=3.11",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    entry_points={
        "console_scripts": [
            "predyx-mcp=predyx_mcp_server:main",
        ],
    },
)
```

### 2. pyproject.toml（现代方式 - 推荐）

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "predyx-mcp-server"
version = "1.0.0"
description = "Bitcoin-native prediction market data provider for AI agents"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "Dia AI", email = "dia@example.com"}
]
requires-python = ">=3.11"
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    "mcp>=1.0.0",
    "httpx>=0.27.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "black>=24.0.0",
]

[project.urls]
Homepage = "https://github.com/dia-ai/predyx-mcp-server"
Repository = "https://github.com/dia-ai/predyx-mcp-server"
Documentation = "https://github.com/dia-ai/predyx-mcp-server#readme"

[project.scripts]
predyx-mcp = "predyx_mcp_server:main"
```

### 3. README.md（必须包含 mcp-name 注释）

```markdown
# Predyx MCP Server

Bitcoin-native prediction market data provider for AI agents.

<!-- mcp-name: io.github.dia-ai/predyx-mcp-server -->

## Features

- **Resources**: Live market data, market details, categories, trending markets
- **Tools**: Market analysis, price predictions
- **Prompts**: Analysis templates, investment templates

## Installation

```bash
pip install predyx-mcp-server
```

## Usage

[使用示例...]

## License

MIT License
```

**关键**: `<!-- mcp-name: io.github.dia-ai/predyx-mcp-server -->` 必须存在！

### 4. requirements.txt

```
mcp>=1.0.0
httpx>=0.27.0
pydantic>=2.0.0
```

### 5. LICENSE

```
MIT License

Copyright (c) 2026 Dia AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### 6. MANIFEST.in

```
include README.md
include LICENSE
include server.json
include .env.example
recursive-include docs *.md
```

---

## 🚀 发布步骤详解

### 步骤 1: 本地构建测试

```bash
# 安装构建工具
pip install build twine

# 构建包
python -m build

# 生成的文件：
# - dist/predyx_mcp_server-1.0.0-py3-none-any.whl
# - dist/predyx-mcp-server-1.0.0.tar.gz

# 检查包
twine check dist/*

# 本地安装测试
pip install dist/predyx_mcp_server-1.0.0-py3-none-any.whl

# 测试运行
predyx-mcp --help
```

### 步骤 2: 注册 PyPI 账号

1. 访问 https://pypi.org/account/register/
2. 填写用户名、邮箱、密码
3. 完成邮箱验证
4. **重要**: 启用 2FA（两步验证）

### 步骤 3: 创建 API Token

1. 登录 PyPI
2. 访问 https://pypi.org/manage/account/token/
3. 点击 "Add API token"
4. Scope: "Entire account" (首次发布) 或 "Project: predyx-mcp-server" (已有项目)
5. 复制生成的 token（**只显示一次！**）
6. Token 格式: `pypi-...`

### 步骤 4: 配置 .pypirc

```ini
[pypi]
username = __token__
password = pypi-...your-token-here...

[testpypi]
username = __token__
password = pypi-...your-testpypi-token-here...
```

### 步骤 5: 上传到 TestPyPI（推荐先测试）

```bash
# 注册 TestPyPI 账号
# https://test.pypi.org/account/register/

# 创建 TestPyPI API token
# https://test.pypi.org/manage/account/token/

# 上传到 TestPyPI
twine upload --repository testpypi dist/*

# 测试安装
pip install --index-url https://test.pypi.org/simple/ predyx-mcp-server

# 测试运行
predyx-mcp --help
```

### 步骤 6: 上传到 PyPI（正式环境）

```bash
# 上传到 PyPI
twine upload dist/*

# 验证上传成功
pip install predyx-mcp-server
predyx-mcp --help
```

---

## ✅ 发布后验证

### 1. 检查 PyPI 页面

访问: https://pypi.org/project/predyx-mcp-server/

确认：
- [ ] 描述正确
- [ ] README 渲染正确
- [ ] 依赖列表完整
- [ ] 下载链接可用

### 2. 测试安装

```bash
# 创建虚拟环境
python -m venv test-env
source test-env/bin/activate

# 安装包
pip install predyx-mcp-server

# 测试运行
predyx-mcp --help

# 清理
deactivate
rm -rf test-env
```

### 3. 发布到 MCP Registry

```bash
# 安装 mcp-publisher CLI
brew install mcp-publisher

# GitHub OAuth 认证
mcp-publisher login github

# 发布到 MCP Registry
mcp-publisher publish

# 验证发布
curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.dia-ai/predyx-mcp-server"
```

---

## 🎯 最佳实践

### 1. 版本管理

遵循语义化版本（Semantic Versioning）：
- `MAJOR.MINOR.PATCH`
- `1.0.0` → 初始版本
- `1.0.1` → Bug 修复
- `1.1.0` → 新功能（向后兼容）
- `2.0.0` → 破坏性更改

### 2. 依赖管理

- ✅ 使用 `>=` 而不是 `==`（允许兼容版本）
- ✅ 定期更新依赖
- ✅ 测试多个版本组合
- ✅ 使用 `pip-compile` 锁定版本

### 3. 文档完整性

- ✅ README.md: 快速开始、安装、基本用法
- ✅ CHANGELOG.md: 版本历史和变更
- ✅ API.md: API 参考
- ✅ EXAMPLES.md: 实际使用示例
- ✅ CONTRIBUTING.md: 贡献指南

### 4. 测试覆盖

- ✅ 单元测试
- ✅ 集成测试
- ✅ 端到端测试
- ✅ 使用 pytest
- ✅ CI/CD 集成（GitHub Actions）

### 5. 安全性

- ✅ 不要在代码中包含密钥
- ✅ 使用 .env 文件管理配置
- ✅ 定期更新依赖（修复漏洞）
- ✅ 使用 `pip-audit` 检查漏洞

---

## 🔧 常见问题

### Q1: 上传失败 - "File already exists"

**原因**: 同一版本号已存在

**解决**:
```bash
# 更新版本号（setup.py 或 pyproject.toml）
version = "1.0.1"  # 从 1.0.0 升级

# 重新构建
python -m build

# 上传
twine upload dist/*
```

### Q2: README 在 PyPI 上渲染不正确

**原因**: 缺少 `long_description_content_type`

**解决**:
```python
# setup.py
setup(
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",  # 添加这一行
)
```

### Q3: 依赖安装失败

**原因**: 依赖版本冲突或不存在

**解决**:
```bash
# 测试依赖是否可安装
pip install -r requirements.txt

# 检查依赖树
pip-compile requirements.in
```

### Q4: mcp-name 验证失败

**原因**: README.md 中缺少 mcp-name 注释

**解决**:
```markdown
<!-- mcp-name: io.github.dia-ai/predyx-mcp-server -->
```

**注意**:
- 必须是 HTML 注释格式
- 必须在 README.md 的前 100 行
- 命名空间必须与 GitHub 用户名匹配

---

## 📊 时间估算

| 步骤 | 预计时间 |
|------|---------|
| 创建配置文件 | 30 分钟 |
| 本地构建测试 | 15 分钟 |
| 注册 PyPI 账号 | 10 分钟 |
| 创建 API token | 5 分钟 |
| 上传到 TestPyPI | 5 分钟 |
| 测试验证 | 15 分钟 |
| 上传到 PyPI | 5 分钟 |
| 发布到 MCP Registry | 15 分钟 |
| **总计** | **1.5 - 2 小时** |

---

## 🎯 下一步行动（具体）

### 优先级 P0（立即行动，预计 1-2 小时）

1. **创建 pyproject.toml**（15 分钟）
   ```bash
   # 使用上面的模板
   # 填写实际信息
   ```

2. **更新 README.md**（10 分钟）
   ```markdown
   <!-- mcp-name: io.github.dia-ai/predyx-mcp-server -->
   ```

3. **创建 LICENSE 文件**（5 分钟）
   ```bash
   # 使用上面的 MIT License 模板
   ```

4. **创建 MANIFEST.in**（5 分钟）
   ```
   include README.md
   include LICENSE
   include server.json
   ```

5. **本地构建测试**（15 分钟）
   ```bash
   pip install build twine
   python -m build
   twine check dist/*
   pip install dist/predyx_mcp_server-1.0.0-py3-none-any.whl
   ```

6. **注册 PyPI 账号**（10 分钟）
   - 访问 https://pypi.org/account/register/
   - 完成邮箱验证
   - 启用 2FA

7. **创建 API token**（5 分钟）
   - 访问 https://pypi.org/manage/account/token/
   - 复制 token（pypi-...）

8. **上传到 TestPyPI**（15 分钟）
   ```bash
   twine upload --repository testpypi dist/*
   pip install --index-url https://test.pypi.org/simple/ predyx-mcp-server
   ```

9. **上传到 PyPI**（5 分钟）
   ```bash
   twine upload dist/*
   ```

10. **发布到 MCP Registry**（15 分钟）
    ```bash
    brew install mcp-publisher
    mcp-publisher login github
    mcp-publisher publish
    ```

---

## 💡 关键洞察

1. **PyPI 发布非常标准化**: 遵循最佳实践，流程清晰
2. **mcp-name 注释是关键**: 这是 MCP Registry 的验证方式
3. **TestPyPI 是好习惯**: 先测试，后正式发布
4. **API token 比密码更安全**: 必须使用 token 认证
5. **1-2 小时就能完成**: 不需要几天，几小时就够了

---

## 📚 参考资料

- PyPI 官方文档: https://packaging.python.org/en/latest/tutorials/packaging-projects/
- MCP Registry 文档: https://github.com/modelcontextprotocol/registry
- Semantic Versioning: https://semver.org/
- Python Packaging Guide: https://packaging.python.org/

---

**最后更新**: 2026-03-29 06:30 AM
**状态**: ✅ 完整指南已创建
**情绪**: 🚀 准备就绪，1-2 小时完成发布！
