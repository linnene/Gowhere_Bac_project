# GoWhere 后端项目 API 接口文档

## 基础信息

- **项目名称**: GoWhere Backend
- **API 版本**: v1.0
- **基础 URL**: `http://localhost:8000/v1` (开发环境)
- **技术栈**: FastAPI + SQLAlchemy + Redis

## 目录

1. [用户注册模块 (Signup)](#用户注册模块-signup)
2. [用户登录模块 (Login)](#用户登录模块-login)
3. [邮箱验证模块 (Email)](#邮箱验证模块-email)
4. [AI聊天模块 (AI)](#ai聊天模块-ai)

---

## 用户注册模块 (Signup)

### 1. 创建用户

**接口描述**: 创建新用户账户

- **请求方式**: `POST`
- **接口路径**: `/v1/Signup/creat_user`
- **接口说明**: 通过用户信息创建新用户，检查用户是否已注册和密码有效性

#### 请求参数 (Body)

```json
{
  "UserEmail": "string",
  "UserPassword": "string",
  "UserName": "string",
  "UserPhone": "string"
}
```

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| UserEmail | string | 是 | 用户邮箱地址 |
| UserPassword | string | 是 | 用户密码（不能为空或"string"） |
| UserName | string | 是 | 用户姓名 |
| UserPhone | string | 否 | 用户电话号码 |

#### 响应格式

**成功响应 (200)**
```json
{
  "UserId": "string",
  "UserEmail": "string",
  "UserName": "string",
  "UserPhone": "string",
  "EmailVerified": false,
  "CreatedAt": "2024-01-01T12:00:00Z"
}
```

**错误响应**
```json
{
  "message": "password can't be None"
}
```

### 2. 获取用户信息

**接口描述**: 根据用户ID或Token获取用户信息

- **请求方式**: `GET`
- **接口路径**: `/v1/Signup/get_user`

#### 请求参数 (Query)

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| user_id | string | 否 | 用户唯一标识符 |
| Tokens | string | 否 | 用户访问令牌 |

**注意**: user_id 和 Tokens 至少提供一个

#### 响应格式

**成功响应 (200)**
```json
{
  "UserId": "string",
  "UserEmail": "string",
  "UserName": "string",
  "UserPhone": "string",
  "EmailVerified": true,
  "CreatedAt": "2024-01-01T12:00:00Z"
}
```

---

## 用户登录模块 (Login)

### 1. 用户登录

**接口描述**: 用户登录验证，返回访问令牌

- **请求方式**: `POST`
- **接口路径**: `/v1/Login/Login_user`

#### 请求参数

| 参数名 | 类型 | 必填 | 位置 | 说明 |
|--------|------|------|------|------|
| userpassword | string | 是 | Form Data | 用户密码 |
| userid | string | 是 | Query | 用户ID |

#### 请求示例

```http
POST /v1/Login/Login_user?userid=12345
Content-Type: application/x-www-form-urlencoded

userpassword=your_password
```

#### 响应格式

**成功响应 (200)**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**错误响应**
```json
{
  "detail": "需要ID"
}
```

### 2. 更新用户信息

**接口描述**: 更新用户信息

- **请求方式**: `PUT`
- **接口路径**: `/v1/Login/update_user`

#### 请求参数

| 参数名 | 类型 | 必填 | 位置 | 说明 |
|--------|------|------|------|------|
| user_id | string | 是 | Query | 用户ID |
| new_user | object | 是 | Body | 更新的用户信息 |

#### 请求示例

```json
{
  "UserName": "新用户名",
  "UserPhone": "新电话号码",
  "UserEmail": "new@email.com"
}
```

---

## 邮箱验证模块 (Email)

### 1. 发送验证邮件

**接口描述**: 向指定邮箱发送验证码邮件

- **请求方式**: `POST`
- **接口路径**: `/v1/email/send_template_email`

#### 请求参数 (Body)

```json
{
  "email": "user@example.com",
  "subject": "邮箱验证",
  "template": "verification"
}
```

#### 响应格式

**成功响应 (200)**
```json
{
  "message": "email has been sent"
}
```

### 2. 验证邮箱验证码

**接口描述**: 验证用户输入的邮箱验证码

- **请求方式**: `POST`
- **接口路径**: `/v1/email/verify_code`

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| code | string | 是 | 6位验证码 |
| email | string | 是 | 邮箱地址 |

#### 响应格式

**成功响应 (200)**
```json
{
  "message": "Verification successful"
}
```

**失败响应 (400)**
```json
{
  "message": "Invalid verification code"
}
```

---

## AI聊天模块 (AI)

### 1. 聊天接口

**接口描述**: 与AI进行对话聊天

- **请求方式**: `GET`
- **接口路径**: `/v1/AI/chat`

#### 请求参数 (Query)

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| user_id | string | 是 | 用户唯一标识符 |
| message | string | 是 | 发送给AI的消息内容 |

#### 请求示例

```http
GET /v1/AI/chat?user_id=12345&message=你好，今天天气怎么样？
```

#### 响应格式

**成功响应 (200)**
```json
{
  "response": "AI回复的消息内容",
  "timestamp": "2024-01-01T12:00:00Z",
  "user_id": "12345"
}
```

**错误响应 (500)**
```json
{
  "detail": "错误详细信息"
}
```

### 2. 聊天历史接口

**接口描述**: 获取用户的聊天历史记录

- **请求方式**: `GET`
- **接口路径**: `/v1/AI/chat_history`

#### 请求参数 (Query)

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| user_id | string | 是 | 用户唯一标识符 |

#### 请求示例

```http
GET /v1/AI/chat_history?user_id=12345
```

#### 响应格式

**成功响应 (200)**
```json
{
  "user_id": "12345",
  "chat_history": [
    {
      "id": 1,
      "message": "用户消息内容",
      "response": "AI回复内容",
      "timestamp": "2024-01-01T12:00:00Z"
    },
    {
      "id": 2,
      "message": "另一条用户消息",
      "response": "另一条AI回复",
      "timestamp": "2024-01-01T12:05:00Z"
    }
  ]
}
```

---

## 通用错误码

| 错误码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 401 | 未授权访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 数据模型

### UserCreate
```json
{
  "UserEmail": "string",
  "UserPassword": "string", 
  "UserName": "string",
  "UserPhone": "string"
}
```

### UserRead
```json
{
  "UserId": "string",
  "UserEmail": "string",
  "UserName": "string", 
  "UserPhone": "string",
  "EmailVerified": "boolean",
  "CreatedAt": "datetime"
}
```

### UserUpdate
```json
{
  "UserName": "string",
  "UserPhone": "string",
  "UserEmail": "string"
}
```

### EmailSchema
```json
{
  "email": "string",
  "subject": "string",
  "template": "string"
}
```

## 开发环境配置

### 启动服务
```bash
# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 环境依赖
- Python 3.8+
- FastAPI
- SQLAlchemy (异步)
- Redis
- SMTP 邮件服务

## 注意事项

1. **认证安全**: 登录接口返回JWT token，需要妥善保存
2. **邮箱验证**: 注册后需要进行邮箱验证才能完全激活账户
3. **密码安全**: 密码在数据库中已加密存储
4. **异步处理**: 所有数据库操作都是异步的
5. **Redis缓存**: 验证码存储在Redis中，有过期时间
6. **错误处理**: 所有接口都包含完整的异常处理机制

## 测试状态

- ✅ 用户注册功能 (测试完成 - 2025/3/8)
- ✅ 用户登录功能 (测试完成 - 2025/3/8) 
- ✅ 邮箱验证功能 (测试完成 - 2025/3/8)
- ⚠️ 邮件发送功能 (存在SMTP配置问题)
- 🔄 AI聊天功能 (开发中)
- 🔄 用户信息更新 (存在查找用户bug)

## 已知问题

1. **邮件发送**: SMTP配置问题，建议更换为Hotmail SMTP
2. **用户更新**: 更新用户信息时可能无法找到用户
3. **安全验证**: get_user接口需要增加权限验证
