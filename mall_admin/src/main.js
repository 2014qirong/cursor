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

// 打印环境信息和版本
console.log('当前环境:', import.meta.env)
console.log('Vue版本:', vueVersion)
console.log('启动应用...')
console.log('路由配置:', router.options.routes)

const app = createApp(App)

// 注册ElementPlus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 全局配置
app.config.errorHandler = (err, vm, info) => {
  console.error('Vue错误:', err)
  console.error('错误信息:', info)
  console.error('组件实例:', vm)
}

app.config.warnHandler = (msg, vm, trace) => {
  console.warn('Vue警告:', msg)
  console.warn('警告追踪:', trace)
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