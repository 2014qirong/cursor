<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>积分商城管理</span>
          <el-button type="primary" @click="handleCreateItem">新增积分商品</el-button>
        </div>
      </template>

      <div class="filter-container">
        <el-form :inline="true" :model="listQuery" @keyup.enter="handleFilter">
          <el-form-item label="商品名称">
            <el-input v-model="listQuery.name" placeholder="请输入商品名称" clearable />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="listQuery.status" placeholder="全部状态" clearable>
              <el-option label="上架" :value="1" />
              <el-option label="下架" :value="0" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleFilter">查询</el-button>
            <el-button @click="resetQuery">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <el-table
        v-loading="listLoading"
        :data="list"
        border
        style="width: 100%"
      >
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column label="ID" prop="id" width="80" align="center" />
        <el-table-column label="商品图片" width="100" align="center">
          <template #default="scope">
            <el-image 
              :src="scope.row.pic" 
              :preview-src-list="[scope.row.pic]"
              style="width: 60px; height: 60px"
              fit="cover"
            />
          </template>
        </el-table-column>
        <el-table-column label="商品名称" prop="name" min-width="180" />
        <el-table-column label="积分价格" prop="points" width="120" align="center" />
        <el-table-column label="库存" prop="stock" width="100" align="center" />
        <el-table-column label="已兑换数量" prop="exchangeCount" width="120" align="center" />
        <el-table-column label="排序" prop="sort" width="100" align="center" />
        <el-table-column label="状态" prop="status" width="100" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.status === 1 ? 'success' : 'info'">
              {{ scope.row.status === 1 ? '上架' : '下架' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" prop="createTime" width="180" align="center" />
        <el-table-column label="操作" fixed="right" width="200" align="center">
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
              :type="scope.row.status === 0 ? 'success' : 'warning'" 
              link 
              @click="handleToggleStatus(scope.row)"
            >
              {{ scope.row.status === 0 ? '上架' : '下架' }}
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

      <pagination
        v-show="total > 0"
        :total="total"
        v-model:page="listQuery.page"
        v-model:limit="listQuery.limit"
        @pagination="getList"
      />
    </el-card>

    <!-- 积分商品表单对话框 -->
    <el-dialog
      :title="dialogStatus === 'create' ? '新增积分商品' : '编辑积分商品'"
      v-model="dialogFormVisible"
      width="600px"
    >
      <el-form
        ref="pointsItemFormRef"
        :model="pointsItemForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="商品名称" prop="name">
          <el-input v-model="pointsItemForm.name" placeholder="请输入商品名称" />
        </el-form-item>
        
        <el-form-item label="商品图片" prop="pic">
          <el-upload
            class="avatar-uploader"
            action="/api/upload"
            :show-file-list="false"
            :on-success="handleUploadSuccess"
            :before-upload="beforeUpload"
          >
            <img v-if="pointsItemForm.pic" :src="pointsItemForm.pic" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>

        <el-form-item label="所需积分" prop="points">
          <el-input-number v-model="pointsItemForm.points" :min="1" :max="999999" />
        </el-form-item>

        <el-form-item label="库存" prop="stock">
          <el-input-number v-model="pointsItemForm.stock" :min="0" :max="999999" />
        </el-form-item>

        <el-form-item label="排序" prop="sort">
          <el-input-number v-model="pointsItemForm.sort" :min="0" :max="999" />
        </el-form-item>

        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="pointsItemForm.status">
            <el-radio :label="1">上架</el-radio>
            <el-radio :label="0">下架</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="商品描述" prop="description">
          <el-input 
            v-model="pointsItemForm.description" 
            type="textarea" 
            rows="4" 
            placeholder="请输入商品描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import Pagination from '@/components/Pagination/index.vue'

// 模拟API，实际项目中应该从API获取数据
const getPointsMallList = (params) => {
  console.log('获取积分商城列表参数:', params)
  // 模拟异步请求
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        code: 200,
        data: {
          total: mockList.length,
          items: mockList.slice(
            (params.page - 1) * params.limit,
            params.page * params.limit
          )
        }
      })
    }, 300)
  })
}

// 模拟保存积分商品
const savePointsMallItem = (data) => {
  console.log('保存积分商品:', data)
  return new Promise((resolve) => {
    setTimeout(() => {
      if (data.id) {
        // 更新
        const index = mockList.findIndex(item => item.id === data.id)
        if (index !== -1) {
          mockList[index] = { ...mockList[index], ...data }
        }
      } else {
        // 新增
        const newItem = {
          ...data,
          id: Date.now(),
          createTime: new Date().toISOString().replace('T', ' ').substring(0, 19),
          exchangeCount: 0
        }
        mockList.unshift(newItem)
      }
      resolve({ code: 200, message: '操作成功' })
    }, 300)
  })
}

// 模拟删除积分商品
const deletePointsMallItem = (id) => {
  console.log('删除积分商品:', id)
  return new Promise((resolve) => {
    setTimeout(() => {
      const index = mockList.findIndex(item => item.id === id)
      if (index !== -1) {
        mockList.splice(index, 1)
      }
      resolve({ code: 200, message: '删除成功' })
    }, 300)
  })
}

// 模拟更新积分商品状态
const updatePointsMallItemStatus = (id, status) => {
  console.log('更新积分商品状态:', id, status)
  return new Promise((resolve) => {
    setTimeout(() => {
      const index = mockList.findIndex(item => item.id === id)
      if (index !== -1) {
        mockList[index].status = status
      }
      resolve({ code: 200, message: '状态更新成功' })
    }, 300)
  })
}

// 模拟数据
const mockList = [
  {
    id: 1,
    name: '小米手环7',
    pic: 'https://picsum.photos/200/200?random=1',
    points: 1999,
    stock: 100,
    exchangeCount: 58,
    sort: 1,
    status: 1,
    description: '智能运动手环，心率监测，多种运动模式',
    createTime: '2023-11-15 10:00:00'
  },
  {
    id: 2,
    name: '蓝牙耳机',
    pic: 'https://picsum.photos/200/200?random=2',
    points: 999,
    stock: 200,
    exchangeCount: 124,
    sort: 2,
    status: 1,
    description: '无线蓝牙耳机，降噪立体声',
    createTime: '2023-11-14 09:30:00'
  },
  {
    id: 3,
    name: '保温杯',
    pic: 'https://picsum.photos/200/200?random=3',
    points: 599,
    stock: 150,
    exchangeCount: 87,
    sort: 3,
    status: 1,
    description: '304不锈钢保温杯，24小时保温',
    createTime: '2023-11-13 14:20:00'
  },
  {
    id: 4,
    name: '雨伞',
    pic: 'https://picsum.photos/200/200?random=4',
    points: 399,
    stock: 300,
    exchangeCount: 210,
    sort: 4,
    status: 0,
    description: '防晒防雨两用伞，轻便折叠',
    createTime: '2023-11-12 11:15:00'
  },
  {
    id: 5,
    name: '抱枕',
    pic: 'https://picsum.photos/200/200?random=5',
    points: 299,
    stock: 400,
    exchangeCount: 156,
    sort: 5,
    status: 1,
    description: '舒适亲肤抱枕，午睡办公两用',
    createTime: '2023-11-11 16:40:00'
  }
]

// 列表数据
const list = ref([])
const total = ref(0)
const listLoading = ref(false)

// 表单相关
const dialogStatus = ref('create')
const dialogFormVisible = ref(false)
const pointsItemFormRef = ref(null)
const pointsItemForm = reactive({
  id: undefined,
  name: '',
  pic: '',
  points: 0,
  stock: 0,
  sort: 0,
  status: 1,
  description: ''
})

// 表单规则
const rules = {
  name: [
    { required: true, message: '请输入商品名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在2到50个字符之间', trigger: 'blur' }
  ],
  pic: [
    { required: true, message: '请上传商品图片', trigger: 'change' }
  ],
  points: [
    { required: true, message: '请输入所需积分', trigger: 'blur' }
  ],
  stock: [
    { required: true, message: '请输入库存数量', trigger: 'blur' }
  ]
}

// 查询参数
const listQuery = reactive({
  page: 1,
  limit: 10,
  name: '',
  status: ''
})

// 获取积分商品列表
const getList = async () => {
  listLoading.value = true
  try {
    const response = await getPointsMallList(listQuery)
    list.value = response.data.items
    total.value = response.data.total
  } catch (error) {
    console.error('获取积分商品列表失败:', error)
    ElMessage.error('获取积分商品列表失败')
  } finally {
    listLoading.value = false
  }
}

// 处理查询
const handleFilter = () => {
  listQuery.page = 1
  getList()
}

// 重置查询参数
const resetQuery = () => {
  listQuery.name = ''
  listQuery.status = ''
  handleFilter()
}

// 处理图片上传成功
const handleUploadSuccess = (res) => {
  pointsItemForm.pic = res.data.url
}

// 图片上传前的检查
const beforeUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过2MB!')
    return false
  }
  return true
}

// 打开创建对话框
const handleCreateItem = () => {
  dialogStatus.value = 'create'
  Object.assign(pointsItemForm, {
    id: undefined,
    name: '',
    pic: '',
    points: 0,
    stock: 0,
    sort: 0,
    status: 1,
    description: ''
  })
  dialogFormVisible.value = true
  nextTick(() => {
    if (pointsItemFormRef.value) {
      pointsItemFormRef.value.clearValidate()
    }
  })
}

// 打开编辑对话框
const handleEdit = (row) => {
  dialogStatus.value = 'update'
  Object.assign(pointsItemForm, { ...row })
  dialogFormVisible.value = true
  nextTick(() => {
    if (pointsItemFormRef.value) {
      pointsItemFormRef.value.clearValidate()
    }
  })
}

// 提交表单
const submitForm = () => {
  if (!pointsItemFormRef.value) return
  
  pointsItemFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await savePointsMallItem(pointsItemForm)
        ElMessage.success(dialogStatus.value === 'create' ? '创建成功' : '更新成功')
        dialogFormVisible.value = false
        getList()
      } catch (error) {
        console.error('保存积分商品失败:', error)
        ElMessage.error('操作失败')
      }
    }
  })
}

// 处理删除
const handleDelete = (row) => {
  ElMessageBox.confirm(
    '确定要删除该积分商品吗？删除后无法恢复。',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deletePointsMallItem(row.id)
      ElMessage.success('删除成功')
      getList()
    } catch (error) {
      console.error('删除积分商品失败:', error)
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

// 处理状态切换
const handleToggleStatus = (row) => {
  const newStatus = row.status === 1 ? 0 : 1
  const statusText = newStatus === 1 ? '上架' : '下架'
  
  ElMessageBox.confirm(
    `确定要${statusText}该积分商品吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await updatePointsMallItemStatus(row.id, newStatus)
      ElMessage.success(`${statusText}成功`)
      getList()
    } catch (error) {
      console.error('更新积分商品状态失败:', error)
      ElMessage.error(`${statusText}失败`)
    }
  }).catch(() => {})
}

onMounted(() => {
  getList()
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

.filter-container {
  margin-bottom: 20px;
}

.avatar-uploader {
  :deep(.el-upload) {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: var(--el-transition-duration-fast);

    &:hover {
      border-color: var(--el-color-primary);
    }
  }
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