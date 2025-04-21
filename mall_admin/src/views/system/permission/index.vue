<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>权限管理</span>
          <el-button type="primary" @click="handleAddPermission">添加权限</el-button>
        </div>
      </template>

      <el-table
        v-loading="loading"
        :data="permissionTableData"
        row-key="id"
        border
        default-expand-all
        :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
      >
        <el-table-column prop="name" label="权限名称" min-width="180" />
        <el-table-column prop="code" label="权限标识" width="180" />
        <el-table-column prop="description" label="权限描述" min-width="180" />
        <el-table-column label="类型" width="100" align="center">
          <template #default="scope">
            <el-tag v-if="scope.row.type === 1" type="primary">目录</el-tag>
            <el-tag v-else-if="scope.row.type === 2" type="success">菜单</el-tag>
            <el-tag v-else-if="scope.row.type === 3" type="warning">按钮</el-tag>
            <el-tag v-else>其他</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="path" label="路径" min-width="180" />
        <el-table-column prop="component" label="组件" min-width="180" show-overflow-tooltip />
        <el-table-column prop="icon" label="图标" width="100" align="center">
          <template #default="scope">
            <el-icon v-if="scope.row.icon">
              <component :is="scope.row.icon" />
            </el-icon>
            <span v-else>-</span>
          </template>
        </el-table-column>
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
        <el-table-column label="操作" width="200" fixed="right">
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
              v-if="scope.row.type !== 3"
              size="small"
              type="success"
              link
              @click="handleAddChild(scope.row)"
            >
              添加子项
            </el-button>
            <el-button
              size="small"
              type="danger"
              link
              @click="handleDelete(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑权限对话框 -->
    <el-dialog
      :title="dialogType === 'add' ? '添加权限' : '编辑权限'"
      v-model="dialogVisible"
      width="600px"
    >
      <el-form
        ref="permissionFormRef"
        :model="permissionForm"
        :rules="permissionRules"
        label-width="100px"
      >
        <el-form-item label="上级权限">
          <el-tree-select
            v-model="permissionForm.parentId"
            :data="permissionOptions"
            :props="{ label: 'name', value: 'id', children: 'children' }"
            value-key="id"
            placeholder="请选择上级权限"
            check-strictly
            clearable
            :disabled="dialogType === 'edit' && permissionForm.id === 1"
          />
        </el-form-item>
        
        <el-form-item label="权限类型" prop="type">
          <el-radio-group v-model="permissionForm.type">
            <el-radio :label="1">目录</el-radio>
            <el-radio :label="2">菜单</el-radio>
            <el-radio :label="3">按钮</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="权限名称" prop="name">
          <el-input v-model="permissionForm.name" placeholder="请输入权限名称" />
        </el-form-item>
        
        <el-form-item label="权限标识" prop="code">
          <el-input v-model="permissionForm.code" placeholder="请输入权限标识" />
          <div class="form-item-help">例如：system:user:list，目录或菜单可留空</div>
        </el-form-item>
        
        <template v-if="permissionForm.type !== 3">
          <el-form-item label="路由路径" prop="path">
            <el-input v-model="permissionForm.path" placeholder="请输入路由路径" />
            <div class="form-item-help">例如：/system/user 或 user</div>
          </el-form-item>
          
          <el-form-item v-if="permissionForm.type === 2" label="组件路径" prop="component">
            <el-input v-model="permissionForm.component" placeholder="请输入组件路径" />
            <div class="form-item-help">例如：system/user/index</div>
          </el-form-item>
          
          <el-form-item label="图标" prop="icon">
            <el-input v-model="permissionForm.icon" placeholder="请输入图标名称" />
            <div class="form-item-help">使用Element Plus图标，例如：User</div>
          </el-form-item>
        </template>
        
        <el-form-item label="排序" prop="sort">
          <el-input-number v-model="permissionForm.sort" :min="0" :max="999" />
          <div class="form-item-help">数字越小越靠前</div>
        </el-form-item>
        
        <el-form-item label="权限描述" prop="description">
          <el-input
            v-model="permissionForm.description"
            type="textarea"
            rows="3"
            placeholder="请输入权限描述"
          />
        </el-form-item>
        
        <el-form-item label="状态">
          <el-radio-group v-model="permissionForm.status">
            <el-radio :label="1">启用</el-radio>
            <el-radio :label="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitPermissionForm">确定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 表格数据加载状态
const loading = ref(false)

// 权限数据
const permissionTableData = ref([
  {
    id: 1,
    name: '系统管理',
    code: 'system',
    type: 1,
    path: '/system',
    component: 'Layout',
    icon: 'Setting',
    sort: 1,
    status: 1,
    description: '系统管理模块',
    children: [
      {
        id: 2,
        parentId: 1,
        name: '用户管理',
        code: 'system:user',
        type: 2,
        path: 'user',
        component: 'system/user/index',
        icon: 'User',
        sort: 1,
        status: 1,
        description: '用户管理页面',
        children: [
          {
            id: 8,
            parentId: 2,
            name: '用户查询',
            code: 'system:user:list',
            type: 3,
            sort: 1,
            status: 1,
            description: '查询用户列表'
          },
          {
            id: 9,
            parentId: 2,
            name: '用户新增',
            code: 'system:user:add',
            type: 3,
            sort: 2,
            status: 1,
            description: '新增用户信息'
          },
          {
            id: 10,
            parentId: 2,
            name: '用户修改',
            code: 'system:user:edit',
            type: 3,
            sort: 3,
            status: 1,
            description: '修改用户信息'
          },
          {
            id: 11,
            parentId: 2,
            name: '用户删除',
            code: 'system:user:delete',
            type: 3,
            sort: 4,
            status: 1,
            description: '删除用户信息'
          }
        ]
      },
      {
        id: 3,
        parentId: 1,
        name: '角色管理',
        code: 'system:role',
        type: 2,
        path: 'role',
        component: 'system/role/index',
        icon: 'Avatar',
        sort: 2,
        status: 1,
        description: '角色管理页面',
        children: [
          {
            id: 12,
            parentId: 3,
            name: '角色查询',
            code: 'system:role:list',
            type: 3,
            sort: 1,
            status: 1,
            description: '查询角色列表'
          },
          {
            id: 13,
            parentId: 3,
            name: '角色新增',
            code: 'system:role:add',
            type: 3,
            sort: 2,
            status: 1,
            description: '新增角色信息'
          },
          {
            id: 14,
            parentId: 3,
            name: '角色修改',
            code: 'system:role:edit',
            type: 3,
            sort: 3,
            status: 1,
            description: '修改角色信息'
          },
          {
            id: 15,
            parentId: 3,
            name: '角色删除',
            code: 'system:role:delete',
            type: 3,
            sort: 4,
            status: 1,
            description: '删除角色信息'
          }
        ]
      },
      {
        id: 4,
        parentId: 1,
        name: '权限管理',
        code: 'system:permission',
        type: 2,
        path: 'permission',
        component: 'system/permission/index',
        icon: 'Lock',
        sort: 3,
        status: 1,
        description: '权限管理页面',
        children: [
          {
            id: 16,
            parentId: 4,
            name: '权限查询',
            code: 'system:permission:list',
            type: 3,
            sort: 1,
            status: 1,
            description: '查询权限列表'
          },
          {
            id: 17,
            parentId: 4,
            name: '权限新增',
            code: 'system:permission:add',
            type: 3,
            sort: 2,
            status: 1,
            description: '新增权限信息'
          },
          {
            id: 18,
            parentId: 4,
            name: '权限修改',
            code: 'system:permission:edit',
            type: 3,
            sort: 3,
            status: 1,
            description: '修改权限信息'
          },
          {
            id: 19,
            parentId: 4,
            name: '权限删除',
            code: 'system:permission:delete',
            type: 3,
            sort: 4,
            status: 1,
            description: '删除权限信息'
          }
        ]
      }
    ]
  },
  {
    id: 5,
    name: '商城管理',
    code: 'shop',
    type: 1,
    path: '/shop',
    component: 'Layout',
    icon: 'Shop',
    sort: 2,
    status: 1,
    description: '商城管理模块',
    children: [
      {
        id: 6,
        parentId: 5,
        name: '商品管理',
        code: 'shop:product',
        type: 2,
        path: 'product',
        component: 'shop/product/index',
        icon: 'ShoppingBag',
        sort: 1,
        status: 1,
        description: '商品管理页面',
        children: [
          {
            id: 20,
            parentId: 6,
            name: '商品查询',
            code: 'shop:product:list',
            type: 3,
            sort: 1,
            status: 1,
            description: '查询商品列表'
          },
          {
            id: 21,
            parentId: 6,
            name: '商品新增',
            code: 'shop:product:add',
            type: 3,
            sort: 2,
            status: 1,
            description: '新增商品信息'
          }
        ]
      },
      {
        id: 7,
        parentId: 5,
        name: '订单管理',
        code: 'shop:order',
        type: 2,
        path: 'order',
        component: 'shop/order/index',
        icon: 'Tickets',
        sort: 2,
        status: 1,
        description: '订单管理页面'
      }
    ]
  }
])

// 权限选项，用于级联选择器
const permissionOptions = computed(() => {
  // 添加一个虚拟的根节点
  return [
    {
      id: 0,
      name: '顶级菜单',
      children: permissionTableData.value
    }
  ]
})

// 对话框相关
const dialogVisible = ref(false)
const dialogType = ref('add') // 'add' or 'edit'
const permissionFormRef = ref(null)
const permissionForm = reactive({
  id: undefined,
  parentId: 0,
  name: '',
  code: '',
  type: 1,
  path: '',
  component: '',
  icon: '',
  sort: 0,
  status: 1,
  description: ''
})

// 表单验证规则
const permissionRules = {
  name: [
    { required: true, message: '请输入权限名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  code: [
    { pattern: /^[a-z]+(:[a-z]+)*$/, message: '权限标识格式不正确', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择权限类型', trigger: 'change' }
  ],
  path: [
    { required: true, message: '请输入路由路径', trigger: 'blur', type: 2 }
  ],
  component: [
    { required: true, message: '请输入组件路径', trigger: 'blur', type: 2 }
  ]
}

// 处理添加权限
const handleAddPermission = () => {
  dialogType.value = 'add'
  resetForm()
  dialogVisible.value = true
}

// 处理添加子权限
const handleAddChild = (row) => {
  dialogType.value = 'add'
  resetForm()
  permissionForm.parentId = row.id
  permissionForm.type = row.type === 1 ? 2 : 3
  dialogVisible.value = true
}

// 处理编辑权限
const handleEdit = (row) => {
  dialogType.value = 'edit'
  resetForm()
  Object.assign(permissionForm, { ...row })
  dialogVisible.value = true
}

// 重置表单
const resetForm = () => {
  if (permissionFormRef.value) {
    permissionFormRef.value.resetFields()
  }
  
  Object.assign(permissionForm, {
    id: undefined,
    parentId: 0,
    name: '',
    code: '',
    type: 1,
    path: '',
    component: '',
    icon: '',
    sort: 0,
    status: 1,
    description: ''
  })
}

// 处理状态变更
const handleStatusChange = (row) => {
  const statusText = row.status === 1 ? '启用' : '禁用'
  ElMessage.success(`已${statusText}：${row.name}`)
  
  // 实际应用中应调用API更新状态
  console.log('状态变更:', row)
}

// 处理删除权限
const handleDelete = (row) => {
  ElMessageBox.confirm(`确认删除 ${row.name} 吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 实际应用中应调用API删除
    deletePermission(row.id)
    ElMessage.success('删除成功')
  }).catch(() => {})
}

// 递归删除权限
const deletePermission = (id) => {
  const deleteNode = (list, id) => {
    for (let i = 0; i < list.length; i++) {
      if (list[i].id === id) {
        list.splice(i, 1)
        return true
      }
      if (list[i].children && list[i].children.length) {
        if (deleteNode(list[i].children, id)) {
          return true
        }
      }
    }
    return false
  }
  
  deleteNode(permissionTableData.value, id)
}

// 提交权限表单
const submitPermissionForm = () => {
  if (!permissionFormRef.value) return
  
  permissionFormRef.value.validate((valid) => {
    if (valid) {
      if (dialogType.value === 'add') {
        // 添加权限
        const newPermission = { ...permissionForm }
        
        // 生成一个新的ID
        const maxId = getMaxId(permissionTableData.value)
        newPermission.id = maxId + 1
        
        if (newPermission.parentId === 0) {
          // 添加顶级权限
          permissionTableData.value.push(newPermission)
        } else {
          // 添加子权限
          addChild(permissionTableData.value, newPermission)
        }
        
        ElMessage.success('添加成功')
      } else {
        // 更新权限
        updatePermission(permissionTableData.value, permissionForm)
        ElMessage.success('更新成功')
      }
      
      dialogVisible.value = false
    }
  })
}

// 获取最大ID
const getMaxId = (list) => {
  let maxId = 0
  
  const traverse = (nodes) => {
    for (const node of nodes) {
      if (node.id > maxId) {
        maxId = node.id
      }
      if (node.children && node.children.length) {
        traverse(node.children)
      }
    }
  }
  
  traverse(list)
  return maxId
}

// 添加子权限
const addChild = (list, child) => {
  for (const item of list) {
    if (item.id === child.parentId) {
      if (!item.children) {
        item.children = []
      }
      item.children.push(child)
      return true
    }
    if (item.children && item.children.length) {
      if (addChild(item.children, child)) {
        return true
      }
    }
  }
  return false
}

// 更新权限
const updatePermission = (list, permission) => {
  for (let i = 0; i < list.length; i++) {
    if (list[i].id === permission.id) {
      // 保留子节点
      const children = list[i].children
      list[i] = { ...permission }
      if (children) {
        list[i].children = children
      }
      return true
    }
    if (list[i].children && list[i].children.length) {
      if (updatePermission(list[i].children, permission)) {
        return true
      }
    }
  }
  return false
}

onMounted(() => {
  loading.value = true
  // 模拟获取数据
  setTimeout(() => {
    loading.value = false
  }, 500)
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

.form-item-help {
  font-size: 12px;
  color: #999;
  line-height: 1.5;
  margin-top: 4px;
}
</style> 