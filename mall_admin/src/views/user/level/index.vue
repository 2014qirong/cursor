<template>
  <div class="app-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>会员等级管理</span>
          <el-button type="primary" size="small" @click="handleAddLevel">添加等级</el-button>
        </div>
      </template>
      
      <el-table :data="levelList" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="name" label="等级名称" width="120"></el-table-column>
        <el-table-column prop="icon" label="图标" width="100">
          <template #default="scope">
            <el-image
              style="width: 30px; height: 30px"
              :src="scope.row.icon || ''"
              fit="contain"
            ></el-image>
          </template>
        </el-table-column>
        <el-table-column prop="pointsThreshold" label="积分门槛" width="120"></el-table-column>
        <el-table-column prop="discount" label="折扣" width="100">
          <template #default="scope">
            {{ scope.row.discount }}折
          </template>
        </el-table-column>
        <el-table-column prop="description" label="等级描述"></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-switch
              v-model="scope.row.status"
              :active-value="1"
              :inactive-value="0"
              @change="handleStatusChange(scope.row)"
            ></el-switch>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="handleEditLevel(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDeleteLevel(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 等级表单对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form :model="levelForm" label-width="100px">
        <el-form-item label="等级名称">
          <el-input v-model="levelForm.name" placeholder="请输入等级名称"></el-input>
        </el-form-item>
        <el-form-item label="图标">
          <el-upload
            class="avatar-uploader"
            action="#"
            :auto-upload="false"
            :show-file-list="false"
          >
            <img v-if="levelForm.icon" :src="levelForm.icon" class="avatar">
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="积分门槛">
          <el-input-number v-model="levelForm.pointsThreshold" :min="0" :step="100"></el-input-number>
        </el-form-item>
        <el-form-item label="折扣">
          <el-input-number v-model="levelForm.discount" :min="0" :max="10" :precision="1" :step="0.1"></el-input-number>
          <span class="form-tip">0-10之间，例如：8.5表示85折</span>
        </el-form-item>
        <el-form-item label="等级描述">
          <el-input type="textarea" v-model="levelForm.description" placeholder="请输入等级描述"></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="levelForm.status" :active-value="1" :inactive-value="0"></el-switch>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmitLevel">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { Plus } from '@element-plus/icons-vue'

const loading = ref(false)

// 等级列表
const levelList = ref([
  {
    id: 1,
    name: '普通会员',
    icon: '',
    pointsThreshold: 0,
    discount: 10,
    description: '普通会员享受正常价格',
    status: 1
  },
  {
    id: 2,
    name: '银卡会员',
    icon: '',
    pointsThreshold: 1000,
    discount: 9.5,
    description: '银卡会员享受95折优惠',
    status: 1
  },
  {
    id: 3,
    name: '金卡会员',
    icon: '',
    pointsThreshold: 5000,
    discount: 9,
    description: '金卡会员享受9折优惠',
    status: 1
  },
  {
    id: 4,
    name: '钻石会员',
    icon: '',
    pointsThreshold: 10000,
    discount: 8.5,
    description: '钻石会员享受85折优惠和专属客服',
    status: 1
  }
])

// 对话框相关
const dialogVisible = ref(false)
const dialogTitle = ref('添加等级')
const levelForm = reactive({
  id: null,
  name: '',
  icon: '',
  pointsThreshold: 0,
  discount: 10,
  description: '',
  status: 1
})

// 加载数据
const fetchLevelList = () => {
  loading.value = true
  // 模拟API请求
  setTimeout(() => {
    loading.value = false
  }, 500)
}

// 添加等级
const handleAddLevel = () => {
  dialogTitle.value = '添加等级'
  Object.assign(levelForm, {
    id: null,
    name: '',
    icon: '',
    pointsThreshold: 0,
    discount: 10,
    description: '',
    status: 1
  })
  dialogVisible.value = true
}

// 编辑等级
const handleEditLevel = (row) => {
  dialogTitle.value = '编辑等级'
  Object.assign(levelForm, { ...row })
  dialogVisible.value = true
}

// 删除等级
const handleDeleteLevel = (row) => {
  console.log('删除等级', row)
}

// 状态变更
const handleStatusChange = (row) => {
  console.log('状态变更', row)
}

// 提交等级表单
const handleSubmitLevel = () => {
  console.log('提交等级', levelForm)
  dialogVisible.value = false
}

// 初始化
fetchLevelList()
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.form-tip {
  margin-left: 10px;
  color: #909399;
  font-size: 12px;
}
.avatar-uploader {
  width: 100px;
  height: 100px;
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader:hover {
  border-color: #409EFF;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  text-align: center;
  line-height: 100px;
}
.avatar {
  width: 100px;
  height: 100px;
  display: block;
}
</style> 