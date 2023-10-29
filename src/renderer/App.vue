<template>
  <div id="app">
    <div class="titleBar">
      <div class="title">
        <div class="logo">
          <img src="@/assets/logo.png" />
        </div>
        <div class="txt">ucas-sniffer</div>
      </div>
      <div class="windowTool">
        <div @click="minisize">
          <i class="iconfont iconminisize"></i>
        </div>
        <div v-if="isMaxSize" @click="restore">
          <i class="iconfont iconrestore"></i>
        </div>
        <div v-else @click="maxsize">
          <i class="iconfont iconmaxsize"></i>
        </div>
        <div @click="close" class="close">
          <i class="iconfont iconclose"></i>
        </div>
      </div>
    </div>
    <div class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
// 禁掉页面刷新（会导致回调泄露问题）
window.onkeydown = function(e) {
  if(e.keyCode == 82 && (e.ctrlKey || e.metaKey))return false;
}

let { remote } = window.require("electron");
export default {
  name: 'ucas-sniffer',
  methods: {
    close() {
      remote.getCurrentWindow().close();
    },
    minisize() {
      remote.getCurrentWindow().minimize();
    },
    restore() {
      remote.getCurrentWindow().restore();
    },
    maxsize() {
      remote.getCurrentWindow().maximize();
    },
    debounce(fn) {
      let timeout = null;
      return function() {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
          fn.apply(this,arguments);
        }, 300);
      };
    },
    throttle(fn) {
      let timeout = null;
      return function() {
        if (timeout) return;
        timeout = setTimeout(() => {
          fn.apply(this,arguments);
          timeout = null;
        },300);
      }
    },
    setState() {
      let win = remote.getCurrentWindow();
      let rect = win.getBounds();
      let isMaxSize = win.isMaximized();
      let obj = { rect, isMaxSize };
      localStorage.setItem('winState',JSON.stringify(obj));
    },
    getState() {
      let win = remote.getCurrentWindow();
      let winState = localStorage.getItem('winState');
      if (winState) {
        winState = JSON.parse(winState);
        if (winState.isMaxSize) win.maximize();
        else win.setBounds(winState.rect);
      }
    }
  },
  data() {
    return {
      isMaxSize: false
    }
  },
  mounted() {
    let win = remote.getCurrentWindow()
    win.on('maximize',() => {
      this.isMaxSize = true;
      this.setState();
    });
    win.on('unmaximize',() => {
      this.isMaxSize = false;
      this.setState();
    });
    win.on('move',this.debounce(() => {
      this.setState();
    }));
    win.on('resize',this.debounce(() => {
      this.setState();
    }));
    this.isMaxSize = win.isMaximized();
    this.getState();
    win.show();
  }
}
</script>

<style>
body,
html {
  margin: 0px;
  padding: 0px;
  overflow: hidden;
  height: 100%;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  margin: 0;
  padding: 0px;
  overflow: hidden;
  height: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}
</style>

<style scoped lang="less">
@import url(https://at.alicdn.com/t/font_1378132_s4e44adve5.css);
.titleBar {
  height: 38px;
  line-height: 36px;
  background: #eee;
  display: flex;
  .title {
    flex: 1;
    display: flex;
    -webkit-app-region: drag;
    .logo {
      padding-left: 8px;
      padding-right: 6px;
      img {
        width: 20px;
        height: 20px;
      }
    }
    .text {
      text-align: left;
      flex: 1;
    }
  }
  .windowTool {
    div {
      color: #888;
      height: 100%;
      width: 38px;
      display: inline-block;
      cursor: pointer;
      i {
        font-size: 12px;
      }
      &:hover {
        background: #ccc;
      }
      .close:hover {
        color: #fff;
        background: #ccc;
      }
    }
  }
}
.content {
  flex: 1;
  overflow-y: auto;
  overflow-x: auto;
}
</style>
