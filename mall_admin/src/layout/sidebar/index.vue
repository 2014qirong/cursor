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
        v-for="route in routes"
        :key="route.path"
        :item="route"
        :base-path="route.path"
      />
    </el-menu>
  </div>
</template>

<script setup>
import { computed } from 'vue'
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

// 过滤路由 - 只显示没有hidden标记的路由
const routes = computed(() => {
  return constantRoutes.filter(route => !route.hidden)
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