import Vue from 'vue'
import axios from 'axios'

// import Antd from 
import 'ant-design-vue/dist/antd.css' 

import App from './App'
import router from './router'
import store from './store'


if (!process.env.IS_WEB) Vue.use(require('vue-electron'))
Vue.use(require('ant-design-vue')) // 不太清楚为什么 import 不行，但 require 就可以


const request = axios.create({
  baseURL: 'http://127.0.0.1:8000/service',
  timeout: 5000
})

Vue.http = Vue.prototype.$http = request
Vue.config.productionTip = false


/* eslint-disable no-new */
new Vue({
  components: { App },
  router,
  store,
  template: '<App/>'
}).$mount('#app')
