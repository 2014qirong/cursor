<template>
  <div class="app-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>限时折扣活动</span>
          <el-button type="primary" @click="handleCreate">
            <el-icon><Plus /></el-icon>新增活动
          </el-button>
        </div>
      </template>
      
      <div class="filter-container">
        <el-input
          v-model="listQuery.title"
          placeholder="活动名称"
          style="width: 200px;"
          class="filter-item"
          clearable
        />
        <el-select
          v-model="listQuery.status"
          placeholder="活动状态"
          clearable
          class="filter-item"
          style="width: 130px"
        >
          <el-option v-for="item in statusOptions" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          class="filter-item"
          style="width: 340px"
        />
        <el-button type="primary" @click="handleFilter">
          <el-icon><Search /></el-icon>搜索
        </el-button>
        <el-button @click="resetFilter">
          <el-icon><Refresh /></el-icon>重置
        </el-button>
      </div>
      
      <el-table
        v-loading="listLoading"
        :data="list"
        border
        fit
        highlight-current-row
        style="width: 100%"
      >
        <el-table-column label="ID" prop="id" align="center" width="80">
          <template #default="scope">
            <span>{{ scope.row.id }}</span>
          </template>
        </el-table-column>
        <el-table-column label="活动名称" min-width="180" align="center">
          <template #default="scope">
            <span>{{ scope.row.title }}</span>
          </template>
        </el-table-column>
        <el-table-column label="开始时间" width="160" align="center">
          <template #default="scope">
            <span>{{ scope.row.startTime }}</span>
          </template>
        </el-table-column>
        <el-table-column label="结束时间" width="160" align="center">
          <template #default="scope">
            <span>{{ scope.row.endTime }}</span>
          </template>
        </el-table-column>
        <el-table-column label="折扣力度" width="110" align="center">
          <template #default="scope">
            <span>{{ scope.row.discount }}折</span>
          </template>
        </el-table-column>
        <el-table-column label="商品数量" width="100" align="center">
          <template #default="scope">
            <span>{{ scope.row.productCount }}</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="250" class-name="small-padding fixed-width">
          <template #default="scope">
            <el-button
              size="small"
              type="primary"
              @click="handleUpdate(scope.row)"
            >
              编辑
            </el-button>
            <el-button
              size="small"
              type="success"
              @click="handleViewProducts(scope.row)"
            >
              查看商品
            </el-button>
            <el-button
              v-if="scope.row.status === '未开始'"
              size="small"
              type="danger"
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
        @pagination="fetchData"
      />
    </el-card>
    
    <!-- 活动表单对话框 -->
    <el-dialog :title="dialogStatus === 'create' ? '新增活动' : '编辑活动'" v-model="dialogFormVisible">
      <el-form
        ref="dataForm"
        :model="temp"
        label-position="left"
        label-width="100px"
        style="width: 400px; margin-left:50px;"
      >
        <el-form-item label="活动名称" prop="title">
          <el-input v-model="temp.title" />
        </el-form-item>
        <el-form-item label="活动时间">
          <el-date-picker
            v-model="temp.activityTime"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            style="width: 300px"
          />
        </el-form-item>
        <el-form-item label="折扣力度">
          <el-input-number v-model="temp.discount" :min="1" :max="9.9" :precision="1" :step="0.1" />
          <span class="discount-unit">折</span>
        </el-form-item>
        <el-form-item label="活动说明">
          <el-input type="textarea" v-model="temp.description" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="dialogStatus === 'create' ? createData() : updateData()">确 定</el-button>
        </div>
      </template>
    </el-dialog>
    
    <!-- 活动商品列表对话框 -->
    <el-dialog title="活动商品" v-model="dialogProductVisible" width="800px">
      <div class="filter-container" style="margin-bottom: 15px;">
        <el-button type="primary" @click="handleAddProducts">
          <el-icon><Plus /></el-icon>添加商品
        </el-button>
      </div>
      
      <el-table
        :data="productList"
        border
        fit
        highlight-current-row
        style="width: 100%"
      >
        <el-table-column label="商品ID" prop="id" align="center" width="80" />
        <el-table-column label="商品图片" width="100" align="center">
          <template #default="scope">
            <el-image 
              style="width: 60px; height: 60px"
              :src="scope.row.image"
              :preview-src-list="[scope.row.image]">
            </el-image>
          </template>
        </el-table-column>
        <el-table-column label="商品名称" min-width="180" align="center" prop="name" />
        <el-table-column label="原价" width="100" align="center">
          <template #default="scope">
            <span>¥{{ scope.row.price }}</span>
          </template>
        </el-table-column>
        <el-table-column label="折扣价" width="100" align="center">
          <template #default="scope">
            <span class="discount-price">¥{{ scope.row.discountPrice }}</span>
          </template>
        </el-table-column>
        <el-table-column label="库存" width="80" align="center" prop="stock" />
        <el-table-column label="操作" align="center" width="120">
          <template #default="scope">
            <el-button size="small" type="danger" @click="handleRemoveProduct(scope.row)">
              移除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, toRefs, onMounted } from 'vue'
import { Search, Plus, Refresh } from '@element-plus/icons-vue'
import Pagination from '@/components/common/Pagination.vue'

console.log('限时折扣组件加载中...')

const list = ref([
  {
    id: 1,
    title: '618电器促销',
    startTime: '2023-06-15 00:00:00',
    endTime: '2023-06-18 23:59:59',
    discount: 8.5,
    productCount: 28,
    status: '未开始'
  },
  {
    id: 2,
    title: '五一特惠',
    startTime: '2023-04-29 00:00:00',
    endTime: '2023-05-03 23:59:59',
    discount: 7.5,
    productCount: 56,
    status: '已结束'
  },
  {
    id: 3,
    title: '春季上新',
    startTime: '2023-03-01 00:00:00',
    endTime: '2023-03-15 23:59:59',
    discount: 9.0,
    productCount: 36,
    status: '已结束'
  }
])
const total = ref(3)
const listLoading = ref(false)
const listQuery = reactive({
  page: 1,
  limit: 10,
  title: '',
  status: ''
})
const statusOptions = ref([
  { value: '未开始', label: '未开始' },
  { value: '进行中', label: '进行中' },
  { value: '已结束', label: '已结束' }
])
const dateRange = ref([])
const dialogFormVisible = ref(false)
const dialogProductVisible = ref(false)
const dialogStatus = ref('')
const temp = reactive({
  id: undefined,
  title: '',
  activityTime: [],
  discount: 8.0,
  description: ''
})
const productList = ref([
  {
    id: 1,
    image: 'https://placeholder.pics/svg/100x100',
    name: 'iPhone 14 Pro 256GB 暗夜紫',
    price: 8999.00,
    discountPrice: 7649.15,
    stock: 100
  },
  {
    id: 2,
    image: 'https://placeholder.pics/svg/100x100',
    name: 'MacBook Pro 14" M2 Pro',
    price: 14999.00,
    discountPrice: 12749.15,
    stock: 50
  },
  {
    id: 3,
    image: 'https://placeholder.pics/svg/100x100',
    name: 'AirPods Pro 2',
    price: 1899.00,
    discountPrice: 1614.15,
    stock: 200
  }
])
const currentActivityId = ref(null)

// 获取状态对应的标签类型
const getStatusType = (status) => {
  switch (status) {
    case '未开始':
      return 'info'
    case '进行中':
      return 'success'
    case '已结束':
      return 'warning'
    default:
      return ''
  }
}

const fetchData = () => {
  console.log('获取限时折扣数据...')
  listLoading.value = true
  // 模拟API请求
  setTimeout(() => {
    listLoading.value = false
    console.log('数据加载完成')
  }, 500)
}

const resetTemp = () => {
  temp.id = undefined
  temp.title = ''
  temp.activityTime = []
  temp.discount = 8.0
  temp.description = ''
}

const handleFilter = () => {
  console.log('筛选查询', listQuery)
  listQuery.page = 1
  fetchData()
}

const resetFilter = () => {
  listQuery.title = ''
  listQuery.status = ''
  dateRange.value = []
  console.log('重置筛选条件')
  fetchData()
}

const handleCreate = () => {
  resetTemp()
  dialogStatus.value = 'create'
  dialogFormVisible.value = true
  console.log('打开创建对话框')
}

const createData = () => {
  // 创建新活动
  console.log('创建新活动', temp)
  dialogFormVisible.value = false
  fetchData()
}

const handleUpdate = (row) => {
  Object.assign(temp, row)
  temp.activityTime = [new Date(row.startTime), new Date(row.endTime)]
  dialogStatus.value = 'update'
  dialogFormVisible.value = true
  console.log('编辑活动', row.id)
}

const updateData = () => {
  // 更新活动
  console.log('更新活动', temp)
  dialogFormVisible.value = false
  fetchData()
}

const handleDelete = (row) => {
  // 删除活动
  console.log('删除活动', row.id)
}

const handleViewProducts = (row) => {
  currentActivityId.value = row.id
  dialogProductVisible.value = true
  console.log('查看活动商品', row.id)
  // 获取活动商品列表
}

const handleAddProducts = () => {
  // 添加商品到活动
  console.log('添加商品到活动', currentActivityId.value)
}

const handleRemoveProduct = (row) => {
  // 从活动中移除商品
  console.log('从活动中移除商品', row.id)
}

onMounted(() => {
  console.log('限时折扣组件已挂载')
  fetchData()
})
</script>

<style scoped>
.filter-container {
  padding-bottom: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.filter-item {
  margin-right: 10px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.discount-unit {
  margin-left: 10px;
}

.discount-price {
  color: #ff4500;
  font-weight: bold;
}
</style> 