<template>
  <div class="app-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>库存管理</span>
          <el-button type="primary" size="small" @click="handleBatchUpdate">批量修改</el-button>
        </div>
      </template>
      
      <div class="filter-container">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="商品名称">
            <el-input v-model="searchForm.name" placeholder="请输入商品名称" clearable></el-input>
          </el-form-item>
          <el-form-item label="库存状态">
            <el-select v-model="searchForm.stockStatus" placeholder="请选择库存状态" clearable>
              <el-option label="充足" value="sufficient"></el-option>
              <el-option label="不足" value="insufficient"></el-option>
              <el-option label="告急" value="urgent"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <el-table :data="stockList" style="width: 100%" v-loading="loading" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="name" label="商品名称" min-width="200"></el-table-column>
        <el-table-column prop="sku" label="SKU" width="120"></el-table-column>
        <el-table-column prop="specs" label="规格" width="120">
          <template #default="scope">
            <div>
              <div v-for="(value, key) in scope.row.specs" :key="key">{{ key }}: {{ value }}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="stock" label="库存数量" width="100">
          <template #default="scope">
            <el-input-number 
              v-model="scope.row.stock" 
              :min="0" 
              :step="1" 
              size="small"
              @change="(value) => handleStockChange(scope.row, value)"
            ></el-input-number>
          </template>
        </el-table-column>
        <el-table-column prop="alertThreshold" label="预警阈值" width="100"></el-table-column>
        <el-table-column prop="stockStatus" label="库存状态" width="100">
          <template #default="scope">
            <el-tag :type="getStockStatusType(scope.row)">
              {{ getStockStatusText(scope.row) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button size="small" @click="handleLogHistory(scope.row)">日志</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-container">
        <el-pagination
          background
          layout="total, sizes, prev, pager, next, jumper"
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        >
        </el-pagination>
      </div>
    </el-card>
    
    <!-- 批量修改对话框 -->
    <el-dialog v-model="batchDialogVisible" title="批量修改库存" width="500px">
      <el-form :model="batchForm" label-width="100px">
        <el-form-item label="修改方式">
          <el-radio-group v-model="batchForm.updateType">
            <el-radio :label="'increase'">增加</el-radio>
            <el-radio :label="'decrease'">减少</el-radio>
            <el-radio :label="'set'">设置为</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="数量">
          <el-input-number v-model="batchForm.value" :min="0" :step="1"></el-input-number>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="batchForm.remark" type="textarea" placeholder="请输入备注信息"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="batchDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleBatchConfirm">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const loading = ref(false)
const selectedItems = ref([])

// 搜索表单
const searchForm = reactive({
  name: '',
  stockStatus: ''
})

// 分页信息
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 100
})

// 库存列表
const stockList = ref([
  {
    id: 1,
    name: '智能电视 55英寸',
    sku: 'TV-55-001',
    specs: { '尺寸': '55英寸', '颜色': '黑色' },
    stock: 100,
    alertThreshold: 20
  },
  {
    id: 2,
    name: '智能电视 55英寸',
    sku: 'TV-55-002',
    specs: { '尺寸': '55英寸', '颜色': '银色' },
    stock: 15,
    alertThreshold: 20
  },
  {
    id: 3,
    name: '男士休闲裤',
    sku: 'MP-001-XL',
    specs: { '尺寸': 'XL', '颜色': '黑色' },
    stock: 5,
    alertThreshold: 10
  },
  {
    id: 4,
    name: '男士休闲裤',
    sku: 'MP-001-L',
    specs: { '尺寸': 'L', '颜色': '黑色' },
    stock: 0,
    alertThreshold: 10
  },
  {
    id: 5,
    name: '女士连衣裙',
    sku: 'WD-001-M',
    specs: { '尺寸': 'M', '颜色': '红色' },
    stock: 50,
    alertThreshold: 10
  }
])

// 批量修改相关
const batchDialogVisible = ref(false)
const batchForm = reactive({
  updateType: 'increase',
  value: 0,
  remark: ''
})

// 获取库存状态类型
const getStockStatusType = (row) => {
  if (row.stock === 0) return 'danger'
  if (row.stock <= row.alertThreshold) return 'warning'
  return 'success'
}

// 获取库存状态文本
const getStockStatusText = (row) => {
  if (row.stock === 0) return '无库存'
  if (row.stock <= row.alertThreshold) return '不足'
  return '充足'
}

// 加载数据
const fetchStockList = () => {
  loading.value = true
  // 这里应该是接口请求
  setTimeout(() => {
    loading.value = false
  }, 500)
}

// 搜索
const handleSearch = () => {
  pagination.currentPage = 1
  fetchStockList()
}

// 重置搜索
const resetSearch = () => {
  searchForm.name = ''
  searchForm.stockStatus = ''
  handleSearch()
}

// 库存变更
const handleStockChange = (row, value) => {
  console.log('库存变更', row, value)
}

// 多选变化
const handleSelectionChange = (selection) => {
  selectedItems.value = selection
}

// 批量修改
const handleBatchUpdate = () => {
  if (selectedItems.value.length === 0) {
    alert('请至少选择一项')
    return
  }
  batchForm.updateType = 'increase'
  batchForm.value = 0
  batchForm.remark = ''
  batchDialogVisible.value = true
}

// 批量修改确认
const handleBatchConfirm = () => {
  console.log('批量修改', {
    items: selectedItems.value,
    updateType: batchForm.updateType,
    value: batchForm.value,
    remark: batchForm.remark
  })
  batchDialogVisible.value = false
}

// 查看日志
const handleLogHistory = (row) => {
  console.log('查看库存日志', row)
}

// 分页大小变化
const handleSizeChange = (size) => {
  pagination.pageSize = size
  fetchStockList()
}

// 页数变化
const handleCurrentChange = (page) => {
  pagination.currentPage = page
  fetchStockList()
}

// 初始化
fetchStockList()
</script>

<style scoped>
.filter-container {
  margin-bottom: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style> 