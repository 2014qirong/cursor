<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>角色管理</span>
          <el-button type="primary" @click="handleAddRole">新增角色</el-button>
        </div>
      </template>

      <!-- 角色列表 -->
      <el-table
        v-loading="loading"
        :data="roleList"
        border
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="角色名称" width="150" />
        <el-table-column prop="code" label="角色标识" width="150" />
        <el-table-column prop="description" label="角色描述" min-width="200" />
        <el-table-column prop="sort" label="排序" width="80" align="center" />
        <el-table-column label="状态" width="100" align="center">
          <template #default="scope">
            <el-switch
              v-model="scope.row.status"
              :active-value="1"
              :inactive-value="0"
              @change="handleStatusChange(scope.row)"
            />
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="160" />
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="scope">
            <el-button
              size="small"
              type="primary"
              link
              @click="handleEdit(scope.row)"
            >
              编辑
            </el-button>
            <el-button
              size="small"
              type="success"
              link
              @click="handleAssignPermission(scope.row)"
            >
              分配权限
            </el-button>
            <el-button
              size="small"
              type="danger"
              link
              :disabled="scope.row.isSystem === 1"
              @click="handleDelete(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="queryParams.pageNum"
          v-model:page-size="queryParams.pageSize"
          :page-sizes="[10, 20, 30, 50]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 添加/编辑角色对话框 -->
    <el-dialog
      :title="dialogType === 'add' ? '新增角色' : '编辑角色'"
      v-model="dialogVisible"
      width="500px"
    >
      <el-form
        ref="roleFormRef"
        :model="roleForm"
        :rules="roleRules"
        label-width="80px"
      >
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="roleForm.name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="角色标识" prop="code">
          <el-input v-model="roleForm.code" placeholder="请输入角色标识" />
          <div class="form-help">例如：admin, user, operator</div>
        </el-form-item>
        <el-form-item label="角色描述" prop="description">
          <el-input
            v-model="roleForm.description"
            type="textarea"
            rows="3"
            placeholder="请输入角色描述"
          />
        </el-form-item>
        <el-form-item label="排序" prop="sort">
          <el-input-number v-model="roleForm.sort" :min="0" :max="999" />
          <div class="form-help">数字越小越靠前</div>
        </el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="roleForm.status">
            <el-radio :label="1">启用</el-radio>
            <el-radio :label="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitRoleForm">确定</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 分配权限对话框 -->
    <el-dialog
      title="分配权限"
      v-model="permDialogVisible"
      width="550px"
    >
      <el-form label-width="80px">
        <el-form-item label="角色名称">
          <span>{{ currentRole.name }}</span>
        </el-form-item>
        <el-form-item label="角色标识">
          <span>{{ currentRole.code }}</span>
        </el-form-item>
        <el-form-item label="权限分配">
          <el-tree
            ref="permTreeRef"
            :data="permissionData"
            :props="{ label: 'name', children: 'children' }"
            show-checkbox
            node-key="id"
            default-expand-all
            :default-checked-keys="checkedPermissionKeys"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="permDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitPermissionAssignment">确定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 加载状态
const loading = ref(false)

// 查询参数
const queryParams = reactive({
  pageNum: 1,
  pageSize: 10
})

// 总数据条数
const total = ref(0)

// 角色列表数据
const roleList = ref([
  {
    id: 1,
    name: '超级管理员',
    code: 'admin',
    description: '系统最高权限，拥有所有权限',
    sort: 1,
    status: 1,
    isSystem: 1,
    createTime: '2023-01-01 00:00:00'
  },
  {
    id: 2,
    name: '商城管理员',
    code: 'shop_admin',
    description: '拥有商城管理相关权限',
    sort: 2,
    status: 1,
    isSystem: 0,
    createTime: '2023-01-01 00:00:00'
  },
  {
    id: 3,
    name: '内容管理员',
    code: 'content_admin',
    description: '负责内容管理和审核',
    sort: 3,
    status: 1,
    isSystem: 0,
    createTime: '2023-01-01 00:00:00'
  },
  {
    id: 4,
    name: '营销专员',
    code: 'marketing',
    description: '负责营销活动管理',
    sort: 4,
    status: 1,
    isSystem: 0,
    createTime: '2023-01-01 00:00:00'
  },
  {
    id: 5,
    name: '客服人员',
    code: 'customer_service',
    description: '负责订单处理和客户服务',
    sort: 5,
    status: 1,
    isSystem: 0,
    createTime: '2023-01-01 00:00:00'
  }
])

// 权限列表数据
const permissionData = ref([
  {
    id: 1,
    name: '系统管理',
    children: [
      {
        id: 2,
        name: '用户管理',
        children: [
          { id: 8, name: '用户查询' },
          { id: 9, name: '用户新增' },
          { id: 10, name: '用户修改' },
          { id: 11, name: '用户删除' }
        ]
      },
      {
        id: 3,
        name: '角色管理',
        children: [
          { id: 12, name: '角色查询' },
          { id: 13, name: '角色新增' },
          { id: 14, name: '角色修改' },
          { id: 15, name: '角色删除' }
        ]
      },
      {
        id: 4,
        name: '权限管理',
        children: [
          { id: 16, name: '权限查询' },
          { id: 17, name: '权限新增' },
          { id: 18, name: '权限修改' },
          { id: 19, name: '权限删除' }
        ]
      }
    ]
  },
  {
    id: 5,
    name: '商城管理',
    children: [
      {
        id: 6,
        name: '商品管理',
        children: [
          { id: 20, name: '商品查询' },
          { id: 21, name: '商品新增' },
          { id: 22, name: '商品修改' },
          { id: 23, name: '商品删除' }
        ]
      },
      {
        id: 7,
        name: '订单管理',
        children: [
          { id: 24, name: '订单查询' },
          { id: 25, name: '订单处理' },
          { id: 26, name: '订单导出' }
        ]
      }
    ]
  }
])

// 角色表单相关
const dialogVisible = ref(false)
const dialogType = ref('add') // 'add' or 'edit'
const roleFormRef = ref(null)
const roleForm = reactive({
  id: undefined,
  name: '',
  code: '',
  description: '',
  sort: 0,
  status: 1,
  isSystem: 0
})

// 权限分配对话框相关
const permDialogVisible = ref(false)
const permTreeRef = ref(null)
const currentRole = ref({})
const checkedPermissionKeys = ref([])

// 角色表单验证规则
const roleRules = {
  name: [
    { required: true, message: '请输入角色名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入角色标识', trigger: 'blur' },
    { pattern: /^[a-z][a-z0-9_]*$/, message: '角色标识只能包含小写字母、数字和下划线，并且以字母开头', trigger: 'blur' }
  ]
}

// 处理分页大小变更
const handleSizeChange = (val) => {
  queryParams.pageSize = val
  fetchRoleList()
}

// 处理页码变更
const handleCurrentChange = (val) => {
  queryParams.pageNum = val
  fetchRoleList()
}

// 获取角色列表数据
const fetchRoleList = () => {
  loading.value = true
  
  // 模拟API请求
  setTimeout(() => {
    // 分页处理，实际项目中应由后端返回分页后的数据
    total.value = roleList.value.length
    loading.value = false
  }, 300)
}

// 处理添加角色
const handleAddRole = () => {
  dialogType.value = 'add'
  resetRoleForm()
  dialogVisible.value = true
}

// 处理编辑角色
const handleEdit = (row) => {
  dialogType.value = 'edit'
  resetRoleForm()
  Object.assign(roleForm, { ...row })
  dialogVisible.value = true
}

// 重置角色表单
const resetRoleForm = () => {
  if (roleFormRef.value) {
    roleFormRef.value.resetFields()
  }
  
  Object.assign(roleForm, {
    id: undefined,
    name: '',
    code: '',
    description: '',
    sort: 0,
    status: 1,
    isSystem: 0
  })
}

// 提交角色表单
const submitRoleForm = () => {
  if (!roleFormRef.value) return
  
  roleFormRef.value.validate((valid) => {
    if (valid) {
      if (dialogType.value === 'add') {
        // 新增角色
        const newRole = { ...roleForm }
        
        // 生成ID和创建时间
        const maxId = Math.max(...roleList.value.map(item => item.id), 0)
        newRole.id = maxId + 1
        newRole.createTime = new Date().toLocaleString()
        
        roleList.value.push(newRole)
        ElMessage.success('新增角色成功')
      } else {
        // 编辑角色
        const index = roleList.value.findIndex(item => item.id === roleForm.id)
        if (index !== -1) {
          roleList.value[index] = { ...roleList.value[index], ...roleForm }
          ElMessage.success('修改角色成功')
        }
      }
      
      dialogVisible.value = false
    }
  })
}

// 处理角色状态变更
const handleStatusChange = (row) => {
  const statusText = row.status === 1 ? '启用' : '禁用'
  ElMessage.success(`已${statusText}角色：${row.name}`)
  
  // 实际应用中应调用API更新状态
  console.log('状态变更:', row)
}

// 处理删除角色
const handleDelete = (row) => {
  ElMessageBox.confirm(`确认删除角色 ${row.name} 吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    const index = roleList.value.findIndex(item => item.id === row.id)
    if (index !== -1) {
      roleList.value.splice(index, 1)
      ElMessage.success('删除角色成功')
    }
  }).catch(() => {})
}

// 处理分配权限
const handleAssignPermission = (row) => {
  currentRole.value = { ...row }
  permDialogVisible.value = true
  
  // 模拟获取当前角色权限
  // 实际应该调用API获取
  if (row.id === 1) { // 超级管理员拥有所有权限
    const allPermIds = getAllPermissionIds(permissionData.value)
    checkedPermissionKeys.value = allPermIds
  } else if (row.id === 2) { // 商城管理员
    checkedPermissionKeys.value = [5, 6, 7, 20, 21, 22, 23, 24, 25, 26]
  } else {
    checkedPermissionKeys.value = [8, 12, 16] // 默认基础查看权限
  }
}

// 获取所有权限ID
const getAllPermissionIds = (permissions) => {
  const ids = []
  
  const getIds = (items) => {
    for (const item of items) {
      ids.push(item.id)
      if (item.children && item.children.length > 0) {
        getIds(item.children)
      }
    }
  }
  
  getIds(permissions)
  return ids
}

// 提交权限分配
const submitPermissionAssignment = () => {
  if (!permTreeRef.value) return
  
  const checkedKeys = permTreeRef.value.getCheckedKeys()
  const halfCheckedKeys = permTreeRef.value.getHalfCheckedKeys()
  const allCheckedKeys = [...checkedKeys, ...halfCheckedKeys]
  
  // 实际应用中应调用API保存权限分配
  console.log('保存权限分配:', currentRole.value.id, allCheckedKeys)
  
  ElMessage.success(`已成功为角色 ${currentRole.value.name} 分配权限`)
  permDialogVisible.value = false
}

onMounted(() => {
  fetchRoleList()
})
</script>

<style lang="scss" scoped>
.app-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}

.form-help {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}
</style> 