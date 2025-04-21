<template>
  <div class="app-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>用户列表</span>
          <el-button type="primary" size="small">添加用户</el-button>
        </div>
      </template>
      
      <div class="filter-container">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="用户名">
            <el-input v-model="searchForm.username" placeholder="请输入用户名" clearable></el-input>
          </el-form-item>
          <el-form-item label="手机号">
            <el-input v-model="searchForm.phone" placeholder="请输入手机号" clearable></el-input>
          </el-form-item>
          <el-form-item label="用户状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
              <el-option label="正常" value="normal"></el-option>
              <el-option label="禁用" value="disabled"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <el-table :data="userList" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="avatar" label="头像" width="80">
          <template #default="scope">
            <el-avatar :size="40" :src="scope.row.avatar"></el-avatar>
          </template>
        </el-table-column>
        <el-table-column prop="username" label="用户名" width="120"></el-table-column>
        <el-table-column prop="nickname" label="昵称" width="120"></el-table-column>
        <el-table-column prop="phone" label="手机号" width="120"></el-table-column>
        <el-table-column prop="level" label="用户等级" width="120">
          <template #default="scope">
            <el-tag :type="getLevelTagType(scope.row.level)">{{ scope.row.levelName }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-switch
              v-model="scope.row.status"
              :active-value="'normal'"
              :inactive-value="'disabled'"
              @change="handleStatusChange(scope.row)"
            ></el-switch>
          </template>
        </el-table-column>
        <el-table-column prop="registerTime" label="注册时间" min-width="180"></el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="handleViewDetail(scope.row)">查看</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-container">
        <el-pagination
          background
          layout="total, sizes, prev, pager, next, jumper"
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        >
        </el-pagination>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(false)

// 搜索表单
const searchForm = reactive({
  username: '',
  phone: '',
  status: ''
})

// 分页信息
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 100
})

// 用户列表
const userList = ref([
  {
    id: 1,
    avatar: '',
    username: 'user001',
    nickname: '张三',
    phone: '13800138001',
    level: 1,
    levelName: '普通会员',
    status: 'normal',
    registerTime: '2023-01-15 10:30:00'
  },
  {
    id: 2,
    avatar: '',
    username: 'user002',
    nickname: '李四',
    phone: '13800138002',
    level: 2,
    levelName: '银卡会员',
    status: 'normal',
    registerTime: '2023-02-20 15:45:00'
  },
  {
    id: 3,
    avatar: '',
    username: 'user003',
    nickname: '王五',
    phone: '13800138003',
    level: 3,
    levelName: '金卡会员',
    status: 'normal',
    registerTime: '2023-03-10 09:15:00'
  },
  {
    id: 4,
    avatar: '',
    username: 'user004',
    nickname: '赵六',
    phone: '13800138004',
    level: 4,
    levelName: '钻石会员',
    status: 'disabled',
    registerTime: '2023-04-05 14:20:00'
  }
])

// 获取用户等级对应的标签类型
const getLevelTagType = (level) => {
  const types = ['', 'info', 'success', 'warning', 'danger']
  return types[level] || 'info'
}

// 加载数据
const fetchUserList = () => {
  loading.value = true
  // 模拟API请求
  setTimeout(() => {
    loading.value = false
  }, 500)
}

// 搜索
const handleSearch = () => {
  pagination.currentPage = 1
  fetchUserList()
}

// 重置搜索
const resetSearch = () => {
  searchForm.username = ''
  searchForm.phone = ''
  searchForm.status = ''
  handleSearch()
}

// 查看用户详情
const handleViewDetail = (row) => {
  router.push(`/user/detail/${row.id}`)
}

// 更改用户状态
const handleStatusChange = (row) => {
  console.log('状态变更', row)
}

// 删除用户
const handleDelete = (row) => {
  console.log('删除用户', row)
}

// 分页大小变化
const handleSizeChange = (size) => {
  pagination.pageSize = size
  fetchUserList()
}

// 页数变化
const handleCurrentChange = (page) => {
  pagination.currentPage = page
  fetchUserList()
}

// 初始化
fetchUserList()
</script>

<style scoped>
.filter-container {
  margin-bottom: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style> 