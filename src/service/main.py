from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sniffer import Sniffer
import pprint
from model import *

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 标头
)
sniffer = Sniffer()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI JSON API"}

@app.get("/service/fetchInterfaces")
def fetchInterfaces():
    interfaces = sniffer.get_network_interfaces()
    return {"data": interfaces}

@app.post("/service/setInterface")
def setInterface(data: dict):
    if "interface_name" in data:
        ok = sniffer.set_network_interface(data["interface_name"])
        if ok:
            return {"data": {}, "msg": "网卡配置成功", "status": 200}
        else:
            return {"data": {}, "msg": "网卡配置失败: 网卡不存在", "status": 400}
    return {"data": {}, "msg": "网卡配置失败: 请求参数错误", "status": 400}
    
@app.post("/service/setFilterExperssion")
def setFilterExperssion(data: dict):
    if "filter_exp" in data:
        ok = sniffer.set_filter_expression(data["filter_exp"])
        if ok:
            return {"data": {}, "msg": "", "status": 200}
        else:
            return {"data": {}, "msg": "过滤表达式语法错误", "status": 400}
    return {"data": {}, "msg": "请求参数错误", "status": 400}

@app.get("/service/start_online_sniffing")
def startOnlineSniffing():
    ok = sniffer.start_online_sniffing()
    if not ok:
        return {"data": {}, "msg": "抓包失败", "status": 400}
    packets = sniffer.get_analyzed_packets()
    # print("[*]packets")
    # print(packets)
    return {"data": packets, "msg": "", "status": 200}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)