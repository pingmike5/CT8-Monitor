# 📡 CT8 放号监控机器人

本项目是一个用于监控 [CT8](https://www.ct8.biz) 放号情况的 Telegram 机器人，自动检查并在放号时通知用户。目前已部署并运行在 Telegram 频道：

👉 [@ct8jiankoog](https://t.me/ct8jiankoog)

> ⚠️ 若频道失效，可参考本项目 **自行搭建机器人服务**。

---

## 🚀 部署说明

本项目适配于多数容器平台，已在 [Render.com](https://render.com) 上成功运行。你也可以部署到：

- Railway
- Fly.io
- Docker 本地
- Koyeb、Zeabur 等平台

---

## 🛠️ 环境变量配置

| 变量名 | 描述 |
|--------|------|
| `TELEGRAM_BOT_TOKEN` | Telegram 机器人 Token，来自 [@BotFather](https://t.me/BotFather) |
| `TELEGRAM_CHAT_ID`   | 用户或频道的 ID（可通过 [@userinfobot](https://t.me/userinfobot) 获取） |
| `CHECK_INTERVAL`     | （可选）检查间隔时间（单位：秒），默认值为 `60` |

---

## 🐳 Docker 镜像

你可以直接拉取并运行预构建镜像：

```bash
docker run -d \
  -e TELEGRAM_BOT_TOKEN=xxx \
  -e TELEGRAM_CHAT_ID=123456 \
  -e CHECK_INTERVAL=60 \
  pingmike/ct8-watcher:latest
