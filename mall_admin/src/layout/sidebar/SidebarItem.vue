<template>
  <div v-if="!item.hidden">
    <!-- 没有子菜单的路由项 -->
    <template v-if="hasOneShowingChild(item.children, item) && (!onlyOneChild.children || onlyOneChild.noShowingChildren) && !item.alwaysShow">
      <app-link 
        v-if="onlyOneChild.meta && onlyOneChild.meta.title" 
        :to="resolvePath(onlyOneChild.path)"
        @click="handleItemClick(onlyOneChild)"
      >
        <el-menu-item :index="resolvePath(onlyOneChild.path)">
          <el-icon v-if="onlyOneChild.meta && onlyOneChild.meta.icon">
            <component :is="onlyOneChild.meta.icon"></component>
          </el-icon>
          <template #title>{{ onlyOneChild.meta.title }}</template>
        </el-menu-item>
      </app-link>
    </template>

    <!-- 有子菜单的路由项 -->
    <el-sub-menu v-else-if="item && item.path" :index="resolvePath(item.path)" popper-append-to-body>
      <template #title @click="handleSubmenuTitleClick(item)">
        <el-icon v-if="item.meta && item.meta.icon">
          <component :is="item.meta.icon"></component>
        </el-icon>
        <span v-if="item.meta && item.meta.title">{{ item.meta.title }}</span>
      </template>
      
      <sidebar-item
        v-for="child in item.children"
        :key="child.path"
        :item="child"
        :base-path="resolvePath(child.path)"
      />
    </el-sub-menu>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { isExternal } from '@/utils/validate'
import AppLink from './Link.vue'
import path from 'path-browserify'

const router = useRouter()
const props = defineProps({
  item: {
    type: Object,
    required: true
  },
  basePath: {
    type: String,
    default: ''
  }
})

const onlyOneChild = ref(null)

// 调试信息
onMounted(() => {
  console.log('当前菜单项:', props.item)
})

// 点击菜单项
const handleItemClick = (item) => {
  if (!item || !item.path) return
  
  console.log('点击菜单项:', item)
  const fullPath = resolvePath(item.path)
  console.log('跳转路径:', fullPath)
  
  // 尝试通过编程式导航进行跳转
  try {
    router.push(fullPath)
  } catch (err) {
    console.error('路由跳转错误:', err)
  }
}

// 点击子菜单标题
const handleSubmenuTitleClick = (item) => {
  if (!item || !item.path) return
  
  console.log('点击子菜单标题:', item)
  
  if (item.redirect) {
    const redirectPath = isExternal(item.redirect) ? item.redirect : resolvePath(item.redirect)
    console.log('重定向路径:', redirectPath)
    
    // 尝试跳转到重定向路径
    try {
      router.push(redirectPath)
    } catch (err) {
      console.error('重定向跳转错误:', err)
    }
  }
}

// 判断是否只有一个可显示的子路由
const hasOneShowingChild = (children = [], parent) => {
  if (!children) {
    children = []
  }
  
  // 过滤掉隐藏的子路由
  const showingChildren = children.filter(item => {
    return !item.hidden
  })

  // 如果只有一个子路由
  if (showingChildren.length === 1) {
    onlyOneChild.value = showingChildren[0]
    return true
  }

  // 如果没有子路由，则将父路由作为唯一子路由
  if (showingChildren.length === 0) {
    // 确保父路由有meta属性
    onlyOneChild.value = { 
      ...parent, 
      path: '', 
      noShowingChildren: true,
      meta: parent.meta || { title: '', icon: '' } // 确保meta对象存在
    }
    return true
  }

  return false
}

// 解析路径
const resolvePath = (routePath) => {
  if (isExternal(routePath)) {
    return routePath
  }
  if (isExternal(props.basePath)) {
    return props.basePath
  }
  return path.resolve(props.basePath, routePath)
}
</script>

<style lang="scss" scoped>
.el-icon {
  margin-right: 6px;
  font-size: 18px;
  vertical-align: middle;
}

.el-menu-item, .el-sub-menu__title {
  &:hover {
    background-color: #263445 !important;
  }
}

.is-active > .el-menu-item {
  color: #409EFF !important;
}
</style> 