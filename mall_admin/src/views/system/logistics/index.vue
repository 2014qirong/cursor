<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>物流配置</span>
          <el-button type="primary" @click="handleAddLogistics">添加物流公司</el-button>
        </div>
      </template>

      <el-table
        v-loading="listLoading"
        :data="logisticsList"
        border
        style="width: 100%"
      >
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column label="ID" prop="id" width="80" align="center" />
        <el-table-column label="物流公司名称" prop="name" min-width="120" />
        <el-table-column label="编码" prop="code" width="120" align="center" />
        <el-table-column label="排序" prop="sort" width="80" align="center" />
        <el-table-column label="状态" prop="status" width="100" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.status === 1 ? 'success' : 'info'">
              {{ scope.row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" align="center">
          <template #default="scope">
            <el-button 
              size="small" 
              type="primary" 
              link 
              @click="handleEditLogistics(scope.row)"
            >
              编辑
            </el-button>
            <el-button 
              size="small" 
              :type="scope.row.status === 0 ? 'success' : 'warning'" 
              link 
              @click="handleStatusChange(scope.row)"
            >
              {{ scope.row.status === 0 ? '启用' : '禁用' }}
            </el-button>
            <el-button 
              size="small" 
              type="danger" 
              link 
              @click="handleDeleteLogistics(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 基本设置 -->
      <el-divider content-position="left">基本设置</el-divider>
      
      <el-form
        ref="settingsFormRef"
        :model="settingsForm"
        label-width="120px"
        class="settings-form"
      >
        <el-form-item label="运费计算方式">
          <el-radio-group v-model="settingsForm.freightType">
            <el-radio :label="1">按件数</el-radio>
            <el-radio :label="2">按重量</el-radio>
            <el-radio :label="3">按体积</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="默认物流公司">
          <el-select v-model="settingsForm.defaultCompany" placeholder="请选择默认物流公司">
            <el-option
              v-for="item in logisticsList.filter(i => i.status === 1)"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="免运费额度">
          <el-input-number 
            v-model="settingsForm.freeShippingAmount" 
            :min="0" 
            :precision="2" 
            :step="10"
          />
          <span class="ml-2">元，订单满额免运费（0表示不启用）</span>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="saveSettings">保存设置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 物流公司表单对话框 -->
    <el-dialog
      :title="dialogStatus === 'create' ? '添加物流公司' : '编辑物流公司'"
      v-model="dialogFormVisible"
      width="500px"
    >
      <el-form
        ref="logisticsFormRef"
        :model="logisticsForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="公司名称" prop="name">
          <el-input v-model="logisticsForm.name" placeholder="请输入物流公司名称" />
        </el-form-item>
        
        <el-form-item label="编码" prop="code">
          <el-input v-model="logisticsForm.code" placeholder="请输入物流公司编码" />
        </el-form-item>
        
        <el-form-item label="排序" prop="sort">
          <el-input-number v-model="logisticsForm.sort" :min="0" :max="999" />
        </el-form-item>
        
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="logisticsForm.status">
            <el-radio :label="1">启用</el-radio>
            <el-radio :label="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取消</el-button>
          <el-button type="primary" @click="submitLogisticsForm">确定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 列表数据
const logisticsList = ref([
  {
    id: 1,
    name: '顺丰速运',
    code: 'SF',
    sort: 1,
    status: 1
  },
  {
    id: 2,
    name: '中通快递',
    code: 'ZTO',
    sort: 2,
    status: 1
  },
  {
    id: 3,
    name: '圆通速递',
    code: 'YTO',
    sort: 3,
    status: 1
  },
  {
    id: 4,
    name: '申通快递',
    code: 'STO',
    sort: 4,
    status: 1
  },
  {
    id: 5,
    name: '韵达快递',
    code: 'YD',
    sort: 5,
    status: 1
  },
  {
    id: 6,
    name: '邮政EMS',
    code: 'EMS',
    sort: 6,
    status: 1
  },
  {
    id: 7,
    name: '百世快递',
    code: 'HTKY',
    sort: 7,
    status: 0
  }
])

const listLoading = ref(false)

// 表单相关
const dialogStatus = ref('create')
const dialogFormVisible = ref(false)
const logisticsFormRef = ref(null)
const logisticsForm = reactive({
  id: undefined,
  name: '',
  code: '',
  sort: 0,
  status: 1
})

// 基本设置表单
const settingsFormRef = ref(null)
const settingsForm = reactive({
  freightType: 1,
  defaultCompany: 1,
  freeShippingAmount: 99
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入物流公司名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在2到50个字符之间', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入物流公司编码', trigger: 'blur' },
    { pattern: /^[A-Z0-9]+$/, message: '编码只能包含大写字母和数字', trigger: 'blur' }
  ]
}

// 打开添加对话框
const handleAddLogistics = () => {
  dialogStatus.value = 'create'
  Object.assign(logisticsForm, {
    id: undefined,
    name: '',
    code: '',
    sort: 0,
    status: 1
  })
  dialogFormVisible.value = true
  nextTick(() => {
    if (logisticsFormRef.value) {
      logisticsFormRef.value.clearValidate()
    }
  })
}

// 打开编辑对话框
const handleEditLogistics = (row) => {
  dialogStatus.value = 'update'
  Object.assign(logisticsForm, { ...row })
  dialogFormVisible.value = true
  nextTick(() => {
    if (logisticsFormRef.value) {
      logisticsFormRef.value.clearValidate()
    }
  })
}

// 提交表单
const submitLogisticsForm = () => {
  if (!logisticsFormRef.value) return
  
  logisticsFormRef.value.validate((valid) => {
    if (valid) {
      if (dialogStatus.value === 'create') {
        // 新增物流公司
        const newId = logisticsList.value.length > 0 
          ? Math.max(...logisticsList.value.map(item => item.id)) + 1 
          : 1
        logisticsList.value.push({
          ...logisticsForm,
          id: newId
        })
        ElMessage.success('添加成功')
      } else {
        // 更新物流公司
        const index = logisticsList.value.findIndex(item => item.id === logisticsForm.id)
        if (index !== -1) {
          logisticsList.value[index] = { ...logisticsForm }
          ElMessage.success('更新成功')
        }
      }
      dialogFormVisible.value = false
    }
  })
}

// 处理状态变更
const handleStatusChange = (row) => {
  const newStatus = row.status === 1 ? 0 : 1
  const statusText = newStatus === 1 ? '启用' : '禁用'
  
  ElMessageBox.confirm(
    `确定要${statusText}该物流公司吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    const index = logisticsList.value.findIndex(item => item.id === row.id)
    if (index !== -1) {
      logisticsList.value[index].status = newStatus
      ElMessage.success(`${statusText}成功`)
    }
  }).catch(() => {})
}

// 处理删除
const handleDeleteLogistics = (row) => {
  ElMessageBox.confirm(
    '确定要删除该物流公司吗？删除后无法恢复。',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    const index = logisticsList.value.findIndex(item => item.id === row.id)
    if (index !== -1) {
      logisticsList.value.splice(index, 1)
      ElMessage.success('删除成功')
    }
  }).catch(() => {})
}

// 保存基本设置
const saveSettings = () => {
  // 实际应用中应该调用API保存设置
  console.log('保存物流基本设置:', settingsForm)
  ElMessage.success('物流基本设置保存成功')
}

onMounted(() => {
  // 模拟获取数据
  listLoading.value = true
  setTimeout(() => {
    listLoading.value = false
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

.settings-form {
  max-width: 600px;
  margin-top: 20px;
}

.ml-2 {
  margin-left: 10px;
}
</style> 