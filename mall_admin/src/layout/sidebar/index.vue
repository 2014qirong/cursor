<template>
  <div class="sidebar-menu">
    <!-- 调试信息显示 -->
    <div v-if="isDebug" class="debug-panel">
      <h4>菜单调试信息</h4>
      <div class="debug-count">路由数量: {{ routes.length }}</div>
      <div v-for="(route, index) in routes" :key="index" class="debug-item">
        - {{ route.path }} ({{ route.meta?.title || '无标题' }})
      </div>
    </div>
    
    <el-menu
      :default-active="activeMenu"
      :collapse="isCollapse"
      :unique-opened="true"
      :collapse-transition="false"
      background-color="#304156"
      text-color="#bfcbd9"
      active-text-color="#409EFF"
      mode="vertical"
    >
      <sidebar-item
        v-for="route in filteredRoutes"
        :key="route.path"
        :item="route"
        :base-path="route.path"
      />
    </el-menu>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import SidebarItem from './SidebarItem.vue'
import { constantRoutes } from '@/router'
import { useAppStore } from '@/store/modules/app'

const appStore = useAppStore()
const route = useRoute()
const router = useRouter()
const isDebug = ref(true) // 控制是否显示调试信息

// 从布局组件传入的isCollapse状态
const isCollapse = computed(() => !appStore.sidebar.opened)

// 当前激活的菜单
const activeMenu = computed(() => {
  const { meta, path } = route
  if (meta.activeMenu) {
    return meta.activeMenu
  }
  return path
})

// 所有路由
const routes = computed(() => {
  return constantRoutes.filter(route => !route.hidden)
})

// 过滤后的路由 - 确保包含需要的字段
const filteredRoutes = computed(() => {
  return routes.value.map(route => {
    // 确保每个路由对象都有正确的结构
    return {
      ...route,
      meta: route.meta || { title: route.name || '未命名' },
      children: route.children || []
    }
  })
})

onMounted(() => {
  console.log('侧边栏路由:', routes.value)
  console.log('路由器已注册路由:', router.getRoutes())
})
</script>

<style lang="scss" scoped>
.sidebar-menu {
  border-right: none;
  
  :deep(.el-menu) {
    border-right: none;
  }
  
  :deep(.el-menu--collapse) {
    width: 54px;
  }
}

.debug-panel {
  padding: 10px;
  background: rgba(0, 0, 0, 0.2);
  color: #eee;
  font-size: 12px;
  
  h4 {
    margin-bottom: 5px;
    color: #fff;
  }
  
  .debug-count {
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  .debug-item {
    padding: 2px 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}
</style> 