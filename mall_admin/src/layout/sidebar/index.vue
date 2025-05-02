<template>
  <div class="sidebar-menu">
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
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import SidebarItem from './SidebarItem.vue'
import { constantRoutes } from '@/router'
import { useAppStore } from '@/store/modules/app'

const appStore = useAppStore()
const route = useRoute()

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
</style> 