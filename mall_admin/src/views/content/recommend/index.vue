<template>
  <div class="app-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>推荐位管理</span>
          <el-button type="primary" @click="handleAdd">新增推荐位</el-button>
        </div>
      </template>

      <el-table
        v-loading="loading"
        :data="recommendList"
        border
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="推荐位名称" min-width="120" />
        <el-table-column prop="code" label="推荐位标识" width="150" />
        <el-table-column prop="type" label="推荐类型" width="100">
          <template #default="scope">
            <el-tag v-if="scope.row.type === 1">首页</el-tag>
            <el-tag v-else-if="scope.row.type === 2" type="success">分类页</el-tag>
            <el-tag v-else-if="scope.row.type === 3" type="warning">专题页</el-tag>
            <el-tag v-else type="info">其他</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="sort" label="排序" width="80" align="center" />
        <el-table-column prop="status" label="状态" width="80" align="center">
          <template #default="scope">
            <el-switch
              v-model="scope.row.status"
              :active-value="1"
              :inactive-value="0"
              @change="handleStatusChange(scope.row)"
            />
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="180" />
        <el-table-column label="操作" width="220" fixed="right">
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
              @click="handleItems(scope.row)"
            >
              管理商品
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

    <!-- 添加/编辑推荐位对话框 -->
    <el-dialog
      :title="dialogType === 'add' ? '新增推荐位' : '编辑推荐位'"
      v-model="dialogVisible"
      width="550px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="推荐位名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入推荐位名称" />
        </el-form-item>
        <el-form-item label="推荐位标识" prop="code">
          <el-input 
            v-model="form.code" 
            placeholder="请输入推荐位标识代码" 
            :disabled="dialogType === 'edit'"
          />
          <div class="form-help">推荐位标识只能包含字母、数字和下划线，建议使用英文</div>
        </el-form-item>
        <el-form-item label="推荐类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择推荐类型" style="width: 100%">
            <el-option label="首页" :value="1" />
            <el-option label="分类页" :value="2" />
            <el-option label="专题页" :value="3" />
            <el-option label="其他" :value="4" />
          </el-select>
        </el-form-item>
        <el-form-item label="排序" prop="sort">
          <el-input-number v-model="form.sort" :min="0" :max="999" />
        </el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="form.status">
            <el-radio :label="1">启用</el-radio>
            <el-radio :label="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input 
            v-model="form.remark" 
            type="textarea" 
            rows="3" 
            placeholder="请输入备注信息" 
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 管理推荐商品对话框 -->
    <el-dialog
      title="管理推荐商品"
      v-model="itemsDialogVisible"
      width="900px"
    >
      <div v-if="currentRecommend.id" class="recommend-items">
        <div class="recommend-title">
          <h3>{{ currentRecommend.name }} - 推荐商品列表</h3>
          <el-button type="primary" @click="openSelectProducts">添加商品</el-button>
        </div>
        
        <el-table
          :data="recommendItems"
          border
          style="width: 100%"
        >
          <el-table-column type="index" label="序号" width="50" />
          <el-table-column label="商品图片" width="80">
            <template #default="scope">
              <el-image
                style="width: 50px; height: 50px"
                :src="scope.row.pic"
                fit="cover"
                :preview-src-list="[scope.row.pic]"
              />
            </template>
          </el-table-column>
          <el-table-column prop="name" label="商品名称" min-width="200" />
          <el-table-column prop="price" label="售价" width="100">
            <template #default="scope">
              ¥{{ scope.row.price.toFixed(2) }}
            </template>
          </el-table-column>
          <el-table-column prop="sort" label="排序" width="80" align="center">
            <template #default="scope">
              <el-input-number 
                v-model="scope.row.sort" 
                :min="0" 
                :max="99" 
                size="small"
                @change="handleItemSortChange(scope.row)"
              />
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100" align="center">
            <template #default="scope">
              <el-button
                size="small"
                type="danger"
                link
                @click="removeItem(scope.row, scope.$index)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 页面加载状态
const loading = ref(false)

// 推荐位列表数据
const recommendList = ref([
  {
    id: 1,
    name: '首页轮播下方推荐',
    code: 'home_banner_bottom',
    type: 1,
    sort: 1,
    status: 1,
    remark: '首页轮播图下方的推荐商品位',
    createTime: '2023-04-10 10:30:22'
  },
  {
    id: 2,
    name: '首页人气推荐',
    code: 'home_popular',
    type: 1,
    sort: 2,
    status: 1,
    remark: '首页人气推荐商品位',
    createTime: '2023-04-10 11:15:48'
  },
  {
    id: 3,
    name: '首页新品推荐',
    code: 'home_new',
    type: 1,
    sort: 3,
    status: 1,
    remark: '首页新品推荐商品位',
    createTime: '2023-04-10 14:22:36'
  },
  {
    id: 4,
    name: '分类页热门推荐',
    code: 'category_hot',
    type: 2,
    sort: 1,
    status: 0,
    remark: '分类页顶部热门推荐',
    createTime: '2023-04-12 09:31:27'
  }
])

// 表单相关
const dialogVisible = ref(false)
const dialogType = ref('add')
const formRef = ref(null)
const form = reactive({
  id: undefined,
  name: '',
  code: '',
  type: 1,
  sort: 0,
  status: 1,
  remark: ''
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入推荐位名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入推荐位标识', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9_]+$/, message: '推荐位标识只能包含字母、数字和下划线', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择推荐类型', trigger: 'change' }
  ]
}

// 推荐商品相关
const itemsDialogVisible = ref(false)
const currentRecommend = ref({})
const recommendItems = ref([
  {
    id: 101,
    name: '2024新款春季连衣裙',
    price: 129.00,
    pic: 'https://img.alicdn.com/imgextra/i3/O1CN01MXIs031FgFyogtjpR_!!6000000000514-0-yinhe.jpg',
    sort: 1
  },
  {
    id: 102,
    name: '男士休闲运动套装春秋季',
    price: 199.80,
    pic: 'https://img.alicdn.com/imgextra/i1/O1CN01uqDRY01bTaRkOlECn_!!6000000003469-0-yinhe.jpg',
    sort: 2
  },
  {
    id: 103,
    name: '儿童防晒衣夏季薄款',
    price: 89.90,
    pic: 'https://img.alicdn.com/imgextra/i4/O1CN01qRjmeP1RQh9nCDWwO_!!6000000002108-0-yinhe.jpg',
    sort: 3
  }
])

// 获取推荐位列表
const getRecommendList = () => {
  loading.value = true
  // 这里应该调用API获取推荐位列表
  setTimeout(() => {
    loading.value = false
  }, 500)
}

// 处理添加推荐位
const handleAdd = () => {
  resetForm()
  dialogType.value = 'add'
  dialogVisible.value = true
}

// 处理编辑推荐位
const handleEdit = (row) => {
  resetForm()
  dialogType.value = 'edit'
  Object.assign(form, { ...row })
  dialogVisible.value = true
}

// 重置表单
const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  Object.assign(form, {
    id: undefined,
    name: '',
    code: '',
    type: 1,
    sort: 0,
    status: 1,
    remark: ''
  })
}

// 提交表单
const submitForm = () => {
  if (!formRef.value) return
  
  formRef.value.validate((valid) => {
    if (valid) {
      if (dialogType.value === 'add') {
        // 新增推荐位
        const newItem = { ...form }
        newItem.id = Date.now()
        newItem.createTime = new Date().toLocaleString()
        recommendList.value.push(newItem)
        ElMessage.success('新增推荐位成功')
      } else {
        // 编辑推荐位
        const index = recommendList.value.findIndex(item => item.id === form.id)
        if (index !== -1) {
          recommendList.value[index] = { ...recommendList.value[index], ...form }
          ElMessage.success('修改推荐位成功')
        }
      }
      dialogVisible.value = false
    }
  })
}

// 处理删除推荐位
const handleDelete = (row) => {
  ElMessageBox.confirm(`确认删除推荐位 ${row.name} ?`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 实际应调用API删除
    const index = recommendList.value.findIndex(item => item.id === row.id)
    if (index !== -1) {
      recommendList.value.splice(index, 1)
      ElMessage.success('删除成功')
    }
  }).catch(() => {})
}

// 处理状态变更
const handleStatusChange = (row) => {
  const text = row.status === 1 ? '启用' : '禁用'
  ElMessage.success(`已${text}推荐位：${row.name}`)
}

// 处理管理推荐商品
const handleItems = (row) => {
  currentRecommend.value = { ...row }
  itemsDialogVisible.value = true
  
  // 这里应该调用API获取推荐位商品
  // 目前使用静态数据模拟
}

// 处理推荐商品排序变更
const handleItemSortChange = (row) => {
  ElMessage.success(`商品 ${row.name} 排序已更新`)
}

// 移除推荐商品
const removeItem = (row, index) => {
  ElMessageBox.confirm(`确认移除商品 ${row.name} ?`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    recommendItems.value.splice(index, 1)
    ElMessage.success('商品已从推荐位移除')
  }).catch(() => {})
}

// 打开选择商品对话框
const openSelectProducts = () => {
  ElMessage.info('选择商品功能需要对接商品列表，本示例不做实现')
}

onMounted(() => {
  getRecommendList()
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

.form-help {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.recommend-items {
  .recommend-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    
    h3 {
      margin: 0;
      color: #303133;
    }
  }
}
</style> 