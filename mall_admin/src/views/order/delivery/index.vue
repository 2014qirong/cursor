<template>
  <!-- 页面容器 -->
  <div class="app-container">
    <!-- 卡片组件 -->
    <el-card class="box-card">
      <!-- 卡片头部 -->
      <template #header>
        <div class="card-header">
          <span>发货管理</span>
        </div>
      </template>
      
      <!-- 搜索表单 -->
      <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="68px">
        <el-form-item label="订单号" prop="orderNo">
          <el-input v-model="queryParams.orderNo" placeholder="请输入订单号" clearable style="width: 240px" />
        </el-form-item>
        <el-form-item label="收货人" prop="receiverName">
          <el-input v-model="queryParams.receiverName" placeholder="请输入收货人" clearable style="width: 240px" />
        </el-form-item>
        <el-form-item label="发货状态" prop="status">
          <el-select v-model="queryParams.status" placeholder="请选择发货状态" clearable style="width: 240px">
            <el-option v-for="dict in statusOptions" :key="dict.value" :label="dict.label" :value="dict.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="下单时间">
          <el-date-picker v-model="dateRange" style="width: 240px" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期"></el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
          <el-button icon="Refresh" @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 操作按钮 -->
      <el-row :gutter="10" class="mb8">
        <el-col :span="1.5">
          <el-button type="primary" plain icon="Plus" @click="handleBatchDelivery">批量发货</el-button>
        </el-col>
        <el-col :span="1.5">
          <el-button type="warning" plain icon="Download" @click="handleExport">导出</el-button>
        </el-col>
        <right-toolbar v-model:showSearch="showSearch"></right-toolbar>
      </el-row>

      <!-- 数据表格 -->
      <el-table v-loading="loading" :data="deliveryList" border>
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column label="订单号" align="center" prop="orderNo" />
        <el-table-column label="收货人" align="center" prop="receiverName" />
        <el-table-column label="收货地址" align="center" prop="receiverAddress" :show-overflow-tooltip="true" />
        <el-table-column label="联系电话" align="center" prop="receiverPhone" />
        <el-table-column label="订单金额" align="center" prop="orderAmount" sortable />
        <el-table-column label="下单时间" align="center" prop="createTime" width="160" sortable />
        <el-table-column label="发货状态" align="center" prop="status">
          <template #default="scope">
            <el-tag :type="scope.row.status === '0' ? 'danger' : scope.row.status === '1' ? 'success' : 'info'">
              {{ statusFormatter(scope.row) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="200">
          <template #default="scope">
            <el-button v-if="scope.row.status === '0'" size="small" type="success" @click="handleDelivery(scope.row)">发货</el-button>
            <el-button size="small" type="primary" @click="handleDetail(scope.row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页组件 -->
      <div class="pagination-container">
        <el-pagination
          background
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          v-model:current-page="queryParams.pageNum"
          v-model:page-size="queryParams.pageSize"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
// 引入组件
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'

// 路由对象
const router = useRouter()

// 显示搜索条件
const showSearch = ref(true)
// 加载状态
const loading = ref(false)
// 总记录数
const total = ref(0)
// 日期范围
const dateRange = ref([])
// 查询参数
const queryParams = reactive({
  pageNum: 1,
  pageSize: 10,
  orderNo: '',
  receiverName: '',
  status: ''
})

// 发货状态选项
const statusOptions = [
  { value: '0', label: '待发货' },
  { value: '1', label: '已发货' },
  { value: '2', label: '已签收' }
]

// 发货列表数据
const deliveryList = ref([
  {
    id: 1,
    orderNo: 'ORDER2023042100001',
    receiverName: '张三',
    receiverAddress: '广东省广州市天河区体育西路123号',
    receiverPhone: '13800138001',
    orderAmount: 299.99,
    createTime: '2023-04-21 10:23:45',
    status: '0'
  },
  {
    id: 2,
    orderNo: 'ORDER2023042000002',
    receiverName: '李四',
    receiverAddress: '广东省深圳市南山区科技园456号',
    receiverPhone: '13800138002',
    orderAmount: 99.50,
    createTime: '2023-04-20 15:34:21',
    status: '1'
  },
  {
    id: 3,
    orderNo: 'ORDER2023041900003',
    receiverName: '王五',
    receiverAddress: '广东省东莞市长安镇新安路789号',
    receiverPhone: '13800138003',
    orderAmount: 158.80,
    createTime: '2023-04-19 09:12:33',
    status: '2'
  }
])

// 状态格式化
const statusFormatter = (row) => {
  if (row.status === '0') {
    return '待发货'
  } else if (row.status === '1') {
    return '已发货'
  } else if (row.status === '2') {
    return '已签收'
  }
  return '未知状态'
}

// 查询方法
const handleQuery = () => {
  // 模拟查询操作
  loading.value = true
  setTimeout(() => {
    loading.value = false
    ElMessage.success('查询成功')
  }, 500)
}

// 重置查询
const resetQuery = () => {
  dateRange.value = []
  Object.keys(queryParams).forEach(key => {
    if (key !== 'pageNum' && key !== 'pageSize') {
      queryParams[key] = ''
    }
  })
  handleQuery()
}

// 分页大小变化
const handleSizeChange = (size) => {
  queryParams.pageSize = size
  handleQuery()
}

// 页码变化
const handleCurrentChange = (page) => {
  queryParams.pageNum = page
  handleQuery()
}

// 详情
const handleDetail = (row) => {
  router.push(`/order/detail/${row.id}`)
}

// 发货
const handleDelivery = (row) => {
  ElMessageBox.confirm(`确认要对订单 ${row.orderNo} 执行发货操作吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 模拟发货操作
    setTimeout(() => {
      row.status = '1'
      ElMessage.success('发货成功')
    }, 500)
  }).catch(() => {})
}

// 批量发货
const handleBatchDelivery = () => {
  ElMessage.info('批量发货功能开发中...')
}

// 导出
const handleExport = () => {
  ElMessage.info('导出功能开发中...')
}

// 页面加载时执行
onMounted(() => {
  // 实际项目中应从后端获取数据
  total.value = deliveryList.value.length
})
</script>

<style scoped>
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
.mb8 {
  margin-bottom: 8px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style> 