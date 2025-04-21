<template>
  <div class="app-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>优惠券管理</span>
          <el-button type="primary" size="small" @click="handleAdd">新增优惠券</el-button>
        </div>
      </template>
      
      <div class="filter-container">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="优惠券名称">
            <el-input v-model="searchForm.name" placeholder="请输入优惠券名称" clearable></el-input>
          </el-form-item>
          <el-form-item label="优惠券类型">
            <el-select v-model="searchForm.type" placeholder="请选择类型" clearable>
              <el-option label="满减券" value="fullReduction"></el-option>
              <el-option label="折扣券" value="discount"></el-option>
              <el-option label="无门槛券" value="noThreshold"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
              <el-option label="未开始" value="upcoming"></el-option>
              <el-option label="进行中" value="ongoing"></el-option>
              <el-option label="已结束" value="expired"></el-option>
              <el-option label="已停用" value="disabled"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <el-table :data="couponList" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="name" label="优惠券名称" min-width="180"></el-table-column>
        <el-table-column prop="type" label="类型" width="100">
          <template #default="scope">
            <el-tag :type="getTypeTagType(scope.row.type)">{{ getTypeTagText(scope.row.type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="优惠内容" width="180">
          <template #default="scope">
            <span v-if="scope.row.type === 'fullReduction'">
              满{{ scope.row.fullAmount }}减{{ scope.row.reduceAmount }}
            </span>
            <span v-else-if="scope.row.type === 'discount'">
              {{ scope.row.discount }}折
            </span>
            <span v-else-if="scope.row.type === 'noThreshold'">
              无门槛减{{ scope.row.reduceAmount }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="有效期" width="280">
          <template #default="scope">
            {{ scope.row.startTime }} 至 {{ scope.row.endTime }}
          </template>
        </el-table-column>
        <el-table-column prop="totalCount" label="发放数量" width="100"></el-table-column>
        <el-table-column prop="usedCount" label="已使用" width="100"></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusTagType(scope.row.status)">{{ getStatusTagText(scope.row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="success" @click="handleIssue(scope.row)" v-if="scope.row.status !== 'disabled' && scope.row.status !== 'expired'">发放</el-button>
            <el-button size="small" type="danger" @click="handleDisable(scope.row)" v-if="scope.row.status !== 'disabled' && scope.row.status !== 'expired'">停用</el-button>
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
    
    <!-- 优惠券表单对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px">
      <el-form :model="couponForm" label-width="100px">
        <el-form-item label="优惠券名称">
          <el-input v-model="couponForm.name" placeholder="请输入优惠券名称"></el-input>
        </el-form-item>
        <el-form-item label="优惠券类型">
          <el-select v-model="couponForm.type" placeholder="请选择优惠券类型" style="width: 100%">
            <el-option label="满减券" value="fullReduction"></el-option>
            <el-option label="折扣券" value="discount"></el-option>
            <el-option label="无门槛券" value="noThreshold"></el-option>
          </el-select>
        </el-form-item>
        
        <template v-if="couponForm.type === 'fullReduction'">
          <el-form-item label="满足金额">
            <el-input-number v-model="couponForm.fullAmount" :min="0" :precision="2" :step="10"></el-input-number>
          </el-form-item>
          <el-form-item label="减免金额">
            <el-input-number v-model="couponForm.reduceAmount" :min="0" :precision="2" :step="1"></el-input-number>
          </el-form-item>
        </template>
        
        <template v-if="couponForm.type === 'discount'">
          <el-form-item label="折扣">
            <el-input-number v-model="couponForm.discount" :min="0" :max="10" :precision="1" :step="0.1"></el-input-number>
            <span style="margin-left: 10px; color: #909399;">0-10之间，例如8.5代表85折</span>
          </el-form-item>
        </template>
        
        <template v-if="couponForm.type === 'noThreshold'">
          <el-form-item label="减免金额">
            <el-input-number v-model="couponForm.reduceAmount" :min="0" :precision="2" :step="1"></el-input-number>
          </el-form-item>
        </template>
        
        <el-form-item label="有效期">
          <el-date-picker
            v-model="couponForm.validityPeriod"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 100%"
          ></el-date-picker>
        </el-form-item>
        
        <el-form-item label="发放总量">
          <el-input-number v-model="couponForm.totalCount" :min="1" :step="100"></el-input-number>
          <span style="margin-left: 10px; color: #909399;">0表示不限量</span>
        </el-form-item>
        
        <el-form-item label="每人限领">
          <el-input-number v-model="couponForm.perLimit" :min="1" :step="1"></el-input-number>
          <span style="margin-left: 10px; color: #909399;">0表示不限制</span>
        </el-form-item>
        
        <el-form-item label="适用商品">
          <el-radio-group v-model="couponForm.applicableScope">
            <el-radio label="all">全场通用</el-radio>
            <el-radio label="category">指定分类</el-radio>
            <el-radio label="product">指定商品</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="使用说明">
          <el-input 
            v-model="couponForm.description" 
            type="textarea" 
            :rows="3" 
            placeholder="请输入优惠券使用说明"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 发放优惠券对话框 -->
    <el-dialog v-model="issueDialogVisible" title="发放优惠券" width="500px">
      <el-form :model="issueForm" label-width="100px">
        <el-form-item label="发放方式">
          <el-radio-group v-model="issueForm.issueType">
            <el-radio label="all">全部用户</el-radio>
            <el-radio label="new">新用户</el-radio>
            <el-radio label="level">会员等级</el-radio>
            <el-radio label="custom">指定用户</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="会员等级" v-if="issueForm.issueType === 'level'">
          <el-select v-model="issueForm.userLevel" placeholder="请选择会员等级" style="width: 100%">
            <el-option label="普通会员" value="1"></el-option>
            <el-option label="银卡会员" value="2"></el-option>
            <el-option label="金卡会员" value="3"></el-option>
            <el-option label="钻石会员" value="4"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="指定用户" v-if="issueForm.issueType === 'custom'">
          <el-input 
            v-model="issueForm.userIds" 
            type="textarea" 
            :rows="3" 
            placeholder="请输入用户ID，多个用户以英文逗号分隔"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="发放数量">
          <el-input-number v-model="issueForm.count" :min="1" :step="10"></el-input-number>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="issueDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleIssueSubmit" :loading="issueLoading">确定发放</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

// 加载状态
const loading = ref(false)
const issueLoading = ref(false)

// 搜索表单
const searchForm = reactive({
  name: '',
  type: '',
  status: ''
})

// 分页信息
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 100
})

// 优惠券列表
const couponList = ref([
  {
    id: 1,
    name: '新用户专享券',
    type: 'noThreshold',
    reduceAmount: 10,
    startTime: '2023-06-01 00:00:00',
    endTime: '2023-06-30 23:59:59',
    totalCount: 1000,
    usedCount: 215,
    status: 'ongoing'
  },
  {
    id: 2,
    name: '夏季促销满减券',
    type: 'fullReduction',
    fullAmount: 100,
    reduceAmount: 20,
    startTime: '2023-07-01 00:00:00',
    endTime: '2023-07-31 23:59:59',
    totalCount: 5000,
    usedCount: 0,
    status: 'upcoming'
  },
  {
    id: 3,
    name: '会员专享折扣券',
    type: 'discount',
    discount: 8.5,
    startTime: '2023-05-01 00:00:00',
    endTime: '2023-05-31 23:59:59',
    totalCount: 2000,
    usedCount: 1568,
    status: 'expired'
  },
  {
    id: 4,
    name: '618大促满减券',
    type: 'fullReduction',
    fullAmount: 300,
    reduceAmount: 50,
    startTime: '2023-06-10 00:00:00',
    endTime: '2023-06-20 23:59:59',
    totalCount: 10000,
    usedCount: 3567,
    status: 'disabled'
  }
])

// 对话框相关
const dialogVisible = ref(false)
const dialogTitle = ref('新增优惠券')
const couponForm = reactive({
  id: null,
  name: '',
  type: 'fullReduction',
  fullAmount: 100,
  reduceAmount: 10,
  discount: 9,
  validityPeriod: [],
  totalCount: 1000,
  perLimit: 1,
  applicableScope: 'all',
  description: ''
})

// 发放对话框相关
const issueDialogVisible = ref(false)
const currentCoupon = ref(null)
const issueForm = reactive({
  issueType: 'all',
  userLevel: '',
  userIds: '',
  count: 100
})

// 获取优惠券类型标签类型
const getTypeTagType = (type) => {
  const types = {
    'fullReduction': 'primary',
    'discount': 'success',
    'noThreshold': 'warning'
  }
  return types[type] || 'info'
}

// 获取优惠券类型标签文本
const getTypeTagText = (type) => {
  const texts = {
    'fullReduction': '满减券',
    'discount': '折扣券',
    'noThreshold': '无门槛券'
  }
  return texts[type] || '未知'
}

// 获取优惠券状态标签类型
const getStatusTagType = (status) => {
  const types = {
    'upcoming': 'info',
    'ongoing': 'success',
    'expired': 'default',
    'disabled': 'danger'
  }
  return types[status] || 'info'
}

// 获取优惠券状态标签文本
const getStatusTagText = (status) => {
  const texts = {
    'upcoming': '未开始',
    'ongoing': '进行中',
    'expired': '已结束',
    'disabled': '已停用'
  }
  return texts[status] || '未知'
}

// 加载数据
const fetchCouponList = () => {
  loading.value = true
  // 模拟API请求
  setTimeout(() => {
    loading.value = false
  }, 500)
}

// 搜索
const handleSearch = () => {
  pagination.currentPage = 1
  fetchCouponList()
}

// 重置搜索
const resetSearch = () => {
  searchForm.name = ''
  searchForm.type = ''
  searchForm.status = ''
  handleSearch()
}

// 新增优惠券
const handleAdd = () => {
  dialogTitle.value = '新增优惠券'
  couponForm.id = null
  couponForm.name = ''
  couponForm.type = 'fullReduction'
  couponForm.fullAmount = 100
  couponForm.reduceAmount = 10
  couponForm.discount = 9
  couponForm.validityPeriod = []
  couponForm.totalCount = 1000
  couponForm.perLimit = 1
  couponForm.applicableScope = 'all'
  couponForm.description = ''
  dialogVisible.value = true
}

// 编辑优惠券
const handleEdit = (row) => {
  dialogTitle.value = '编辑优惠券'
  couponForm.id = row.id
  couponForm.name = row.name
  couponForm.type = row.type
  couponForm.fullAmount = row.fullAmount || 0
  couponForm.reduceAmount = row.reduceAmount || 0
  couponForm.discount = row.discount || 0
  couponForm.validityPeriod = [row.startTime, row.endTime]
  couponForm.totalCount = row.totalCount
  couponForm.perLimit = row.perLimit || 1
  couponForm.applicableScope = row.applicableScope || 'all'
  couponForm.description = row.description || ''
  dialogVisible.value = true
}

// 提交优惠券表单
const handleSubmit = () => {
  // 表单验证逻辑
  if (!couponForm.name) {
    alert('请输入优惠券名称')
    return
  }
  
  if (!couponForm.validityPeriod || couponForm.validityPeriod.length !== 2) {
    alert('请选择有效期')
    return
  }
  
  // 模拟API请求
  console.log('提交优惠券', couponForm)
  dialogVisible.value = false
}

// 停用优惠券
const handleDisable = (row) => {
  console.log('停用优惠券', row)
  // 实际项目中应该调用API
  row.status = 'disabled'
}

// 发放优惠券
const handleIssue = (row) => {
  currentCoupon.value = row
  issueForm.issueType = 'all'
  issueForm.userLevel = ''
  issueForm.userIds = ''
  issueForm.count = 100
  issueDialogVisible.value = true
}

// 提交发放
const handleIssueSubmit = () => {
  if (issueForm.issueType === 'level' && !issueForm.userLevel) {
    alert('请选择会员等级')
    return
  }
  
  if (issueForm.issueType === 'custom' && !issueForm.userIds) {
    alert('请输入用户ID')
    return
  }
  
  issueLoading.value = true
  
  // 模拟API请求
  setTimeout(() => {
    console.log('发放优惠券', {
      couponId: currentCoupon.value.id,
      ...issueForm
    })
    issueLoading.value = false
    issueDialogVisible.value = false
  }, 500)
}

// 分页大小变化
const handleSizeChange = (size) => {
  pagination.pageSize = size
  fetchCouponList()
}

// 页数变化
const handleCurrentChange = (page) => {
  pagination.currentPage = page
  fetchCouponList()
}

// 初始化
fetchCouponList()
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.filter-container {
  margin-bottom: 20px;
}
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style> 