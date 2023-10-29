# ucas-sniffer

> ucas-sniffer
> 代码存疑的地方如果有同学后面 review 我的代码可以帮忙解答一下疑惑，感激不尽~

# 依赖
- node v16.20.2
```bash
yarn add ant-design-vue
yarn add babel-plugin-import
yarn add less@3.9.0  --dev
yarn add less-loader@4.1.0 --dev
```

- <del>放弃基于 node-pcap 库抓包, 这个库已经 3 年没更新了，并且在 win 下容易出现奇怪错误，考虑用 python scapy 来抓包，然后通过 Node 调用 Python 服务。</del>