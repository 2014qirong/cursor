<template>
  <el-breadcrumb class="app-breadcrumb" separator="/">
    <transition-group name="breadcrumb">
      <el-breadcrumb-item v-for="(item, index) in breadcrumbs" :key="item.path">
        <span
          v-if="index === breadcrumbs.length - 1 || !item.redirect"
          class="no-redirect"
        >{{ item.meta.title }}</span>
        <a v-else @click.prevent="handleLink(item)">{{ item.meta.title }}</a>
      </el-breadcrumb-item>
    </transition-group>
  </el-breadcrumb>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const breadcrumbs = ref([])

// 生成面包屑导航
const getBreadcrumb = () => {
  // 如果当前路由没有matched属性，直接返回
  if (!route.matched) {
    return
  }
  
  // 过滤掉没有meta.title的路由和不显示的路由
  const matched = route.matched.filter(
    item => item.meta && item.meta.title && item.meta.breadcrumb !== false
  )

  // 如果设置了redirect的路由，则把首页路由添加到面包屑数组
  if (!matched[0]?.path.startsWith('/dashboard')) {
    matched.unshift({
      path: '/dashboard',
      meta: { title: '首页' },
      redirect: '/'
    })
  }

  breadcrumbs.value = matched
}

// 面包屑导航点击事件
const handleLink = (item) => {
  const { redirect, path } = item
  if (redirect) {
    router.push(redirect)
    return
  }
  router.push(path)
}

// 监听路由变化，更新面包屑导航
watch(
  () => route.path,
  () => {
    getBreadcrumb()
  },
  { immediate: true }
)
</script>

<style lang="scss" scoped>
.app-breadcrumb {
  display: inline-block;
  font-size: 14px;
  line-height: 50px;
  margin-left: 8px;
  
  .no-redirect {
    color: #97a8be;
    cursor: text;
  }
}

.breadcrumb-enter-active,
.breadcrumb-leave-active {
  transition: all 0.5s;
}

.breadcrumb-enter-from,
.breadcrumb-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

.breadcrumb-leave-active {
  position: absolute;
}
</style> 