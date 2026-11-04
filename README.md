# KV Note

基于 **Cloudflare Workers + KV** 的轻量在线笔记 / 粘贴板服务，支持 Markdown、自定义密钥、过期时间与访问统计。

## 功能特性

- 在线编辑器，实时 Markdown 预览
- 自定义笔记 key，留空自动生成 8 位随机 ID
- 支持 TTL 过期时间（单位：秒）
- 自动统计访问次数
- `/list` 查看最近笔记
- `/admin` 密码管理后台（查看 / 删除）
- 自动识别 `.md` / `.html` / `.json` / 纯文本

## 部署步骤

1. 登录 Cloudflare，进入 **Workers & Pages → KV**，创建一个 KV 命名空间。
2. 新建一个 Worker，粘贴本项目代码。
3. Worker 设置 → **KV 命名空间绑定**：
   - 变量名称：`NOTE`
   - 选择刚创建的 KV 命名空间。
4. （推荐）在 Worker 环境变量中配置，覆盖代码内默认值：

   | 变量名 | 说明 |
   |--------|------|
   | `API_TOKEN` | 写入接口令牌 |
   | `ADMIN_PASS` | 管理后台密码 |

   > 默认值为 `changeme`，上线前务必修改。

## 路由说明

| 路径 | 用途 |
|------|------|
| `/` | 编辑器主页 |
| `/list` | 最近笔记列表 |
| `/admin?pass=密码` | 管理后台 |
| `/delete?pass=密码&key=xxx` | 删除笔记 |
| `/set?token=令牌` | API 写入（POST） |
| `/{key}` | 读取笔记 |

## API 写入示例

```http
POST /set?token=你的API_TOKEN
Content-Type: application/json
```

```json
{
  "key": "test",
  "value": "# Hello\nMarkdown 内容",
  "ttl": 3600
}
```

- `key`：可选，留空自动随机生成
- `value`：必填
- `ttl`：可选，单位秒，`0` 表示永久

成功返回：

```json
{
  "success": true,
  "key": "test",
  "url": "/test"
}
```

## 内容识别规则

访问 `/{key}` 时：

1. key 以 `.md` 结尾 / 内容以 `#` 开头 / 含代码块 → Markdown 渲染页（带目录、浏览量）
2. `.html` → 原样输出 HTML
3. `.json` → 返回 JSON
4. 其他 → 纯文本
5. 每访问一次，浏览计数 +1

## 注意事项

- 过期为**代码懒清理**：访问笔记或进入后台时才检查删除，无定时任务。
- KV 本身不支持 TTL，过期时间保存在 metadata 中。
- 笔记明文存储，**不加密**，请勿存放敏感数据。
- 存在已知安全短板（XSS、GET 删除、URL 携带密钥），仅适合个人自用，勿公网开放。

## License

MIT，仅供学习自用。
