<template>
  <div class="app-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>用户详情</span>
          <el-button @click="$router.go(-1)">返回</el-button>
        </div>
      </template>
      
      <div class="user-detail" v-loading="loading">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="用户ID">{{ userInfo.id }}</el-descriptions-item>
          <el-descriptions-item label="用户名">{{ userInfo.username }}</el-descriptions-item>
          <el-descriptions-item label="头像">
            <el-avatar :size="60" :src="userInfo.avatar"></el-avatar>
          </el-descriptions-item>
          <el-descriptions-item label="昵称">{{ userInfo.nickname }}</el-descriptions-item>
          <el-descriptions-item label="手机号">{{ userInfo.phone }}</el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ userInfo.email }}</el-descriptions-item>
          <el-descriptions-item label="会员等级">
            <el-tag :type="getLevelTagType(userInfo.level)">{{ userInfo.levelName }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="积分">{{ userInfo.points }}</el-descriptions-item>
          <el-descriptions-item label="账户余额">￥{{ userInfo.balance.toFixed(2) }}</el-descriptions-item>
          <el-descriptions-item label="注册时间">{{ userInfo.registerTime }}</el-descriptions-item>
          <el-descriptions-item label="最后登录">{{ userInfo.lastLoginTime }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="userInfo.status === 'normal' ? 'success' : 'danger'">
              {{ userInfo.status === 'normal' ? '正常' : '禁用' }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>

        <div class="user-tabs">
          <el-tabs v-model="activeTab">
            <el-tab-pane label="订单记录" name="orders">
              <el-table :data="orderList" style="width: 100%">
                <el-table-column prop="id" label="订单号" width="180"></el-table-column>
                <el-table-column prop="createTime" label="下单时间" width="180"></el-table-column>
                <el-table-column prop="amount" label="金额" width="120">
                  <template #default="scope">￥{{ scope.row.amount.toFixed(2) }}</template>
                </el-table-column>
                <el-table-column prop="status" label="状态" width="120">
                  <template #default="scope">
                    <el-tag :type="getOrderStatusType(scope.row.status)">
                      {{ getOrderStatusText(scope.row.status) }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="操作">
                  <template #default="scope">
                    <el-button size="small">查看详情</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
            
            <el-tab-pane label="购物车" name="cart">
              <el-table :data="cartList" style="width: 100%">
                <el-table-column prop="productName" label="商品名称"></el-table-column>
                <el-table-column prop="price" label="单价" width="120">
                  <template #default="scope">￥{{ scope.row.price.toFixed(2) }}</template>
                </el-table-column>
                <el-table-column prop="quantity" label="数量" width="100"></el-table-column>
                <el-table-column label="小计" width="120">
                  <template #default="scope">
                    ￥{{ (scope.row.price * scope.row.quantity).toFixed(2) }}
                  </template>
                </el-table-column>
                <el-table-column prop="addTime" label="加入时间" width="180"></el-table-column>
              </el-table>
            </el-tab-pane>
            
            <el-tab-pane label="收货地址" name="address">
              <el-table :data="addressList" style="width: 100%">
                <el-table-column prop="name" label="收货人" width="120"></el-table-column>
                <el-table-column prop="phone" label="手机号" width="120"></el-table-column>
                <el-table-column prop="address" label="详细地址"></el-table-column>
                <el-table-column prop="isDefault" label="是否默认" width="100">
                  <template #default="scope">
                    <el-tag type="success" v-if="scope.row.isDefault">默认</el-tag>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const userId = route.params.id
const loading = ref(true)
const activeTab = ref('orders')

// 用户信息
const userInfo = reactive({
  id: userId,
  username: 'user001',
  avatar: '',
  nickname: '张三',
  phone: '13800138001',
  email: 'user001@example.com',
  level: 2,
  levelName: '银卡会员',
  points: 520,
  balance: 1000.00,
  registerTime: '2023-01-15 10:30:00',
  lastLoginTime: '2023-06-10 14:25:00',
  status: 'normal'
})

// 订单列表
const orderList = ref([
  {
    id: '20230610001',
    createTime: '2023-06-10 09:30:00',
    amount: 299.00,
    status: 'completed'
  },
  {
    id: '20230525002',
    createTime: '2023-05-25 15:40:00',
    amount: 459.90,
    status: 'completed'
  },
  {
    id: '20230418003',
    createTime: '2023-04-18 11:20:00',
    amount: 1299.00,
    status: 'canceled'
  }
])

// 购物车列表
const cartList = ref([
  {
    productName: '智能手机',
    price: 2999.00,
    quantity: 1,
    addTime: '2023-06-09 16:45:00'
  },
  {
    productName: '蓝牙耳机',
    price: 299.00,
    quantity: 2,
    addTime: '2023-06-08 09:20:00'
  }
])

// 收货地址列表
const addressList = ref([
  {
    name: '张三',
    phone: '13800138001',
    address: '广东省广州市天河区天河路100号',
    isDefault: true
  },
  {
    name: '张三(公司)',
    phone: '13800138001',
    address: '广东省广州市番禺区市桥北路120号',
    isDefault: false
  }
])

// 获取用户等级对应的标签类型
const getLevelTagType = (level) => {
  const types = ['', 'info', 'success', 'warning', 'danger']
  return types[level] || 'info'
}

// 获取订单状态对应的标签类型
const getOrderStatusType = (status) => {
  const types = {
    'pending': 'info',
    'processing': 'warning',
    'shipping': 'primary',
    'completed': 'success',
    'canceled': 'danger'
  }
  return types[status] || 'info'
}

// 获取订单状态对应的文本
const getOrderStatusText = (status) => {
  const texts = {
    'pending': '待付款',
    'processing': '处理中',
    'shipping': '已发货',
    'completed': '已完成',
    'canceled': '已取消'
  }
  return texts[status] || '未知'
}

// 加载用户数据
const fetchUserData = () => {
  loading.value = true
  // 模拟API请求
  setTimeout(() => {
    loading.value = false
  }, 500)
}

onMounted(() => {
  fetchUserData()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.user-detail {
  padding: 20px 0;
}
.user-tabs {
  margin-top: 30px;
}
</style> 