<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>退款详情</span>
          <el-button type="primary" @click="goBack">返回列表</el-button>
        </div>
      </template>
      
      <el-descriptions title="退款基本信息" :column="2" border>
        <el-descriptions-item label="退款单号">{{ refundInfo.refundNo }}</el-descriptions-item>
        <el-descriptions-item label="关联订单号">
          <router-link :to="'/order/detail/' + refundInfo.orderId" class="link-type">
            {{ refundInfo.orderNo }}
          </router-link>
        </el-descriptions-item>
        <el-descriptions-item label="申请时间">{{ refundInfo.applyTime }}</el-descriptions-item>
        <el-descriptions-item label="申请金额">¥{{ refundInfo.amount }}</el-descriptions-item>
        <el-descriptions-item label="退款类型">{{ refundInfo.type }}</el-descriptions-item>
        <el-descriptions-item label="退款状态">
          <el-tag :type="getStatusType(refundInfo.status)">{{ refundInfo.status }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="退款原因" :span="2">{{ refundInfo.reason }}</el-descriptions-item>
        <el-descriptions-item label="退款说明" :span="2">{{ refundInfo.description }}</el-descriptions-item>
      </el-descriptions>
      
      <div class="section-divider"></div>
      
      <div class="section-title">退款商品</div>
      <el-table :data="refundProducts" border style="width: 100%; margin-bottom: 20px;">
        <el-table-column prop="id" label="商品ID" width="80" align="center" />
        <el-table-column label="商品图片" width="100" align="center">
          <template #default="scope">
            <el-image 
              style="width: 60px; height: 60px"
              :src="scope.row.image" 
              :preview-src-list="[scope.row.image]">
            </el-image>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="商品名称" min-width="200" show-overflow-tooltip />
        <el-table-column prop="specs" label="规格" width="150" />
        <el-table-column prop="price" label="单价" width="100" align="center">
          <template #default="scope">¥{{ scope.row.price }}</template>
        </el-table-column>
        <el-table-column prop="quantity" label="数量" width="80" align="center" />
        <el-table-column prop="subtotal" label="小计" width="100" align="center">
          <template #default="scope">¥{{ scope.row.subtotal }}</template>
        </el-table-column>
      </el-table>
      
      <div class="section-divider"></div>
      
      <div class="section-title">退款凭证</div>
      <div class="image-list">
        <div v-for="(image, index) in refundInfo.images" :key="index" class="image-item">
          <el-image 
            :src="image" 
            :preview-src-list="refundInfo.images"
            fit="cover">
          </el-image>
        </div>
      </div>
      
      <div class="section-divider"></div>
      
      <div class="section-title">处理记录</div>
      <el-timeline>
        <el-timeline-item
          v-for="(activity, index) in refundInfo.logs"
          :key="index"
          :timestamp="activity.time"
          :type="activity.type"
        >
          {{ activity.content }}
          <div v-if="activity.remark" class="activity-remark">备注：{{ activity.remark }}</div>
        </el-timeline-item>
      </el-timeline>
      
      <div class="section-divider"></div>
      
      <div v-if="refundInfo.status === '待处理'" class="action-area">
        <el-form :model="processingForm" label-width="100px">
          <el-form-item label="处理结果">
            <el-radio-group v-model="processingForm.result">
              <el-radio label="approve">同意退款</el-radio>
              <el-radio label="reject">拒绝退款</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="退款金额" v-if="processingForm.result === 'approve'">
            <el-input-number v-model="processingForm.amount" :min="0" :precision="2" :step="0.01" style="width: 200px;" />
            <span class="amount-tip">最大可退：¥{{ refundInfo.amount }}</span>
          </el-form-item>
          <el-form-item label="处理备注">
            <el-input type="textarea" v-model="processingForm.remark" :rows="3" placeholder="请输入处理备注" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitProcessing">提交处理结果</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
  </div>
</template>

<script>
import { defineComponent, reactive, toRefs, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default defineComponent({
  name: 'RefundDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const state = reactive({
      refundInfo: {
        refundNo: 'RF202305120001',
        orderId: 1,
        orderNo: 'OR202305120001',
        applyTime: '2023-05-12 10:23:45',
        amount: 99.99,
        type: '仅退款',
        status: '待处理',
        reason: '不想要了',
        description: '刚收到货，但是我不想要了，想退款',
        images: [
          'https://placeholder.pics/svg/300x300/DEDEDE/555555/退款凭证1',
          'https://placeholder.pics/svg/300x300/DEDEDE/555555/退款凭证2'
        ],
        logs: [
          { time: '2023-05-12 10:23:45', type: 'primary', content: '用户申请退款', remark: '申请金额：¥99.99' },
          { time: '2023-05-12 10:30:12', type: 'info', content: '系统自动接收退款申请', remark: '' }
        ]
      },
      refundProducts: [
        { 
          id: 1, 
          image: 'https://placeholder.pics/svg/100x100', 
          name: 'iPhone 14 Pro 256GB 暗夜紫', 
          specs: '暗夜紫 256GB', 
          price: 8999.00, 
          quantity: 1, 
          subtotal: 8999.00 
        }
      ],
      processingForm: {
        result: 'approve',
        amount: 99.99,
        remark: ''
      }
    })
    
    const getStatusType = (status) => {
      const statusMap = {
        '待处理': 'warning',
        '已通过': 'success',
        '已拒绝': 'danger',
        '已完成': 'info'
      }
      return statusMap[status] || 'info'
    }
    
    const goBack = () => {
      router.push('/order/refund')
    }
    
    const submitProcessing = () => {
      // 提交处理结果
      if (state.processingForm.result === 'approve') {
        state.refundInfo.status = '已通过'
        state.refundInfo.logs.push({
          time: new Date().toLocaleString(),
          type: 'success',
          content: '管理员同意退款',
          remark: `退款金额：¥${state.processingForm.amount}, 备注：${state.processingForm.remark}`
        })
      } else {
        state.refundInfo.status = '已拒绝'
        state.refundInfo.logs.push({
          time: new Date().toLocaleString(),
          type: 'danger',
          content: '管理员拒绝退款',
          remark: `备注：${state.processingForm.remark}`
        })
      }
    }
    
    onMounted(() => {
      // 获取退款详情
      const refundId = route.params.id
      console.log('加载退款详情，ID:', refundId)
      // 这里应该调用API获取退款详情
    })
    
    return {
      ...toRefs(state),
      getStatusType,
      goBack,
      submitProcessing
    }
  }
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-divider {
  margin: 30px 0;
  border-top: 1px solid #EBEEF5;
}

.section-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #303133;
}

.link-type {
  color: #409EFF;
  text-decoration: none;
}

.link-type:hover {
  text-decoration: underline;
}

.image-list {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.image-item {
  width: 150px;
  height: 150px;
  border-radius: 4px;
  overflow: hidden;
  border: 1px solid #EBEEF5;
}

.image-item .el-image {
  width: 100%;
  height: 100%;
}

.activity-remark {
  font-size: 13px;
  color: #909399;
  margin-top: 5px;
}

.action-area {
  background-color: #F5F7FA;
  padding: 20px;
  border-radius: 4px;
}

.amount-tip {
  margin-left: 10px;
  color: #909399;
  font-size: 14px;
}
</style> 