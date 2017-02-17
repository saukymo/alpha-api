FROM registry.cn-hangzhou.aliyuncs.com/acs/python
WORKDIR /app
COPY . /app
RUN pip install -r requirement.txt

EXPOSE 7000
CMD python app.py
