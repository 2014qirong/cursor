<template>
  <div class="app-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>退款/售后管理</span>
        </div>
      </template>
      
      <div class="filter-container">
        <el-input
          v-model="listQuery.orderNo"
          placeholder="订单编号"
          style="width: 200px;"
          class="filter-item"
          clearable
        />
        <el-select
          v-model="listQuery.status"
          placeholder="退款状态"
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
        <el-button type="primary" icon="Search" @click="handleFilter">搜索</el-button>
        <el-button icon="Refresh" @click="resetFilter">重置</el-button>
      </div>
      
      <el-table
        v-loading="listLoading"
        :data="list"
        border
        fit
        highlight-current-row
        style="width: 100%"
      >
        <el-table-column label="退款单号" align="center" width="180">
          <template #default="scope">
            <span>{{ scope.row.refundNo }}</span>
          </template>
        </el-table-column>
        <el-table-column label="关联订单" align="center" width="180">
          <template #default="scope">
            <router-link :to="'/order/detail?id='+scope.row.orderId" class="link-type">
              {{ scope.row.orderNo }}
            </router-link>
          </template>
        </el-table-column>
        <el-table-column label="申请时间" width="160" align="center">
          <template #default="scope">
            <span>{{ scope.row.applyTime }}</span>
          </template>
        </el-table-column>
        <el-table-column label="申请金额" width="110" align="center">
          <template #default="scope">
            <span>¥{{ scope.row.amount }}</span>
          </template>
        </el-table-column>
        <el-table-column label="退款类型" width="120" align="center">
          <template #default="scope">
            <span>{{ scope.row.type }}</span>
          </template>
        </el-table-column>
        <el-table-column label="退款原因" min-width="200" align="center">
          <template #default="scope">
            <span>{{ scope.row.reason }}</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="230" class-name="small-padding fixed-width">
          <template #default="scope">
            <el-button
              v-if="scope.row.status === '待处理'"
              type="primary"
              size="small"
              @click="handleProcess(scope.row)"
            >
              处理
            </el-button>
            <el-button
              v-if="scope.row.status === '待处理'"
              type="success"
              size="small"
              @click="handleApprove(scope.row)"
            >
              通过
            </el-button>
            <el-button
              v-if="scope.row.status === '待处理'"
              type="danger"
              size="small"
              @click="handleReject(scope.row)"
            >
              拒绝
            </el-button>
            <el-button size="small" type="info" @click="handleDetail(scope.row)">
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <pagination
        v-show="total > 0"
        :total="total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.limit"
        @pagination="fetchData"
      />
    </el-card>
    
    <!-- 处理退款对话框 -->
    <el-dialog v-model="dialogVisible" title="处理退款申请" width="500px">
      <el-form :model="refundForm" label-width="100px">
        <el-form-item label="退款金额">
          <el-input-number v-model="refundForm.amount" :min="0" :precision="2" :step="0.01" />
        </el-form-item>
        <el-form-item label="处理意见">
          <el-input type="textarea" v-model="refundForm.remark" :rows="3" placeholder="请输入处理意见" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="submitRefund">确 定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import Pagination from '@/components/common/Pagination.vue'
import { ElMessage } from 'element-plus'

// 列表数据
const list = ref([
  {
    refundNo: 'RF202305120001',
    orderId: 1,
    orderNo: 'OR202305120001',
    applyTime: '2023-05-12 10:23:45',
    amount: 99.99,
    type: '仅退款',
    reason: '不想要了',
    status: '待处理'
  },
  {
    refundNo: 'RF202305110002',
    orderId: 2,
    orderNo: 'OR202305110023',
    applyTime: '2023-05-11 16:44:12',
    amount: 299.00,
    type: '退货退款',
    reason: '商品质量问题',
    status: '已通过'
  },
  {
    refundNo: 'RF202305100003',
    orderId: 3,
    orderNo: 'OR202305100045',
    applyTime: '2023-05-10 09:12:34',
    amount: 59.90,
    type: '仅退款',
    reason: '重复购买',
    status: '已拒绝'
  }
])
const total = ref(3)
const listLoading = ref(false)
const listQuery = reactive({
  page: 1,
  limit: 10,
  orderNo: '',
  status: ''
})
const statusOptions = [
  { value: '待处理', label: '待处理' },
  { value: '已通过', label: '已通过' },
  { value: '已拒绝', label: '已拒绝' },
  { value: '已完成', label: '已完成' }
]
const dateRange = ref([])
const dialogVisible = ref(false)
const refundForm = reactive({
  id: null,
  amount: 0,
  remark: ''
})

const fetchData = () => {
  listLoading.value = true
  // 模拟API请求
  setTimeout(() => {
    listLoading.value = false
  }, 500)
}

const handleFilter = () => {
  listQuery.page = 1
  fetchData()
}

const resetFilter = () => {
  listQuery.orderNo = ''
  listQuery.status = ''
  dateRange.value = []
  fetchData()
}

const handleProcess = (row) => {
  refundForm.id = row.refundNo
  refundForm.amount = row.amount
  refundForm.remark = ''
  dialogVisible.value = true
}

const handleApprove = (row) => {
  // 直接通过退款
  ElMessage.success(`已通过退款申请: ${row.refundNo}`)
  fetchData()
}

const handleReject = (row) => {
  // 拒绝退款
  ElMessage.warning(`已拒绝退款申请: ${row.refundNo}`)
  fetchData()
}

const handleDetail = (row) => {
  // 查看退款详情
  ElMessage.info(`查看退款详情: ${row.refundNo}`)
}

const submitRefund = () => {
  // 提交退款处理
  ElMessage.success(`已处理退款申请: ${refundForm.id}`)
  dialogVisible.value = false
  fetchData()
}

// 状态标签类型
const getStatusType = (status) => {
  const map = {
    '待处理': 'warning',
    '已通过': 'success',
    '已拒绝': 'danger',
    '已完成': 'info'
  }
  return map[status] || 'info'
}

onMounted(() => {
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

.link-type {
  color: #409EFF;
  text-decoration: none;
}

.link-type:hover {
  text-decoration: underline;
}
</style> 