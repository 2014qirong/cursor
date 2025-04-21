<template>
  <div class="login-container">
    <el-form
      ref="loginFormRef"
      :model="loginForm"
      :rules="loginRules"
      class="login-form"
      autocomplete="on"
      label-position="left"
    >
      <div class="title-container">
        <h3 class="title">商城小程序管理系统</h3>
      </div>

      <el-form-item prop="username">
        <el-input
          v-model="loginForm.username"
          placeholder="请输入用户名"
          type="text"
          prefix-icon="User"
          autocomplete="on"
        />
      </el-form-item>

      <el-form-item prop="password">
        <el-input
          v-model="loginForm.password"
          placeholder="请输入密码"
          :type="passwordVisible ? 'text' : 'password'"
          prefix-icon="Lock"
          autocomplete="on"
        >
          <template #suffix>
            <el-icon class="el-input__icon" @click="passwordVisible = !passwordVisible">
              <component :is="passwordVisible ? 'View' : 'Hide'" />
            </el-icon>
          </template>
        </el-input>
      </el-form-item>

      <el-button
        :loading="loading"
        type="primary"
        class="login-button"
        @click.prevent="handleLogin"
      >
        登录
      </el-button>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { setToken } from '@/utils/auth'

const router = useRouter()
const loginFormRef = ref(null)
const loading = ref(false)
const passwordVisible = ref(false)

const loginForm = reactive({
  username: 'admin',
  password: '123456'
})

const loginRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = () => {
  loginFormRef.value.validate(valid => {
    if (valid) {
      loading.value = true
      // 这里是模拟登录，实际项目中应该调用登录接口
      setTimeout(() => {
        setToken('admin-token')
        ElMessage.success('登录成功')
        router.push({ path: '/' })
        loading.value = false
      }, 1000)
    } else {
      return false
    }
  })
}
</script>

<style lang="scss" scoped>
$bg: #283443;
$light_gray: #fff;
$cursor: #fff;

@supports (-webkit-backdrop-filter: none) or (backdrop-filter: none) {
  .login-container {
    backdrop-filter: blur(10px);
  }
}

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1600 900'%3E%3Cpolygon fill='%23cc5577' points='957 450 539 900 1396 900'/%3E%3Cpolygon fill='%23882233' points='957 450 872.9 900 1396 900'/%3E%3Cpolygon fill='%23c45577' points='-60 900 398 662 816 900'/%3E%3Cpolygon fill='%23822233' points='337 900 398 662 816 900'/%3E%3Cpolygon fill='%23b95577' points='1203 546 1552 900 876 900'/%3E%3Cpolygon fill='%237a2233' points='1203 546 1552 900 1162 900'/%3E%3Cpolygon fill='%23b05577' points='641 695 886 900 367 900'/%3E%3Cpolygon fill='%23742233' points='587 900 641 695 886 900'/%3E%3Cpolygon fill='%23a45577' points='1710 900 1401 632 1096 900'/%3E%3Cpolygon fill='%236d2233' points='1710 900 1401 632 1365 900'/%3E%3Cpolygon fill='%239b5577' points='1210 900 971 687 725 900'/%3E%3Cpolygon fill='%23662233' points='943 900 1210 900 971 687'/%3E%3C/svg%3E");
  background-attachment: fixed;
  background-size: cover;
  display: flex;
  justify-content: center;
  align-items: center;
  
  .login-form {
    position: relative;
    width: 450px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;
    
    .login-button {
      width: 100%;
      margin-bottom: 30px;
    }
  }
  
  .title-container {
    position: relative;
    
    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0 auto 40px;
      text-align: center;
      font-weight: bold;
    }
  }
  
  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
    margin-bottom: 25px;
  }
  
  :deep(.el-input) {
    display: inline-block;
    height: 47px;
    width: 100%;
    
    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;
      appearance: none;
      
      &::placeholder {
        color: rgba(255, 255, 255, 0.7);
      }
    }
    
    .el-input__wrapper {
      background-color: transparent;
      box-shadow: none;
      padding: 0;
    }
  }
}
</style> 