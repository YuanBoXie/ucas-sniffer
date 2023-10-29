<template>
  <div class="container">
    <!-- <div class="row">
      <a-input class="input" v-model="ruleInput" />
      <a-button type="primary" class="button">设置规则</a-button>
    </div> -->

    <div class="row">
      <a-select class="select" v-model="selected_interface">
        <a-select-option
          v-for="(option, index) in available_interfaces"
          :key="index"
          :value="option"
        >
          {{ option }}
        </a-select-option>
      </a-select>
      <a-button type="primary" class="button" @click="setInterface"
        >设置网卡</a-button
      >
    </div>

    <div class="row">
      <span class="slider-label">最大捕获数量:</span>
      <a-slider
        class="slider"
        v-model="maxCaptureCount"
        :min="0"
        :max="100"
        :default-value="10"
      />
    </div>

    <div class="row">
      <span class="slider-label">最大捕获时间:</span>
      <a-slider
        class="slider"
        v-model="maxCaptureTime"
        :min="0"
        :max="100"
        :default-value="10"
      />
    </div>

    <div class="row">
      <a-button
        type="primary"
        class="sniff-button"
        @click="startCapture"
        :disabled="isSniffing"
        >开始抓包</a-button
      >
    </div>
    <!-- <div class="row">
      <a-button
        type="primary"
        class="sniff-button"
        @click="pauseCapture"
        :disabled="!isSniffing"
        >暂停抓包</a-button
      >
    </div> -->

    <div class="row">
      <a-table
        class="table"
        :data-source="packets_data"
        :rowKey="(record) => record.time"
        :customRow="rowClick"
        :pagination="false"
      >
        <!-- 添加No列并使用插槽渲染计数 -->
        <a-table-column title="No." key="index" :customRender="renderNo" />
        <a-table-column title="Time" dataIndex="time" key="time" />
        <a-table-column title="Source" dataIndex="src" key="src" />
        <a-table-column title="Destination" dataIndex="dst" key="dst" />
        <a-table-column title="Protocol" dataIndex="protocol" key="protocol" />
        <a-table-column title="Length" dataIndex="length" key="length" />
        <a-table-column
          title="Info"
          dataIndex="summary"
          key="info"
          width="300"
          class="overflow-hidden"
        />
      </a-table>
    </div>

    <div class="row">
      <a-tree
        class="tree"
        :data="selected_packet_treedata"
      >
        <a-tree-node v-for="layer in selected_packet_treedata" :title="layer.label" :key="layer.label">
          <a-tree-node
            v-for="child in layer.list"
            :title="child"
            :key="child"
          />
        </a-tree-node>
      </a-tree>
    </div>

    <div class="row">
      <div class="hex-display">{{ selected_packet["raw"] }}</div>
    </div>
  </div>
</template>
  
<script>
export default {
  name: "index",
  data() {
    return {
      ruleInput: "",
      maxCaptureCount: 0,
      maxCaptureTime: 0,
      selected_interface: "",
      available_interfaces: [],
      isSniffing: false,
      packets_data: [],
      selected_packet: {},
      selected_packet_treedata: [], 
    };
  },
  created() {
    this.fetchInterfaces();
  },
  methods: {
    async fetchInterfaces() {
      let resp = await this.$http.get("/fetchInterfaces");
      this.available_interfaces = resp.data.data;
    },
    async setInterface() {
      if (this.selected_interface == "") return;
      let resp = await this.$http.post("/setInterface", {
        interface_name: this.selected_interface,
      });
      console.log(resp);
      if (resp.data.status == 200) {
        this.$message.success(resp.data.msg);
      } else {
        this.$message.error(resp.data.msg);
      }
    },
    async startCapture() {
      if (this.selected_interface == "") {
        this.$message.info("请先选择网卡");
        return;
      }
      let resp = await this.$http.get("/start_online_sniffing");
      let data = resp.data.data;
      console.log(data);
      this.isSniffing = false;
      this.packets_data = data;
    },
    async pauseCapture() {},
    renderNo(text, record, index) {
      return index;
    },
    parsePacketLayerData(layers) {
      let parsedLayers = []
      layers.forEach(layer => {
        let parsedLayer = {
          "label": layer["summary"],
          "list": []
        }
        Object.keys(layer).forEach(key => {
          if(key != "summary") { 
            parsedLayer["list"].push(`${key}: ${layer[key]}`)
          }
        })
        parsedLayers.push(parsedLayer)
      })
      return parsedLayers
    },
    rowClick(record, index) {
      return {
        on: {
          click: () => {
            this.selected_packet = record;
            this.selected_packet_treedata = this.parsePacketLayerData(record.layers)
            console.log(this.selected_packet_treedata)
          },
        },
      };
    },
  },
};
</script>
  
<style scoped lang="less">
.container {
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.row {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}
.tree {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.input {
  width: 80%;
  margin-right: 10px;
}

.select {
  width: 80%;
  margin-right: 10px;
}

.button {
  margin-right: 10px;
  width: 140px;
}

.slider-label {
  width: 140px;
  text-align: left;
}

.slider {
  width: 80%;
}

.sniff-button {
  width: 100%;
}

.table {
  width: 100%;
  max-height: 300px;
  overflow-y: scroll;
  overflow-x: scroll;
  &::-webkit-scrollbar {
    width: 4px;
  }
  &::-webkit-scrollbar-track {
    background-color: transparent;
    -webkit-border-radius: 2em;
    -moz-border-radius: 2em;
    border-radius: 2em;
  }
  &::-webkit-scrollbar-thumb {
    background-color: #ccc;
    -webkit-border-radius: 2em;
    -moz-border-radius: 2em;
    border-radius: 2em;
  }
}

.tree {
  width: 100%;
  max-height: 200px;
  padding: 20px;
  border: 1px solid #ccc;
  overflow-y: scroll;
  &::-webkit-scrollbar {
    width: 4px;
    height: 4px;
  }
  &::-webkit-scrollbar-track {
    background-color: transparent;
    -webkit-border-radius: 2em;
    -moz-border-radius: 2em;
    border-radius: 2em;
  }
  &::-webkit-scrollbar-thumb {
    background-color: #ccc;
    -webkit-border-radius: 2em;
    -moz-border-radius: 2em;
    border-radius: 2em;
  }
}

.hex-display {
  margin-top: 20px;
  padding: 20px;
  max-height: 140px;
  width: 100%;
  border: 1px solid #ccc;
  white-space: pre-wrap;
  text-align: left;
  overflow-y: scroll;
  &::-webkit-scrollbar {
    width: 4px;
    height: 4px;
  }
  &::-webkit-scrollbar-track {
    background-color: transparent;
    -webkit-border-radius: 2em;
    -moz-border-radius: 2em;
    border-radius: 2em;
  }
  &::-webkit-scrollbar-thumb {
    background-color: #ccc;
    -webkit-border-radius: 2em;
    -moz-border-radius: 2em;
    border-radius: 2em;
  }
}
.overflow-hidden {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>

<style>
.overflow-hidden td{
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>