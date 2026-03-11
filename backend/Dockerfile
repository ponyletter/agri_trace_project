# 多阶段构建 - 编译阶段
FROM golang:1.22-alpine AS builder

WORKDIR /build
# 设置 Go 代理（国内加速）
ENV GOPROXY=https://goproxy.cn,direct
ENV CGO_ENABLED=0
ENV GOOS=linux
ENV GOARCH=amd64

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -ldflags="-s -w" -o agri-trace-server .

# 运行阶段
FROM alpine:3.19

WORKDIR /app
# 安装 ca-certificates（HTTPS 请求需要）
RUN apk --no-cache add ca-certificates tzdata && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone

COPY --from=builder /build/agri-trace-server .
COPY config/config.yaml config/config.yaml

EXPOSE 8080

CMD ["./agri-trace-server"]
