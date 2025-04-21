<template>
  <div class="order-detail">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>订单详情</span>
          <div class="operations">
            <el-button type="primary" @click="goBack">返回列表</el-button>
            <el-button type="primary" @click="printOrder">打印订单</el-button>
            <el-dropdown @command="handleCommand">
              <el-button type="primary">
                操作<el-icon class="el-icon--right"><arrow-down /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item v-if="orderDetail.status === 1" command="pay">确认支付</el-dropdown-item>
                  <el-dropdown-item v-if="orderDetail.status === 2" command="ship">确认发货</el-dropdown-item>
                  <el-dropdown-item v-if="[1, 2].includes(orderDetail.status)" command="cancel">取消订单</el-dropdown-item>
                  <el-dropdown-item v-if="orderDetail.status === 3" command="complete">确认收货</el-dropdown-item>
                  <el-dropdown-item command="remark">添加备注</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </template>
      
      <div v-loading="loading">
        <!-- 订单基本信息 -->
        <el-descriptions title="订单信息" :column="3" border>
          <el-descriptions-item label="订单编号">{{ orderDetail.orderNo }}</el-descriptions-item>
          <el-descriptions-item label="订单状态">
            <el-tag :type="getStatusType(orderDetail.status)">{{ getStatusText(orderDetail.status) }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="下单时间">{{ orderDetail.createTime }}</el-descriptions-item>
          <el-descriptions-item label="支付方式">{{ getPaymentMethod(orderDetail.paymentMethod) }}</el-descriptions-item>
          <el-descriptions-item label="支付时间">{{ orderDetail.payTime || '-' }}</el-descriptions-item>
          <el-descriptions-item label="订单来源">{{ getOrderSource(orderDetail.source) }}</el-descriptions-item>
        </el-descriptions>
        
        <!-- 用户信息 -->
        <el-descriptions title="用户信息" :column="2" border class="mt-20">
          <el-descriptions-item label="用户ID">{{ orderDetail.userId }}</el-descriptions-item>
          <el-descriptions-item label="用户昵称">{{ orderDetail.userName }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ orderDetail.phone }}</el-descriptions-item>
          <el-descriptions-item label="会员等级">{{ orderDetail.userLevel }}</el-descriptions-item>
        </el-descriptions>
        
        <!-- 收货地址信息 -->
        <el-descriptions title="收货信息" :column="1" border class="mt-20">
          <el-descriptions-item label="收货人">{{ orderDetail.receiverName }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ orderDetail.receiverPhone }}</el-descriptions-item>
          <el-descriptions-item label="收货地址">{{ orderDetail.receiverProvince }} {{ orderDetail.receiverCity }} {{ orderDetail.receiverDistrict }} {{ orderDetail.receiverAddress }}</el-descriptions-item>
        </el-descriptions>
        
        <!-- 商品信息 -->
        <div class="product-info mt-20">
          <div class="section-title">商品信息</div>
          <el-table :data="orderDetail.orderItems" style="width: 100%">
            <el-table-column prop="productId" label="商品ID" width="80" />
            <el-table-column label="商品图片" width="100">
              <template #default="scope">
                <el-image 
                  style="width: 60px; height: 60px" 
                  :src="scope.row.productImage" 
                  :preview-src-list="[scope.row.productImage]"
                  fit="cover">
                </el-image>
              </template>
            </el-table-column>
            <el-table-column prop="productName" label="商品名称" />
            <el-table-column label="商品规格" width="150">
              <template #default="scope">
                <div v-if="scope.row.specs">
                  <div v-for="(value, key) in scope.row.specs" :key="key">
                    {{ key }}: {{ value }}
                  </div>
                </div>
                <div v-else>-</div>
              </template>
            </el-table-column>
            <el-table-column prop="price" label="单价" width="100">
              <template #default="scope">
                ¥{{ scope.row.price }}
              </template>
            </el-table-column>
            <el-table-column prop="quantity" label="数量" width="80" />
            <el-table-column prop="totalAmount" label="小计" width="100">
              <template #default="scope">
                ¥{{ scope.row.totalAmount }}
              </template>
            </el-table-column>
          </el-table>
        </div>
        
        <!-- 费用信息 -->
        <div class="amount-info mt-20">
          <div class="section-title">费用信息</div>
          <div class="amount-detail">
            <div class="amount-item">
              <span class="label">商品总价：</span>
              <span class="value">¥{{ orderDetail.productAmount }}</span>
            </div>
            <div class="amount-item">
              <span class="label">运费：</span>
              <span class="value">¥{{ orderDetail.freightAmount }}</span>
            </div>
            <div class="amount-item">
              <span class="label">优惠金额：</span>
              <span class="value">-¥{{ orderDetail.discountAmount }}</span>
            </div>
            <div class="amount-item">
              <span class="label">实付金额：</span>
              <span class="value total-amount">¥{{ orderDetail.totalAmount }}</span>
            </div>
          </div>
        </div>
        
        <!-- 物流信息 -->
        <div v-if="orderDetail.status >= 3" class="logistics-info mt-20">
          <div class="section-title">物流信息</div>
          <el-form label-width="100px">
            <el-form-item label="物流公司">
              {{ orderDetail.shippingCompany }}
            </el-form-item>
            <el-form-item label="物流单号">
              {{ orderDetail.trackingNumber }}
            </el-form-item>
            <el-form-item label="发货时间">
              {{ orderDetail.deliveryTime }}
            </el-form-item>
          </el-form>
          
          <div class="tracking-timeline">
            <el-timeline>
              <el-timeline-item
                v-for="(item, index) in trackingInfo"
                :key="index"
                :timestamp="item.time"
                :type="index === 0 ? 'primary' : ''"
              >
                {{ item.content }}
              </el-timeline-item>
            </el-timeline>
          </div>
        </div>
        
        <!-- 订单备注 -->
        <div class="order-remark mt-20">
          <div class="section-title">订单备注</div>
          <el-input
            v-model="orderDetail.remark"
            type="textarea"
            :rows="3"
            placeholder="暂无备注信息"
            disabled
          />
        </div>
        
        <!-- 订单操作记录 -->
        <div class="order-logs mt-20">
          <div class="section-title">操作记录</div>
          <el-table :data="orderLogs" style="width: 100%">
            <el-table-column prop="operationTime" label="操作时间" width="180" />
            <el-table-column prop="operatorName" label="操作人" width="120" />
            <el-table-column prop="operationType" label="操作类型" width="120">
              <template #default="scope">
                <el-tag>{{ scope.row.operationType }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="content" label="操作内容" />
          </el-table>
        </div>
      </div>
    </el-card>
    
    <!-- 发货弹窗 -->
    <el-dialog v-model="shipDialogVisible" title="确认发货" width="500px">
      <el-form :model="shipForm" ref="shipFormRef" :rules="shipRules" label-width="100px">
        <el-form-item label="物流公司" prop="companyId">
          <el-select v-model="shipForm.companyId" placeholder="请选择物流公司" style="width: 100%">
            <el-option
              v-for="item in shippingCompanies"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="物流单号" prop="trackingNumber">
          <el-input v-model="shipForm.trackingNumber" placeholder="请输入物流单号" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="shipDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmShip">确认</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 取消订单弹窗 -->
    <el-dialog v-model="cancelDialogVisible" title="取消订单" width="500px">
      <el-form :model="cancelForm" ref="cancelFormRef" :rules="cancelRules" label-width="100px">
        <el-form-item label="取消原因" prop="reason">
          <el-select v-model="cancelForm.reason" placeholder="请选择取消原因" style="width: 100%">
            <el-option label="用户申请取消" value="用户申请取消" />
            <el-option label="商品缺货" value="商品缺货" />
            <el-option label="重复下单" value="重复下单" />
            <el-option label="商品价格有误" value="商品价格有误" />
            <el-option label="其他原因" value="其他原因" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="cancelForm.remark" type="textarea" rows="3" placeholder="请输入备注信息" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="cancelDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmCancel">确认</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 添加备注弹窗 -->
    <el-dialog v-model="remarkDialogVisible" title="添加备注" width="500px">
      <el-form :model="remarkForm" ref="remarkFormRef" :rules="remarkRules" label-width="100px">
        <el-form-item label="备注内容" prop="content">
          <el-input v-model="remarkForm.content" type="textarea" rows="3" placeholder="请输入备注内容" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="remarkDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmAddRemark">确认</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowDown } from '@element-plus/icons-vue'
import { getOrderDetail, updateOrderStatus, shipOrder, cancelOrder, addOrderRemark, getShippingInfo, getShippingCompanies } from '@/api/order'

const route = useRoute()
const router = useRouter()
const orderId = route.params.id

// 订单详情数据
const loading = ref(true)
const orderDetail = ref({
  orderNo: '',
  status: 0,
  createTime: '',
  payTime: '',
  paymentMethod: '',
  source: '',
  userId: '',
  userName: '',
  phone: '',
  userLevel: '',
  receiverName: '',
  receiverPhone: '',
  receiverProvince: '',
  receiverCity: '',
  receiverDistrict: '',
  receiverAddress: '',
  orderItems: [],
  productAmount: 0,
  freightAmount: 0,
  discountAmount: 0,
  totalAmount: 0,
  shippingCompany: '',
  trackingNumber: '',
  deliveryTime: '',
  remark: ''
})

// 订单操作记录
const orderLogs = ref([])

// 物流跟踪信息
const trackingInfo = ref([])

// 发货对话框
const shipDialogVisible = ref(false)
const shipFormRef = ref(null)
const shipForm = reactive({
  companyId: '',
  trackingNumber: ''
})
const shipRules = {
  companyId: [{ required: true, message: '请选择物流公司', trigger: 'change' }],
  trackingNumber: [{ required: true, message: '请输入物流单号', trigger: 'blur' }]
}

// 物流公司列表
const shippingCompanies = ref([])

// 取消订单对话框
const cancelDialogVisible = ref(false)
const cancelFormRef = ref(null)
const cancelForm = reactive({
  reason: '',
  remark: ''
})
const cancelRules = {
  reason: [{ required: true, message: '请选择取消原因', trigger: 'change' }]
}

// 备注对话框
const remarkDialogVisible = ref(false)
const remarkFormRef = ref(null)
const remarkForm = reactive({
  content: ''
})
const remarkRules = {
  content: [{ required: true, message: '请输入备注内容', trigger: 'blur' }]
}

// 获取订单详情
const fetchOrderDetail = async () => {
  loading.value = true
  try {
    const res = await getOrderDetail(orderId)
    orderDetail.value = res.data
    
    // 获取订单操作日志
    orderLogs.value = res.data.logs || []
    
    // 如果已发货，获取物流信息
    if (orderDetail.value.status >= 3 && orderDetail.value.trackingNumber) {
      fetchShippingInfo()
    }
  } catch (error) {
    console.error('获取订单详情失败', error)
    ElMessage.error('获取订单详情失败')
  } finally {
    loading.value = false
  }
}

// 获取物流信息
const fetchShippingInfo = async () => {
  try {
    const res = await getShippingInfo(orderId)
    trackingInfo.value = res.data || []
  } catch (error) {
    console.error('获取物流信息失败', error)
  }
}

// 获取物流公司列表
const fetchShippingCompanies = async () => {
  try {
    const res = await getShippingCompanies()
    shippingCompanies.value = res.data || []
  } catch (error) {
    console.error('获取物流公司列表失败', error)
  }
}

// 返回订单列表
const goBack = () => {
  router.push('/order/list')
}

// 打印订单
const printOrder = () => {
  window.print()
}

// 处理下拉菜单命令
const handleCommand = (command) => {
  switch (command) {
    case 'pay':
      confirmUpdateStatus(2, '确认订单已支付？')
      break
    case 'ship':
      openShipDialog()
      break
    case 'cancel':
      openCancelDialog()
      break
    case 'complete':
      confirmUpdateStatus(4, '确认订单已完成？')
      break
    case 'remark':
      openRemarkDialog()
      break
    default:
      break
  }
}

// 确认更新订单状态
const confirmUpdateStatus = (status, message) => {
  ElMessageBox.confirm(message, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await updateOrderStatus(orderId, { status })
      ElMessage.success('操作成功')
      // 刷新订单数据
      fetchOrderDetail()
    } catch (error) {
      console.error('更新订单状态失败', error)
      ElMessage.error('操作失败')
    }
  }).catch(() => {})
}

// 打开发货对话框
const openShipDialog = async () => {
  // 获取物流公司列表
  if (shippingCompanies.value.length === 0) {
    await fetchShippingCompanies()
  }
  shipForm.companyId = ''
  shipForm.trackingNumber = ''
  shipDialogVisible.value = true
}

// 确认发货
const confirmShip = async () => {
  if (!shipFormRef.value) return
  
  await shipFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await shipOrder(orderId, shipForm)
        ElMessage.success('发货成功')
        shipDialogVisible.value = false
        
        // 刷新订单数据
        fetchOrderDetail()
      } catch (error) {
        console.error('发货失败', error)
        ElMessage.error('发货失败')
      }
    }
  })
}

// 打开取消订单对话框
const openCancelDialog = () => {
  cancelForm.reason = ''
  cancelForm.remark = ''
  cancelDialogVisible.value = true
}

// 确认取消订单
const confirmCancel = async () => {
  if (!cancelFormRef.value) return
  
  await cancelFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await cancelOrder(orderId, cancelForm)
        ElMessage.success('取消订单成功')
        cancelDialogVisible.value = false
        
        // 刷新订单数据
        fetchOrderDetail()
      } catch (error) {
        console.error('取消订单失败', error)
        ElMessage.error('取消订单失败')
      }
    }
  })
}

// 打开添加备注对话框
const openRemarkDialog = () => {
  remarkForm.content = orderDetail.value.remark || ''
  remarkDialogVisible.value = true
}

// 确认添加备注
const confirmAddRemark = async () => {
  if (!remarkFormRef.value) return
  
  await remarkFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await addOrderRemark(orderId, { remark: remarkForm.content })
        ElMessage.success('添加备注成功')
        remarkDialogVisible.value = false
        
        // 刷新订单数据
        fetchOrderDetail()
      } catch (error) {
        console.error('添加备注失败', error)
        ElMessage.error('添加备注失败')
      }
    }
  })
}

// 获取订单状态文本
const getStatusText = (status) => {
  const statusMap = {
    0: '已取消',
    1: '待支付',
    2: '待发货',
    3: '待收货',
    4: '已完成',
    5: '退款中',
    6: '已退款'
  }
  return statusMap[status] || '未知状态'
}

// 获取订单状态类型
const getStatusType = (status) => {
  const typeMap = {
    0: 'info',
    1: 'warning',
    2: 'primary',
    3: 'success',
    4: 'success',
    5: 'danger',
    6: 'info'
  }
  return typeMap[status] || 'info'
}

// 获取支付方式文本
const getPaymentMethod = (method) => {
  const methodMap = {
    1: '微信支付',
    2: '支付宝',
    3: '余额支付',
    4: '货到付款'
  }
  return methodMap[method] || '未知方式'
}

// 获取订单来源文本
const getOrderSource = (source) => {
  const sourceMap = {
    1: '小程序商城',
    2: 'H5商城',
    3: 'APP商城',
    4: '网页商城'
  }
  return sourceMap[source] || '未知来源'
}

onMounted(() => {
  fetchOrderDetail()
})
</script>

<style lang="scss" scoped>
.order-detail {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .operations {
      display: flex;
      gap: 10px;
    }
  }
  
  .mt-20 {
    margin-top: 20px;
  }
  
  .section-title {
    font-weight: bold;
    margin-bottom: 15px;
    padding-left: 10px;
    border-left: 4px solid #409eff;
  }
  
  .amount-info {
    .amount-detail {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      background-color: #f5f7fa;
      padding: 15px;
      border-radius: 4px;
      
      .amount-item {
        display: flex;
        margin-bottom: 10px;
        
        .label {
          width: 100px;
          text-align: right;
          margin-right: 10px;
        }
        
        .value {
          font-weight: 500;
          
          &.total-amount {
            color: #f56c6c;
            font-size: 18px;
            font-weight: bold;
          }
        }
      }
    }
  }
  
  .tracking-timeline {
    margin: 20px 0;
    padding: 0 20px;
  }
  
  // 打印样式
  @media print {
    .operations, .el-button {
      display: none !important;
    }
  }
}
</style> 