<template>
  <div class="admin-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>管理员列表</span>
          <el-button type="primary" @click="handleAdd">新增管理员</el-button>
        </div>
      </template>
      
      <!-- 搜索表单 -->
      <el-form :inline="true" :model="queryParams" class="search-form">
        <el-form-item label="用户名">
          <el-input v-model="queryParams.username" placeholder="请输入用户名" clearable @keyup.enter="handleQuery" />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="queryParams.name" placeholder="请输入姓名" clearable @keyup.enter="handleQuery" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="queryParams.phone" placeholder="请输入手机号" clearable @keyup.enter="handleQuery" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="queryParams.status" placeholder="请选择状态" clearable>
            <el-option label="启用" :value="1" />
            <el-option label="禁用" :value="0" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleQuery">查询</el-button>
          <el-button @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 表格 -->
      <el-table
        v-loading="loading"
        :data="adminList"
        style="width: 100%"
        border
      >
        <el-table-column type="index" label="序号" width="50" align="center" />
        <el-table-column prop="username" label="用户名" min-width="120" show-overflow-tooltip />
        <el-table-column prop="name" label="姓名" width="120" show-overflow-tooltip />
        <el-table-column prop="phone" label="手机号" width="120" show-overflow-tooltip />
        <el-table-column prop="email" label="邮箱" min-width="180" show-overflow-tooltip />
        <el-table-column prop="roleName" label="角色" width="120" show-overflow-tooltip />
        <el-table-column prop="lastLoginTime" label="最后登录时间" width="160" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="80" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.status === 1 ? 'success' : 'danger'">
              {{ scope.row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template #default="scope">
            <el-button link type="primary" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button link type="primary" @click="handleResetPwd(scope.row)">重置密码</el-button>
            <el-button 
              link 
              :type="scope.row.status === 1 ? 'danger' : 'success'" 
              @click="handleStatusChange(scope.row)"
            >
              {{ scope.row.status === 1 ? '禁用' : '启用' }}
            </el-button>
            <el-button link type="danger" @click="handleDelete(scope.row)" v-if="scope.row.username !== 'admin'">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="queryParams.pageNum"
          v-model:page-size="queryParams.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
    <!-- 添加/编辑管理员对话框 -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="adminFormRef"
        :model="adminForm"
        :rules="adminRules"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="adminForm.username" placeholder="请输入用户名" :disabled="dialogType === 'edit'" />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="adminForm.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="dialogType === 'add'">
          <el-input v-model="adminForm.password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword" v-if="dialogType === 'add'">
          <el-input v-model="adminForm.confirmPassword" placeholder="请再次输入密码" show-password />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="adminForm.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="adminForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="角色" prop="roleId">
          <el-select v-model="adminForm.roleId" placeholder="请选择角色" style="width: 100%">
            <el-option
              v-for="item in roleOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="adminForm.status">
            <el-radio :label="1">启用</el-radio>
            <el-radio :label="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="adminForm.remark" type="textarea" :rows="3" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="submitForm">确 定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 重置密码对话框 -->
    <el-dialog
      title="重置密码"
      v-model="resetPwdDialogVisible"
      width="500px"
    >
      <el-form
        ref="resetPwdFormRef"
        :model="resetPwdForm"
        :rules="resetPwdRules"
        label-width="100px"
      >
        <el-form-item label="新密码" prop="password">
          <el-input v-model="resetPwdForm.password" placeholder="请输入新密码" show-password />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="resetPwdForm.confirmPassword" placeholder="请再次输入新密码" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="resetPwdDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="submitResetPwd">确 定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getAdminList, addAdmin, updateAdmin, deleteAdmin } from '@/api/system'
import { getRoleList } from '@/api/system'

// 查询参数
const queryParams = reactive({
  pageNum: 1,
  pageSize: 10,
  username: '',
  name: '',
  phone: '',
  status: ''
})

// 管理员列表数据
const loading = ref(false)
const adminList = ref([])
const total = ref(0)

// 角色选项
const roleOptions = ref([])

// 表单对话框
const dialogVisible = ref(false)
const dialogTitle = ref('添加管理员')
const dialogType = ref('add') // add 或 edit
const adminFormRef = ref(null)
const adminForm = reactive({
  id: '',
  username: '',
  name: '',
  password: '',
  confirmPassword: '',
  phone: '',
  email: '',
  roleId: '',
  status: 1,
  remark: ''
})

// 重置密码对话框
const resetPwdDialogVisible = ref(false)
const resetPwdFormRef = ref(null)
const resetPwdForm = reactive({
  id: '',
  password: '',
  confirmPassword: ''
})
const currentResetUser = ref(null)

// 表单校验规则
const validatePassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入密码'))
  } else if (value.length < 6) {
    callback(new Error('密码长度不能小于6位'))
  } else {
    if (adminForm.confirmPassword !== '') {
      if (!adminFormRef.value) return
      adminFormRef.value.validateField('confirmPassword')
    }
    callback()
  }
}

const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== adminForm.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const validateResetConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== resetPwdForm.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const adminRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  password: [
    { required: true, validator: validatePassword, trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  roleId: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ]
}

const resetPwdRules = {
  password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateResetConfirmPassword, trigger: 'blur' }
  ]
}

// 获取管理员列表
const getList = async () => {
  loading.value = true
  try {
    const res = await getAdminList(queryParams)
    adminList.value = res.data.list || []
    total.value = res.data.total || 0
  } catch (error) {
    console.error('获取管理员列表失败', error)
  } finally {
    loading.value = false
  }
}

// 获取角色列表
const getRoles = async () => {
  try {
    const res = await getRoleList({ pageSize: 100 })
    roleOptions.value = res.data.list || []
  } catch (error) {
    console.error('获取角色列表失败', error)
  }
}

// 查询操作
const handleQuery = () => {
  queryParams.pageNum = 1
  getList()
}

// 重置查询条件
const resetQuery = () => {
  Object.assign(queryParams, {
    pageNum: 1,
    pageSize: 10,
    username: '',
    name: '',
    phone: '',
    status: ''
  })
  getList()
}

// 分页大小改变
const handleSizeChange = (size) => {
  queryParams.pageSize = size
  getList()
}

// 分页页码改变
const handleCurrentChange = (current) => {
  queryParams.pageNum = current
  getList()
}

// 新增管理员
const handleAdd = () => {
  resetForm()
  dialogType.value = 'add'
  dialogTitle.value = '添加管理员'
  dialogVisible.value = true
}

// 编辑管理员
const handleEdit = (row) => {
  resetForm()
  dialogType.value = 'edit'
  dialogTitle.value = '编辑管理员'
  
  // 填充表单数据
  Object.assign(adminForm, {
    id: row.id,
    username: row.username,
    name: row.name,
    phone: row.phone,
    email: row.email,
    roleId: row.roleId,
    status: row.status,
    remark: row.remark
  })
  
  dialogVisible.value = true
}

// 重置密码
const handleResetPwd = (row) => {
  resetPwdForm.id = row.id
  resetPwdForm.password = ''
  resetPwdForm.confirmPassword = ''
  currentResetUser.value = row
  resetPwdDialogVisible.value = true
}

// 提交重置密码
const submitResetPwd = async () => {
  if (!resetPwdFormRef.value) return
  
  await resetPwdFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        // 这里是重置密码的API，示例中并没有独立的重置密码API，所以复用了更新管理员API
        await updateAdmin(resetPwdForm.id, { password: resetPwdForm.password })
        ElMessage.success('密码重置成功')
        resetPwdDialogVisible.value = false
      } catch (error) {
        console.error('重置密码失败', error)
        ElMessage.error('重置密码失败')
      }
    }
  })
}

// 改变管理员状态
const handleStatusChange = async (row) => {
  const text = row.status === 1 ? '禁用' : '启用'
  const newStatus = row.status === 1 ? 0 : 1
  
  ElMessageBox.confirm(
    `确认要${text}管理员 ${row.username} 吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await updateAdmin(row.id, { status: newStatus })
      ElMessage.success(`${text}成功`)
      // 修改本地数据
      row.status = newStatus
    } catch (error) {
      console.error(`${text}失败`, error)
      ElMessage.error(`${text}失败`)
    }
  }).catch(() => {})
}

// 删除管理员
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确认要删除管理员 ${row.username} 吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteAdmin(row.id)
      ElMessage.success('删除成功')
      // 刷新列表
      getList()
    } catch (error) {
      console.error('删除失败', error)
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

// 提交表单
const submitForm = async () => {
  if (!adminFormRef.value) return
  
  await adminFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        // 构造提交数据
        const data = {
          username: adminForm.username,
          name: adminForm.name,
          phone: adminForm.phone,
          email: adminForm.email,
          roleId: adminForm.roleId,
          status: adminForm.status,
          remark: adminForm.remark
        }
        
        // 如果是添加模式，需要包含密码
        if (dialogType.value === 'add') {
          data.password = adminForm.password
        }
        
        if (dialogType.value === 'add') {
          await addAdmin(data)
          ElMessage.success('添加成功')
        } else {
          await updateAdmin(adminForm.id, data)
          ElMessage.success('更新成功')
        }
        
        dialogVisible.value = false
        getList()
      } catch (error) {
        console.error('保存失败', error)
        ElMessage.error('保存失败')
      }
    }
  })
}

// 重置表单
const resetForm = () => {
  if (adminFormRef.value) {
    adminFormRef.value.resetFields()
  }
  
  Object.assign(adminForm, {
    id: '',
    username: '',
    name: '',
    password: '',
    confirmPassword: '',
    phone: '',
    email: '',
    roleId: '',
    status: 1,
    remark: ''
  })
}

onMounted(() => {
  getList()
  getRoles()
})
</script>

<style lang="scss" scoped>
.admin-container {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .search-form {
    margin-bottom: 20px;
  }
  
  .pagination-container {
    margin-top: 20px;
    text-align: right;
  }
}
</style> 