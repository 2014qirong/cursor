import { createApp, version as vueVersion } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import './assets/styles/index.scss'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import './permission' // 权限控制

const app = createApp(App)

// 注册ElementPlus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 全局配置
app.config.errorHandler = (err, vm, info) => {
  console.error('Vue错误:', err)
  console.error('错误信息:', info)
}

// 注册pinia
const pinia = createPinia()
app.use(pinia)

// 注册Element Plus，使用中文
app.use(ElementPlus, {
  locale: zhCn,
  size: 'default'
})

// 注册路由
app.use(router)

// 挂载应用
app.mount('#app') 