<template>
  <div class="app-container">
    <el-card>
      <div class="filter-container">
        <el-form :inline="true" :model="listQuery" @keyup.enter="handleFilter">
          <el-form-item label="订单号">
            <el-input v-model="listQuery.orderSn" placeholder="请输入订单号" clearable />
          </el-form-item>
          <el-form-item label="订单状态">
            <el-select v-model="listQuery.status" placeholder="全部状态" clearable>
              <el-option v-for="item in statusOptions" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="下单时间">
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              value-format="YYYY-MM-DD"
            />
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
        @sort-change="handleSortChange"
      >
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column label="订单号" prop="orderSn" min-width="180" />
        <el-table-column label="用户" prop="userName" min-width="100" />
        <el-table-column label="订单金额" prop="totalAmount" min-width="120" sortable="custom">
          <template #default="scope">
            <span>￥{{ scope.row.totalAmount }}</span>
          </template>
        </el-table-column>
        <el-table-column label="订单状态" prop="status" min-width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="支付方式" prop="payType" min-width="120">
          <template #default="scope">
            {{ getPayTypeText(scope.row.payType) }}
          </template>
        </el-table-column>
        <el-table-column label="创建时间" prop="createTime" min-width="180" sortable="custom" />
        <el-table-column label="操作" min-width="220" fixed="right">
          <template #default="scope">
            <el-button size="small" type="primary" link @click="handleDetail(scope.row)">查看</el-button>
            <el-button 
              v-if="scope.row.status === 1" 
              size="small" 
              type="success" 
              link 
              @click="handleShip(scope.row)"
            >
              发货
            </el-button>
            <el-button 
              v-if="scope.row.status === 0" 
              size="small" 
              type="danger" 
              link 
              @click="handleCancel(scope.row)"
            >
              取消
            </el-button>
            <el-button size="small" type="warning" link @click="handlePrint(scope.row)">打印</el-button>
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
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { getOrderList, updateOrderStatus } from '@/api/order'
import Pagination from '@/components/common/Pagination.vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()

// 列表数据
const list = ref([])
const total = ref(0)
const listLoading = ref(false)
const dateRange = ref([])

// 查询参数
const listQuery = reactive({
  page: 1,
  limit: 20,
  orderSn: '',
  status: '',
  startDate: '',
  endDate: '',
  sort: ''
})

// 订单状态选项
const statusOptions = [
  { label: '待付款', value: 0 },
  { label: '待发货', value: 1 },
  { label: '已发货', value: 2 },
  { label: '已完成', value: 3 },
  { label: '已关闭', value: 4 },
  { label: '已取消', value: 5 }
]

// 监听日期范围变化
watch(dateRange, (val) => {
  if (val) {
    listQuery.startDate = val[0]
    listQuery.endDate = val[1]
  } else {
    listQuery.startDate = ''
    listQuery.endDate = ''
  }
})

// 获取状态对应的类型
const getStatusType = (status) => {
  const map = {
    0: 'info',
    1: 'warning',
    2: 'primary',
    3: 'success',
    4: 'danger',
    5: 'danger'
  }
  return map[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const map = {
    0: '待付款',
    1: '待发货',
    2: '已发货',
    3: '已完成',
    4: '已关闭',
    5: '已取消'
  }
  return map[status] || '未知状态'
}

// 获取支付方式文本
const getPayTypeText = (type) => {
  const map = {
    1: '微信支付',
    2: '支付宝',
    3: '余额支付',
    4: '货到付款'
  }
  return map[type] || '未知'
}

// 获取订单列表
const getList = async () => {
  listLoading.value = true
  try {
    const response = await getOrderList(listQuery)
    // 检查响应结构，避免undefined错误
    if (response && response.data) {
      // 如果是期望的数据结构
      if (response.data.items) {
        list.value = response.data.items
        total.value = response.data.total || 0
      } else if (Array.isArray(response.data)) {
        // 如果直接返回数组
        list.value = response.data
        total.value = response.data.length
      } else {
        // 其他情况
        list.value = []
        total.value = 0
        console.warn('订单数据结构异常:', response)
      }
    } else {
      list.value = []
      total.value = 0
      console.warn('返回数据为空')
    }
  } catch (error) {
    console.error('获取订单列表失败:', error)
    list.value = []
    total.value = 0
    ElMessage.error('获取订单列表失败')
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
  Object.assign(listQuery, {
    page: 1,
    orderSn: '',
    status: '',
    startDate: '',
    endDate: '',
    sort: ''
  })
  dateRange.value = []
  getList()
}

// 处理排序变化
const handleSortChange = (column) => {
  if (column.prop && column.order) {
    listQuery.sort = column.prop + (column.order === 'ascending' ? '+' : '-')
  } else {
    listQuery.sort = ''
  }
  getList()
}

// 查看订单详情
const handleDetail = (row) => {
  router.push({ path: `/order/detail/${row.id}` })
}

// 处理发货
const handleShip = (row) => {
  router.push({ path: `/order/delivery`, query: { id: row.id } })
}

// 处理取消订单
const handleCancel = (row) => {
  ElMessageBox.confirm(
    '确定要取消该订单吗？取消后无法恢复。',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await updateOrderStatus(row.id, 5, '管理员取消')
      ElMessage.success('订单已取消')
      getList()
    } catch (error) {
      console.error('取消订单失败:', error)
      ElMessage.error('取消订单失败')
    }
  }).catch(() => {
    // 取消操作，不做处理
  })
}

// 处理打印订单
const handlePrint = (row) => {
  ElMessage.info('打印订单功能开发中...')
}

onMounted(() => {
  getList()
})
</script>

<style lang="scss" scoped>
.app-container {
  padding: 20px;
}

.filter-container {
  padding-bottom: 20px;
}
</style> 