<template>
  <div class="promotion-container">
    <!-- 搜索和操作栏 -->
    <el-card class="filter-container">
      <div class="filter-form">
        <el-form :inline="true" :model="searchForm" class="demo-form-inline">
          <el-form-item label="活动名称">
            <el-input v-model="searchForm.name" placeholder="请输入活动名称" clearable></el-input>
          </el-form-item>
          <el-form-item label="活动类型">
            <el-select v-model="searchForm.type" placeholder="请选择活动类型" clearable>
              <el-option label="满减活动" value="fullReduction"></el-option>
              <el-option label="折扣活动" value="discount"></el-option>
              <el-option label="限时秒杀" value="seckill"></el-option>
              <el-option label="满赠活动" value="gift"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="活动状态">
            <el-select v-model="searchForm.status" placeholder="请选择活动状态" clearable>
              <el-option label="进行中" value="ongoing"></el-option>
              <el-option label="即将开始" value="upcoming"></el-option>
              <el-option label="已结束" value="expired"></el-option>
              <el-option label="已取消" value="canceled"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      <div class="operation-container">
        <el-button type="primary" @click="openAddDialog">添加促销活动</el-button>
      </div>
    </el-card>

    <!-- 数据表格 -->
    <el-card class="table-container">
      <el-table 
        v-loading="loading" 
        :data="promotionList" 
        style="width: 100%"
        border
      >
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="name" label="活动名称" min-width="180"></el-table-column>
        <el-table-column label="活动类型" width="120">
          <template #default="scope">
            <el-tag v-if="scope.row.type === 'fullReduction'" type="success">满减活动</el-tag>
            <el-tag v-else-if="scope.row.type === 'discount'" type="warning">折扣活动</el-tag>
            <el-tag v-else-if="scope.row.type === 'seckill'" type="danger">限时秒杀</el-tag>
            <el-tag v-else-if="scope.row.type === 'gift'" type="info">满赠活动</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="活动规则" min-width="180">
          <template #default="scope">
            <div v-if="scope.row.type === 'fullReduction'">
              满{{ scope.row.rules.fullAmount }}元减{{ scope.row.rules.reduceAmount }}元
            </div>
            <div v-else-if="scope.row.type === 'discount'">
              打{{ scope.row.rules.discount }}折
            </div>
            <div v-else-if="scope.row.type === 'seckill'">
              秒杀价¥{{ scope.row.rules.seckillPrice }}，限购{{ scope.row.rules.limitCount }}件
            </div>
            <div v-else-if="scope.row.type === 'gift'">
              满{{ scope.row.rules.condition }}元赠送礼品
            </div>
          </template>
        </el-table-column>
        <el-table-column label="活动时间" min-width="180">
          <template #default="scope">
            {{ scope.row.startTime }} 至 {{ scope.row.endTime }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="scope">
            <el-tag v-if="scope.row.status === 'ongoing'" type="success">进行中</el-tag>
            <el-tag v-else-if="scope.row.status === 'upcoming'" type="warning">即将开始</el-tag>
            <el-tag v-else-if="scope.row.status === 'expired'" type="info">已结束</el-tag>
            <el-tag v-else-if="scope.row.status === 'canceled'" type="danger">已取消</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="text" size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button 
              type="text" 
              size="small" 
              :disabled="scope.row.status === 'ongoing'"
              @click="handleStart(scope.row)" 
              v-if="scope.row.status === 'upcoming'"
            >
              开始
            </el-button>
            <el-button 
              type="text" 
              size="small" 
              @click="handleStop(scope.row)" 
              v-if="scope.row.status === 'ongoing'"
            >
              停止
            </el-button>
            <el-button 
              type="text" 
              size="small" 
              class="delete-btn" 
              @click="handleDelete(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          background
          layout="total, sizes, prev, pager, next, jumper"
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        ></el-pagination>
      </div>
    </el-card>

    <!-- 添加/编辑促销活动对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogType === 'add' ? '添加促销活动' : '编辑促销活动'" width="700px">
      <el-form :model="promotionForm" ref="promotionFormRef" label-width="100px" :rules="rules">
        <el-form-item label="活动名称" prop="name">
          <el-input v-model="promotionForm.name" placeholder="请输入活动名称"></el-input>
        </el-form-item>
        
        <el-form-item label="活动类型" prop="type">
          <el-select v-model="promotionForm.type" placeholder="请选择活动类型" style="width: 100%">
            <el-option label="满减活动" value="fullReduction"></el-option>
            <el-option label="折扣活动" value="discount"></el-option>
            <el-option label="限时秒杀" value="seckill"></el-option>
            <el-option label="满赠活动" value="gift"></el-option>
          </el-select>
        </el-form-item>
        
        <!-- 满减活动规则表单项 -->
        <template v-if="promotionForm.type === 'fullReduction'">
          <el-form-item label="满足金额">
            <el-input-number v-model="promotionForm.rules.fullAmount" :min="0" :precision="2" :step="10"></el-input-number>
            <span style="margin-left: 10px">元</span>
          </el-form-item>
          <el-form-item label="减免金额">
            <el-input-number v-model="promotionForm.rules.reduceAmount" :min="0" :precision="2" :step="5"></el-input-number>
            <span style="margin-left: 10px">元</span>
          </el-form-item>
        </template>
        
        <!-- 折扣活动规则表单项 -->
        <template v-if="promotionForm.type === 'discount'">
          <el-form-item label="折扣力度">
            <el-input-number v-model="promotionForm.rules.discount" :min="0.1" :max="9.9" :precision="1" :step="0.5"></el-input-number>
            <span style="margin-left: 10px">折</span>
          </el-form-item>
        </template>
        
        <!-- 秒杀活动规则表单项 -->
        <template v-if="promotionForm.type === 'seckill'">
          <el-form-item label="秒杀价格">
            <el-input-number v-model="promotionForm.rules.seckillPrice" :min="0" :precision="2" :step="10"></el-input-number>
            <span style="margin-left: 10px">元</span>
          </el-form-item>
          <el-form-item label="限购数量">
            <el-input-number v-model="promotionForm.rules.limitCount" :min="1" :precision="0" :step="1"></el-input-number>
            <span style="margin-left: 10px">件</span>
          </el-form-item>
        </template>
        
        <!-- 满赠活动规则表单项 -->
        <template v-if="promotionForm.type === 'gift'">
          <el-form-item label="满足条件">
            <el-input-number v-model="promotionForm.rules.condition" :min="0" :precision="2" :step="10"></el-input-number>
            <span style="margin-left: 10px">元</span>
          </el-form-item>
          <el-form-item label="赠品">
            <el-select v-model="promotionForm.rules.giftId" placeholder="请选择赠品" style="width: 100%">
              <el-option 
                v-for="item in giftOptions" 
                :key="item.id" 
                :label="item.name" 
                :value="item.id"
              ></el-option>
            </el-select>
          </el-form-item>
        </template>
        
        <el-form-item label="活动时间">
          <el-date-picker
            v-model="promotionForm.timeRange"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 100%"
          ></el-date-picker>
        </el-form-item>
        
        <el-form-item label="适用商品">
          <el-radio-group v-model="promotionForm.productScope">
            <el-radio label="all">全部商品</el-radio>
            <el-radio label="category">按分类</el-radio>
            <el-radio label="select">指定商品</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <template v-if="promotionForm.productScope === 'category'">
          <el-form-item label="选择分类">
            <el-cascader
              v-model="promotionForm.categoryIds"
              :options="categoryOptions"
              :props="{ checkStrictly: true }"
              placeholder="请选择分类"
              style="width: 100%"
              multiple
            ></el-cascader>
          </el-form-item>
        </template>
        
        <template v-if="promotionForm.productScope === 'select'">
          <el-form-item label="选择商品">
            <div class="select-products">
              <div class="selected-list" v-if="promotionForm.productIds.length > 0">
                <el-tag
                  v-for="productId in promotionForm.productIds"
                  :key="productId"
                  closable
                  @close="handleRemoveProduct(productId)"
                  style="margin-right: 5px; margin-bottom: 5px;"
                >
                  {{ getProductNameById(productId) }}
                </el-tag>
              </div>
              <el-button size="small" @click="showProductSelector = true">添加商品</el-button>
            </div>
          </el-form-item>
        </template>
        
        <el-form-item label="活动描述">
          <el-input 
            v-model="promotionForm.description" 
            type="textarea" 
            :rows="3" 
            placeholder="请输入活动描述"
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
    
    <!-- 商品选择器对话框 -->
    <el-dialog v-model="showProductSelector" title="选择商品" width="800px">
      <div class="filter-container">
        <el-input 
          v-model="productSearchKeyword" 
          placeholder="请输入商品名称搜索" 
          style="width: 300px" 
          @keyup.enter="handleProductSearch"
        >
          <template #append>
            <el-button @click="handleProductSearch">搜索</el-button>
          </template>
        </el-input>
      </div>
      
      <el-table 
        :data="productList" 
        style="width: 100%" 
        v-loading="productLoading"
        @selection-change="handleProductSelectionChange"
      >
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column prop="id" label="商品ID" width="80"></el-table-column>
        <el-table-column prop="name" label="商品名称" min-width="200"></el-table-column>
        <el-table-column prop="price" label="价格" width="100">
          <template #default="scope">
            ¥{{ scope.row.price.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="category" label="分类" width="120"></el-table-column>
      </el-table>
      
      <div class="pagination-container">
        <el-pagination
          background
          layout="total, prev, pager, next"
          v-model:current-page="productPagination.currentPage"
          :page-size="productPagination.pageSize"
          :total="productPagination.total"
          @current-change="handleProductPageChange"
        >
        </el-pagination>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showProductSelector = false">取消</el-button>
          <el-button type="primary" @click="handleConfirmSelectProducts">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, defineExpose } from 'vue'

// 加载状态
const loading = ref(false)
const productLoading = ref(false)

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

// 促销活动列表
const promotionList = ref([
  {
    id: 1,
    name: '618购物节满减',
    type: 'fullReduction',
    rules: {
      fullAmount: 300,
      reduceAmount: 50
    },
    startTime: '2023-06-01 00:00:00',
    endTime: '2023-06-20 23:59:59',
    status: 'ongoing',
    productScope: 'all',
    description: '618购物节活动，全场满300减50'
  },
  {
    id: 2,
    name: '夏季服装折扣',
    type: 'discount',
    rules: {
      discount: 7.5
    },
    startTime: '2023-07-01 00:00:00',
    endTime: '2023-07-15 23:59:59',
    status: 'upcoming',
    productScope: 'category',
    categoryIds: [1],
    description: '夏季服装7.5折特惠'
  },
  {
    id: 3,
    name: '限时秒杀-智能手机',
    type: 'seckill',
    rules: {
      seckillPrice: 1999,
      limitCount: 1
    },
    startTime: '2023-05-20 20:00:00',
    endTime: '2023-05-20 22:00:00',
    status: 'expired',
    productScope: 'select',
    productIds: [101, 102],
    description: '智能手机限时秒杀，原价3999，秒杀价1999'
  },
  {
    id: 4,
    name: '满赠活动-赠品',
    type: 'gift',
    rules: {
      condition: 500,
      giftId: 201
    },
    startTime: '2023-06-10 00:00:00',
    endTime: '2023-06-30 23:59:59',
    status: 'canceled',
    productScope: 'all',
    description: '全场满500元赠送精美礼品'
  }
])

// 对话框相关
const dialogVisible = ref(false)
const dialogType = ref('add') // 'add' 或 'edit'
const promotionFormRef = ref(null)

// 促销活动表单
const promotionForm = reactive({
  id: null,
  name: '',
  type: 'fullReduction',
  rules: {
    fullAmount: 100,
    reduceAmount: 10,
    discount: 8.0,
    seckillPrice: 999,
    limitCount: 1,
    condition: 100,
    giftId: null
  },
  timeRange: [],
  startTime: '',
  endTime: '',
  status: 'upcoming',
  productScope: 'all',
  categoryIds: [],
  productIds: [],
  description: ''
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入活动名称', trigger: 'blur' },
    { min: 2, max: 30, message: '长度在 2 到 30 个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择活动类型', trigger: 'change' }
  ]
}

// 商品选择器相关
const showProductSelector = ref(false)
const productSearchKeyword = ref('')
const selectedProducts = ref([])
const productList = ref([
  { id: 101, name: 'iPhone 14 Pro', price: 7999, category: '手机数码' },
  { id: 102, name: 'Samsung S23 Ultra', price: 8999, category: '手机数码' },
  { id: 103, name: '小米13', price: 3999, category: '手机数码' },
  { id: 104, name: '华为Mate 50', price: 5999, category: '手机数码' },
  { id: 105, name: 'MacBook Air M2', price: 9999, category: '电脑办公' }
])

// 商品分页
const productPagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 100
})

// 分类选项
const categoryOptions = ref([
  {
    value: 1,
    label: '电子产品',
    children: [
      {
        value: 11,
        label: '手机数码'
      },
      {
        value: 12,
        label: '电脑办公'
      }
    ]
  },
  {
    value: 2,
    label: '服装鞋包',
    children: [
      {
        value: 21,
        label: '男装'
      },
      {
        value: 22,
        label: '女装'
      },
      {
        value: 23,
        label: '箱包'
      }
    ]
  }
])

// 赠品选项
const giftOptions = ref([
  { id: 201, name: '精美保温杯' },
  { id: 202, name: '10000mAh充电宝' },
  { id: 203, name: '蓝牙耳机' },
  { id: 204, name: '品牌T恤' }
])

// 方法
const handleSearch = () => {
  console.log('搜索条件', searchForm)
  // TODO: 调用API进行搜索
  pagination.currentPage = 1
}

const resetSearch = () => {
  searchForm.name = ''
  searchForm.type = ''
  searchForm.status = ''
  handleSearch()
}

const handleSizeChange = (size) => {
  pagination.pageSize = size
  // TODO: 重新加载数据
}

const handleCurrentChange = (page) => {
  pagination.currentPage = page
  // TODO: 重新加载数据
}

const openAddDialog = () => {
  dialogType.value = 'add'
  resetPromotionForm()
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogType.value = 'edit'
  Object.assign(promotionForm, row)
  promotionForm.timeRange = [row.startTime, row.endTime]
  dialogVisible.value = true
}

const handleStart = (row) => {
  console.log('开始活动', row)
  // TODO: 调用开始活动API
}

const handleStop = (row) => {
  console.log('停止活动', row)
  // TODO: 调用停止活动API
}

const handleDelete = (row) => {
  console.log('删除活动', row)
  // TODO: 调用删除活动API
}

const resetPromotionForm = () => {
  promotionForm.id = null
  promotionForm.name = ''
  promotionForm.type = 'fullReduction'
  promotionForm.rules = {
    fullAmount: 100,
    reduceAmount: 10,
    discount: 8.0,
    seckillPrice: 999,
    limitCount: 1,
    condition: 100,
    giftId: null
  }
  promotionForm.timeRange = []
  promotionForm.startTime = ''
  promotionForm.endTime = ''
  promotionForm.status = 'upcoming'
  promotionForm.productScope = 'all'
  promotionForm.categoryIds = []
  promotionForm.productIds = []
  promotionForm.description = ''
}

const handleProductSearch = () => {
  console.log('搜索商品', productSearchKeyword.value)
  // TODO: 调用搜索商品API
}

const handleProductPageChange = (page) => {
  productPagination.currentPage = page
  // TODO: 重新加载商品数据
}

const handleProductSelectionChange = (selection) => {
  selectedProducts.value = selection
}

const handleConfirmSelectProducts = () => {
  // 将选中的商品添加到促销活动中
  promotionForm.productIds = [...new Set([...promotionForm.productIds, ...selectedProducts.value.map(item => item.id)])]
  showProductSelector.value = false
}

const handleRemoveProduct = (productId) => {
  const index = promotionForm.productIds.indexOf(productId)
  if (index !== -1) {
    promotionForm.productIds.splice(index, 1)
  }
}

const getProductNameById = (productId) => {
  const product = productList.value.find(item => item.id === productId)
  return product ? product.name : `商品#${productId}`
}

const handleSubmit = async () => {
  if (promotionForm.timeRange && promotionForm.timeRange.length === 2) {
    promotionForm.startTime = promotionForm.timeRange[0]
    promotionForm.endTime = promotionForm.timeRange[1]
  }
  
  console.log('提交表单', promotionForm)
  // TODO: 调用保存或更新API
  dialogVisible.value = false
}

// 生命周期钩子
onMounted(() => {
  // TODO: 加载初始数据
  console.log('组件已挂载，加载数据')
})

// 导出方法供父组件使用
defineExpose({
  handleSearch,
  resetSearch,
  openAddDialog
})
</script>

<style scoped>
.promotion-container {
  padding: 20px;
}

.filter-container {
  margin-bottom: 20px;
}

.filter-form {
  margin-bottom: 15px;
}

.operation-container {
  display: flex;
  justify-content: flex-end;
}

.table-container {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.delete-btn {
  color: #F56C6C;
}

.select-products {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.selected-list {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-bottom: 10px;
}
</style>