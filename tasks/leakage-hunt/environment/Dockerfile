FROM python:3.10-slim

# 安装 pytest
RUN pip install pytest

WORKDIR /app

# 将本地的数据和脚本拷贝到容器内的标准路径
COPY data/ /app/data/
COPY scripts/ /app/scripts/

# 提示：实际运行过程中，Harbor 会动态挂载，但 COPY 保证了环境的完整性