<template>
  <div class="app-wrapper">
    <!-- 侧边栏 -->
    <div class="sidebar-container" :class="{ 'hide-sidebar': isCollapse }">
      <div class="logo-container">
        <img src="@/assets/images/logo.png" alt="logo" class="logo-img">
        <h1 class="logo-title" v-if="!isCollapse">商城管理系统</h1>
      </div>
      <el-scrollbar>
        <sidebar />
      </el-scrollbar>
    </div>
    
    <!-- 主要内容区域 -->
    <div class="main-container">
      <!-- 顶部导航栏 -->
      <div class="navbar">
        <div class="hamburger-container" @click="toggleSideBar">
          <el-icon :size="20">
            <component :is="isCollapse ? 'Expand' : 'Fold'" />
          </el-icon>
        </div>
        <breadcrumb />
        <div class="right-menu">
          <el-dropdown trigger="click" class="avatar-container">
            <div class="avatar-wrapper">
              <el-avatar icon="UserFilled" />
              <span class="user-name">管理员</span>
              <el-icon><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>个人信息</el-dropdown-item>
                <el-dropdown-item>修改密码</el-dropdown-item>
                <el-dropdown-item divided @click="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
      
      <!-- 主要内容 -->
      <div class="app-main">
        <router-view v-slot="{ Component }">
          <transition name="fade-transform" mode="out-in">
            <keep-alive>
              <component :is="Component" />
            </keep-alive>
          </transition>
        </router-view>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import Sidebar from './sidebar/index.vue'
import Breadcrumb from './components/Breadcrumb.vue'
import { removeToken } from '@/utils/auth'
import { useAppStore } from '@/store/modules/app'
import { useUserStore } from '@/store/modules/user'
import { constantRoutes } from '@/router'

const router = useRouter()
const appStore = useAppStore()
const userStore = useUserStore()
const isDebug = ref(false) // 设置为false以隐藏调试信息
const allRoutes = ref([])

// 侧边栏收起状态
const isCollapse = computed(() => !appStore.sidebar.opened)

onMounted(() => {
  // 获取所有路由信息用于调试 - 仅在开发环境需要
  if (isDebug.value) {
    allRoutes.value = router.getRoutes().map(route => ({
      path: route.path,
      name: route.name,
      meta: route.meta,
      children: route.children?.map(child => ({
        path: child.path,
        name: child.name,
        meta: child.meta
      }))
    }))
  }
})

// 切换侧边栏展开/收起
const toggleSideBar = () => {
  appStore.toggleSidebar()
}

// 退出登录
const logout = () => {
  ElMessageBox.confirm('确定要退出登录吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    userStore.logout().then(() => {
      router.push('/login')
    })
  }).catch(() => {})
}
</script>

<style lang="scss" scoped>
.app-wrapper {
  position: relative;
  height: 100%;
  width: 100%;
  display: flex;
}

.sidebar-container {
  transition: width 0.28s;
  width: 210px;
  height: 100%;
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  background-color: #304156;
  z-index: 1001;
  
  &.hide-sidebar {
    width: 54px;
  }
  
  .logo-container {
    height: 50px;
    line-height: 50px;
    display: flex;
    align-items: center;
    padding-left: 15px;
    background: #2b2f3a;
    overflow: hidden;
    
    .logo-img {
      width: 32px;
      height: 32px;
      margin-right: 10px;
    }
    
    .logo-title {
      color: #fff;
      font-size: 16px;
      font-weight: bold;
      margin: 0;
      white-space: nowrap;
    }
  }
}

.main-container {
  min-height: 100%;
  transition: margin-left 0.28s;
  margin-left: 210px;
  position: relative;
  width: calc(100% - 210px);
  
  .sidebar-container.hide-sidebar + & {
    margin-left: 54px;
    width: calc(100% - 54px);
  }
}

.navbar {
  height: 50px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #e6e6e6;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  background-color: #fff;
  
  .hamburger-container {
    line-height: 46px;
    height: 100%;
    padding: 0 15px;
    cursor: pointer;
  }
  
  .right-menu {
    margin-left: auto;
    padding-right: 15px;
    
    .avatar-container {
      .avatar-wrapper {
        display: flex;
        align-items: center;
        cursor: pointer;
        
        .user-name {
          margin: 0 5px;
        }
      }
    }
  }
}

.app-main {
  padding: 15px;
  position: relative;
  overflow: hidden;
  min-height: calc(100vh - 50px);
}

.fade-transform-enter-active,
.fade-transform-leave-active {
  transition: all 0.3s;
}

.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style> 