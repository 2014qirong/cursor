<template>
  <div class="error-page">
    <div class="error-code">404</div>
    <div class="error-desc">抱歉，您访问的页面不存在</div>
    <div class="error-actions">
      <el-button type="primary" @click="goHome">返回首页</el-button>
      <el-button @click="goBack">返回上一页</el-button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push('/')
}

const goBack = () => {
  router.go(-1)
}
</script>

<style lang="scss" scoped>
.error-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f5f7fa;
  
  .error-code {
    font-size: 160px;
    font-weight: bold;
    color: #409EFF;
    text-shadow: 5px 5px 0 #e0e0e0;
    margin-bottom: 20px;
    line-height: 1;
  }
  
  .error-desc {
    font-size: 24px;
    color: #606266;
    margin-bottom: 30px;
  }
  
  .error-actions {
    display: flex;
    gap: 15px;
  }
}
</style> 