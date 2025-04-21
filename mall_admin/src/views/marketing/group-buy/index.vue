<template>
  <div class="group-buy-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>拼团活动管理</span>
          <el-button type="primary" @click="handleAdd">新增拼团活动</el-button>
        </div>
      </template>
      
      <!-- 搜索区域 -->
      <el-form :inline="true" :model="queryParams" class="search-form">
        <el-form-item label="活动名称">
          <el-input v-model="queryParams.name" placeholder="请输入活动名称" clearable @keyup.enter="handleQuery" />
        </el-form-item>
        <el-form-item label="活动状态">
          <el-select v-model="queryParams.status" placeholder="请选择活动状态" clearable>
            <el-option label="未开始" :value="0" />
            <el-option label="进行中" :value="1" />
            <el-option label="已结束" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="活动时间">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
            @change="handleDateRangeChange"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleQuery">查询</el-button>
          <el-button @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 表格区域 -->
      <el-table
        v-loading="loading"
        :data="groupBuyList"
        style="width: 100%"
        border
      >
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="name" label="活动名称" min-width="180" show-overflow-tooltip />
        <el-table-column prop="productName" label="商品名称" min-width="180" show-overflow-tooltip />
        <el-table-column label="活动时间" min-width="260">
          <template #default="scope">
            {{ scope.row.startTime }} 至 {{ scope.row.endTime }}
          </template>
        </el-table-column>
        <el-table-column prop="minCount" label="成团人数" width="100" align="center" />
        <el-table-column prop="originalPrice" label="原价" width="100" align="center">
          <template #default="scope">
            ¥{{ scope.row.originalPrice }}
          </template>
        </el-table-column>
        <el-table-column prop="groupPrice" label="拼团价" width="100" align="center">
          <template #default="scope">
            ¥{{ scope.row.groupPrice }}
          </template>
        </el-table-column>
        <el-table-column label="优惠幅度" width="100" align="center">
          <template #default="scope">
            {{ calculateDiscount(scope.row.originalPrice, scope.row.groupPrice) }}%
          </template>
        </el-table-column>
        <el-table-column prop="totalGroups" label="团数量" width="100" align="center" />
        <el-table-column prop="totalMembers" label="参与人数" width="100" align="center" />
        <el-table-column prop="status" label="活动状态" width="100" align="center">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">{{ getStatusText(scope.row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="200" align="center">
          <template #default="scope">
            <el-button link type="primary" @click="handleViewDetail(scope.row)">详情</el-button>
            <el-button link type="primary" @click="handleEdit(scope.row)" v-if="scope.row.status === 0">编辑</el-button>
            <el-button link type="primary" @click="handleGroupList(scope.row)">团列表</el-button>
            <el-button link type="danger" @click="handleDelete(scope.row)" v-if="scope.row.status === 0">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页区域 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="queryParams.pageNum"
          v-model:page-size="queryParams.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
    <!-- 拼团活动表单对话框 -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="700px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="groupBuyFormRef"
        :model="groupBuyForm"
        :rules="groupBuyRules"
        label-width="100px"
      >
        <el-form-item label="活动名称" prop="name">
          <el-input v-model="groupBuyForm.name" placeholder="请输入活动名称" />
        </el-form-item>
        <el-form-item label="活动时间" prop="timeRange">
          <el-date-picker
            v-model="groupBuyForm.timeRange"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="选择商品" prop="productId">
          <el-select
            v-model="groupBuyForm.productId"
            placeholder="请选择商品"
            filterable
            remote
            :remote-method="remoteProductSearch"
            :loading="productLoading"
            style="width: 100%"
            @change="handleProductChange"
          >
            <el-option
              v-for="item in productOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            >
              <div class="product-option">
                <el-image
                  class="product-image"
                  :src="item.image"
                  fit="cover"
                  :preview-src-list="[item.image]"
                />
                <div class="product-info">
                  <div class="product-name">{{ item.name }}</div>
                  <div class="product-price">¥{{ item.price }}</div>
                </div>
              </div>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="商品规格" prop="skuId" v-if="skuOptions.length > 0">
          <el-select v-model="groupBuyForm.skuId" placeholder="请选择商品规格" style="width: 100%">
            <el-option
              v-for="item in skuOptions"
              :key="item.id"
              :label="item.specsText"
              :value="item.id"
            >
              <div class="sku-option">
                <div class="sku-specs">{{ item.specsText }}</div>
                <div class="sku-price">¥{{ item.price }}</div>
              </div>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="原价" prop="originalPrice">
          <el-input-number v-model="groupBuyForm.originalPrice" :min="0" :precision="2" :step="1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="拼团价" prop="groupPrice">
          <el-input-number v-model="groupBuyForm.groupPrice" :min="0" :precision="2" :step="1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="成团人数" prop="minCount">
          <el-input-number v-model="groupBuyForm.minCount" :min="2" :precision="0" :step="1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="团长优惠" prop="leaderDiscount">
          <el-input-number v-model="groupBuyForm.leaderDiscount" :min="0" :precision="2" :step="1" style="width: 100%" placeholder="团长优惠金额，0表示无优惠" />
        </el-form-item>
        <el-form-item label="活动库存" prop="stock">
          <el-input-number v-model="groupBuyForm.stock" :min="1" :precision="0" :step="1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="每人限购" prop="limitPerUser">
          <el-input-number v-model="groupBuyForm.limitPerUser" :min="1" :precision="0" :step="1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="成团时间" prop="groupTime">
          <el-input-number v-model="groupBuyForm.groupTime" :min="1" :precision="0" :step="1" style="width: 100%" />
          <div class="form-tips">成团有效时间(小时)，超时未成团将自动取消</div>
        </el-form-item>
        <el-form-item label="虚拟成团" prop="virtualGroup">
          <el-switch v-model="groupBuyForm.virtualGroup" />
          <div class="form-tips">开启后，未满人数的团将在倒计时结束前自动成团</div>
        </el-form-item>
        <el-form-item label="活动说明" prop="description">
          <el-input
            v-model="groupBuyForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入活动说明"
          />
        </el-form-item>
        <el-form-item label="活动状态" prop="status">
          <el-radio-group v-model="groupBuyForm.status">
            <el-radio :label="0">未开始</el-radio>
            <el-radio :label="1">进行中</el-radio>
            <el-radio :label="2">已结束</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="submitForm">确 定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 团列表对话框 -->
    <el-dialog
      title="拼团记录"
      v-model="groupListDialogVisible"
      width="900px"
    >
      <el-table
        v-loading="groupListLoading"
        :data="groupRecordList"
        style="width: 100%"
        border
      >
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="groupId" label="团ID" width="100" show-overflow-tooltip />
        <el-table-column prop="leaderName" label="团长" width="100" />
        <el-table-column prop="currentCount" label="当前人数" width="100" align="center" />
        <el-table-column prop="minCount" label="成团人数" width="100" align="center" />
        <el-table-column label="开团时间" min-width="150">
          <template #default="scope">
            {{ scope.row.createTime }}
          </template>
        </el-table-column>
        <el-table-column label="截止时间" min-width="150">
          <template #default="scope">
            {{ scope.row.expireTime }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="scope">
            <el-tag :type="getGroupStatusType(scope.row.status)">
              {{ getGroupStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="120" align="center">
          <template #default="scope">
            <el-button link type="primary" @click="handleGroupMembers(scope.row)">成员</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="groupListQuery.pageNum"
          v-model:page-size="groupListQuery.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="groupListTotal"
          @size-change="handleGroupListSizeChange"
          @current-change="handleGroupListCurrentChange"
        />
      </div>
    </el-dialog>
    
    <!-- 团成员对话框 -->
    <el-dialog
      title="团成员"
      v-model="memberDialogVisible"
      width="600px"
    >
      <el-table
        :data="memberList"
        style="width: 100%"
        border
      >
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="userName" label="用户名称" min-width="120" show-overflow-tooltip />
        <el-table-column prop="userPhone" label="联系电话" width="120" show-overflow-tooltip />
        <el-table-column prop="orderNo" label="订单编号" min-width="140" show-overflow-tooltip />
        <el-table-column prop="joinTime" label="参团时间" min-width="150" />
        <el-table-column prop="isLeader" label="身份" width="80" align="center">
          <template #default="scope">
            <el-tag type="success" v-if="scope.row.isLeader">团长</el-tag>
            <span v-else>成员</span>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getGroupBuyList, createGroupBuy, updateGroupBuy, deleteGroupBuy, getGroupBuyDetail, getGroupBuyRecords } from '@/api/marketing'
import { getProductList } from '@/api/product'

// 查询参数
const queryParams = reactive({
  pageNum: 1,
  pageSize: 10,
  name: '',
  status: '',
  startTime: '',
  endTime: ''
})

// 日期范围
const dateRange = ref([])

// 列表数据
const loading = ref(false)
const groupBuyList = ref([])
const total = ref(0)

// 表单对话框
const dialogVisible = ref(false)
const dialogTitle = ref('新增拼团活动')
const groupBuyFormRef = ref(null)
const groupBuyForm = reactive({
  id: '',
  name: '',
  timeRange: [],
  productId: '',
  productName: '',
  productImage: '',
  skuId: '',
  originalPrice: 0,
  groupPrice: 0,
  minCount: 2,
  leaderDiscount: 0,
  stock: 0,
  limitPerUser: 1,
  groupTime: 24,
  virtualGroup: false,
  description: '',
  status: 0
})

// 表单校验规则
const groupBuyRules = {
  name: [
    { required: true, message: '请输入活动名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  timeRange: [
    { required: true, message: '请选择活动时间', trigger: 'change' }
  ],
  productId: [
    { required: true, message: '请选择商品', trigger: 'change' }
  ],
  originalPrice: [
    { required: true, message: '请输入原价', trigger: 'blur' }
  ],
  groupPrice: [
    { required: true, message: '请输入拼团价', trigger: 'blur' }
  ],
  minCount: [
    { required: true, message: '请输入成团人数', trigger: 'blur' }
  ],
  stock: [
    { required: true, message: '请输入活动库存', trigger: 'blur' }
  ],
  limitPerUser: [
    { required: true, message: '请输入每人限购数量', trigger: 'blur' }
  ],
  groupTime: [
    { required: true, message: '请输入成团时间', trigger: 'blur' }
  ]
}

// 商品选择相关
const productLoading = ref(false)
const productOptions = ref([])
const skuOptions = ref([])

// 拼团记录列表对话框
const groupListDialogVisible = ref(false)
const groupListLoading = ref(false)
const groupRecordList = ref([])
const groupListTotal = ref(0)
const groupListQuery = reactive({
  activityId: '',
  pageNum: 1,
  pageSize: 10
})

// 团成员对话框
const memberDialogVisible = ref(false)
const memberList = ref([])

// 处理日期范围变化
const handleDateRangeChange = (val) => {
  if (val) {
    queryParams.startTime = val[0]
    queryParams.endTime = val[1]
  } else {
    queryParams.startTime = ''
    queryParams.endTime = ''
  }
}

// 计算折扣
const calculateDiscount = (originalPrice, groupPrice) => {
  if (!originalPrice || originalPrice <= 0 || !groupPrice) return 0
  const discount = Math.round((1 - groupPrice / originalPrice) * 100)
  return discount > 0 ? discount : 0
}

// 获取活动状态文本
const getStatusText = (status) => {
  const statusMap = {
    0: '未开始',
    1: '进行中',
    2: '已结束'
  }
  return statusMap[status] || '未知'
}

// 获取活动状态类型
const getStatusType = (status) => {
  const typeMap = {
    0: 'info',
    1: 'success',
    2: 'danger'
  }
  return typeMap[status] || 'info'
}

// 获取拼团状态文本
const getGroupStatusText = (status) => {
  const statusMap = {
    0: '拼团中',
    1: '已成团',
    2: '已失败'
  }
  return statusMap[status] || '未知'
}

// 获取拼团状态类型
const getGroupStatusType = (status) => {
  const typeMap = {
    0: 'warning',
    1: 'success',
    2: 'danger'
  }
  return typeMap[status] || 'info'
}

// 查询拼团活动列表
const getList = async () => {
  loading.value = true
  try {
    const res = await getGroupBuyList(queryParams)
    groupBuyList.value = res.data.list || []
    total.value = res.data.total || 0
  } catch (error) {
    console.error('获取拼团活动列表失败', error)
  } finally {
    loading.value = false
  }
}

// 处理查询按钮点击
const handleQuery = () => {
  queryParams.pageNum = 1
  getList()
}

// 重置查询条件
const resetQuery = () => {
  dateRange.value = []
  Object.assign(queryParams, {
    pageNum: 1,
    pageSize: 10,
    name: '',
    status: '',
    startTime: '',
    endTime: ''
  })
  getList()
}

// 处理分页大小变化
const handleSizeChange = (size) => {
  queryParams.pageSize = size
  getList()
}

// 处理页码变化
const handleCurrentChange = (current) => {
  queryParams.pageNum = current
  getList()
}

// 远程搜索商品
const remoteProductSearch = async (query) => {
  if (query) {
    productLoading.value = true
    try {
      const res = await getProductList({
        name: query,
        pageSize: 10
      })
      productOptions.value = res.data.list || []
    } catch (error) {
      console.error('搜索商品失败', error)
    } finally {
      productLoading.value = false
    }
  } else {
    productOptions.value = []
  }
}

// 处理商品选择变化
const handleProductChange = (productId) => {
  if (productId) {
    const selectedProduct = productOptions.value.find(item => item.id === productId)
    if (selectedProduct) {
      groupBuyForm.productName = selectedProduct.name
      groupBuyForm.productImage = selectedProduct.image
      groupBuyForm.originalPrice = selectedProduct.price
      groupBuyForm.groupPrice = Math.round(selectedProduct.price * 0.8 * 100) / 100 // 默认八折
      
      // 获取商品SKU信息
      skuOptions.value = selectedProduct.skus || []
      if (skuOptions.value.length > 0) {
        groupBuyForm.skuId = skuOptions.value[0].id
      }
    }
  } else {
    skuOptions.value = []
    groupBuyForm.skuId = ''
  }
}

// 添加拼团活动
const handleAdd = () => {
  resetForm()
  dialogTitle.value = '新增拼团活动'
  dialogVisible.value = true
}

// 编辑拼团活动
const handleEdit = async (row) => {
  resetForm()
  dialogTitle.value = '编辑拼团活动'
  
  try {
    const res = await getGroupBuyDetail(row.id)
    const data = res.data
    
    // 填充表单数据
    groupBuyForm.id = data.id
    groupBuyForm.name = data.name
    groupBuyForm.timeRange = [data.startTime, data.endTime]
    groupBuyForm.productId = data.productId
    groupBuyForm.productName = data.productName
    groupBuyForm.productImage = data.productImage
    groupBuyForm.skuId = data.skuId || ''
    groupBuyForm.originalPrice = data.originalPrice
    groupBuyForm.groupPrice = data.groupPrice
    groupBuyForm.minCount = data.minCount
    groupBuyForm.leaderDiscount = data.leaderDiscount
    groupBuyForm.stock = data.stock
    groupBuyForm.limitPerUser = data.limitPerUser
    groupBuyForm.groupTime = data.groupTime
    groupBuyForm.virtualGroup = data.virtualGroup
    groupBuyForm.description = data.description
    groupBuyForm.status = data.status
    
    // 获取商品SKU信息
    if (data.productId) {
      try {
        const productRes = await getProductList({
          ids: [data.productId]
        })
        if (productRes.data.list && productRes.data.list.length > 0) {
          const product = productRes.data.list[0]
          productOptions.value = [product]
          skuOptions.value = product.skus || []
        }
      } catch (error) {
        console.error('获取商品信息失败', error)
      }
    }
    
    dialogVisible.value = true
  } catch (error) {
    console.error('获取拼团活动详情失败', error)
    ElMessage.error('获取拼团活动详情失败')
  }
}

// 查看拼团活动详情
const handleViewDetail = async (row) => {
  try {
    const res = await getGroupBuyDetail(row.id)
    // 这里可以实现详情查看逻辑
    console.log('拼团活动详情', res.data)
    ElMessage.info('查看详情功能待实现')
  } catch (error) {
    console.error('获取拼团活动详情失败', error)
    ElMessage.error('获取拼团活动详情失败')
  }
}

// 删除拼团活动
const handleDelete = (row) => {
  ElMessageBox.confirm(
    '确定要删除该拼团活动吗？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteGroupBuy(row.id)
      ElMessage.success('删除成功')
      getList()
    } catch (error) {
      console.error('删除拼团活动失败', error)
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

// 查看拼团记录
const handleGroupList = async (row) => {
  groupListQuery.activityId = row.id
  groupListQuery.pageNum = 1
  groupListDialogVisible.value = true
  await getGroupRecordsList()
}

// 获取拼团记录列表
const getGroupRecordsList = async () => {
  groupListLoading.value = true
  try {
    const res = await getGroupBuyRecords(
      groupListQuery.activityId,
      {
        pageNum: groupListQuery.pageNum,
        pageSize: groupListQuery.pageSize
      }
    )
    groupRecordList.value = res.data.list || []
    groupListTotal.value = res.data.total || 0
  } catch (error) {
    console.error('获取拼团记录列表失败', error)
  } finally {
    groupListLoading.value = false
  }
}

// 处理拼团记录分页大小变化
const handleGroupListSizeChange = (size) => {
  groupListQuery.pageSize = size
  getGroupRecordsList()
}

// 处理拼团记录页码变化
const handleGroupListCurrentChange = (current) => {
  groupListQuery.pageNum = current
  getGroupRecordsList()
}

// 查看团成员
const handleGroupMembers = (row) => {
  // 模拟数据，实际应该调用API获取
  memberList.value = [
    {
      userName: '张三',
      userPhone: '138****1234',
      orderNo: 'GD20220512123456',
      joinTime: '2022-05-12 10:20:30',
      isLeader: true
    },
    {
      userName: '李四',
      userPhone: '139****5678',
      orderNo: 'GD20220512123457',
      joinTime: '2022-05-12 10:25:45',
      isLeader: false
    },
    {
      userName: '王五',
      userPhone: '137****9012',
      orderNo: 'GD20220512123458',
      joinTime: '2022-05-12 10:30:22',
      isLeader: false
    }
  ]
  memberDialogVisible.value = true
}

// 提交表单
const submitForm = async () => {
  if (!groupBuyFormRef.value) return
  
  await groupBuyFormRef.value.validate(async (valid) => {
    if (valid) {
      // 构造提交数据
      const data = {
        name: groupBuyForm.name,
        startTime: groupBuyForm.timeRange[0],
        endTime: groupBuyForm.timeRange[1],
        productId: groupBuyForm.productId,
        productName: groupBuyForm.productName,
        productImage: groupBuyForm.productImage,
        skuId: groupBuyForm.skuId || null,
        originalPrice: groupBuyForm.originalPrice,
        groupPrice: groupBuyForm.groupPrice,
        minCount: groupBuyForm.minCount,
        leaderDiscount: groupBuyForm.leaderDiscount,
        stock: groupBuyForm.stock,
        limitPerUser: groupBuyForm.limitPerUser,
        groupTime: groupBuyForm.groupTime,
        virtualGroup: groupBuyForm.virtualGroup,
        description: groupBuyForm.description,
        status: groupBuyForm.status
      }
      
      try {
        if (groupBuyForm.id) {
          // 更新
          await updateGroupBuy(groupBuyForm.id, data)
          ElMessage.success('更新成功')
        } else {
          // 新增
          await createGroupBuy(data)
          ElMessage.success('添加成功')
        }
        dialogVisible.value = false
        getList()
      } catch (error) {
        console.error('保存拼团活动失败', error)
        ElMessage.error('保存失败')
      }
    }
  })
}

// 重置表单
const resetForm = () => {
  if (groupBuyFormRef.value) {
    groupBuyFormRef.value.resetFields()
  }
  Object.assign(groupBuyForm, {
    id: '',
    name: '',
    timeRange: [],
    productId: '',
    productName: '',
    productImage: '',
    skuId: '',
    originalPrice: 0,
    groupPrice: 0,
    minCount: 2,
    leaderDiscount: 0,
    stock: 0,
    limitPerUser: 1,
    groupTime: 24,
    virtualGroup: false,
    description: '',
    status: 0
  })
  productOptions.value = []
  skuOptions.value = []
}

onMounted(() => {
  getList()
})
</script>

<style lang="scss" scoped>
.group-buy-container {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .search-form {
    margin-bottom: 20px;
  }
  
  .pagination-container {
    margin-top: 20px;
    text-align: right;
  }
  
  .product-option {
    display: flex;
    align-items: center;
    
    .product-image {
      width: 40px;
      height: 40px;
      margin-right: 10px;
      border-radius: 4px;
    }
    
    .product-info {
      display: flex;
      flex-direction: column;
      
      .product-name {
        font-size: 14px;
        margin-bottom: 5px;
      }
      
      .product-price {
        font-size: 12px;
        color: #f56c6c;
      }
    }
  }
  
  .sku-option {
    display: flex;
    justify-content: space-between;
    
    .sku-specs {
      font-size: 14px;
    }
    
    .sku-price {
      font-size: 14px;
      color: #f56c6c;
    }
  }
  
  .form-tips {
    font-size: 12px;
    color: #909399;
    margin-top: 5px;
  }
}
</style> 