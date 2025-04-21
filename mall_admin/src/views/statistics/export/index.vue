<template>
  <div class="app-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>数据导出</span>
        </div>
      </template>
      
      <div class="export-section">
        <div class="section-title">订单数据</div>
        <div class="export-form">
          <el-form :model="orderExportForm" label-width="120px">
            <el-form-item label="时间范围">
              <el-date-picker
                v-model="orderExportForm.dateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                style="width: 360px"
              />
            </el-form-item>
            
            <el-form-item label="订单状态">
              <el-select
                v-model="orderExportForm.status"
                placeholder="请选择订单状态"
                clearable
                style="width: 360px"
              >
                <el-option v-for="item in orderStatusOptions" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="导出字段">
              <el-checkbox-group v-model="orderExportForm.fields">
                <el-checkbox label="orderNo">订单编号</el-checkbox>
                <el-checkbox label="customer">客户信息</el-checkbox>
                <el-checkbox label="amount">订单金额</el-checkbox>
                <el-checkbox label="products">商品信息</el-checkbox>
                <el-checkbox label="status">订单状态</el-checkbox>
                <el-checkbox label="paymentMethod">支付方式</el-checkbox>
                <el-checkbox label="createTime">创建时间</el-checkbox>
                <el-checkbox label="payTime">支付时间</el-checkbox>
                <el-checkbox label="deliveryTime">发货时间</el-checkbox>
                <el-checkbox label="address">收货地址</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            
            <el-form-item label="文件格式">
              <el-radio-group v-model="orderExportForm.fileFormat">
                <el-radio label="excel">Excel</el-radio>
                <el-radio label="csv">CSV</el-radio>
                <el-radio label="pdf">PDF</el-radio>
              </el-radio-group>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" icon="Download" @click="handleOrderExport">导出订单数据</el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>
      
      <el-divider />
      
      <div class="export-section">
        <div class="section-title">商品数据</div>
        <div class="export-form">
          <el-form :model="productExportForm" label-width="120px">
            <el-form-item label="商品分类">
              <el-cascader
                v-model="productExportForm.category"
                :options="categoryOptions"
                placeholder="请选择商品分类"
                clearable
                style="width: 360px"
              />
            </el-form-item>
            
            <el-form-item label="导出字段">
              <el-checkbox-group v-model="productExportForm.fields">
                <el-checkbox label="id">商品ID</el-checkbox>
                <el-checkbox label="name">商品名称</el-checkbox>
                <el-checkbox label="category">分类信息</el-checkbox>
                <el-checkbox label="price">价格</el-checkbox>
                <el-checkbox label="cost">成本</el-checkbox>
                <el-checkbox label="stock">库存</el-checkbox>
                <el-checkbox label="sales">销量</el-checkbox>
                <el-checkbox label="attributes">商品属性</el-checkbox>
                <el-checkbox label="images">商品图片</el-checkbox>
                <el-checkbox label="createTime">创建时间</el-checkbox>
                <el-checkbox label="updateTime">更新时间</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            
            <el-form-item label="文件格式">
              <el-radio-group v-model="productExportForm.fileFormat">
                <el-radio label="excel">Excel</el-radio>
                <el-radio label="csv">CSV</el-radio>
                <el-radio label="pdf">PDF</el-radio>
              </el-radio-group>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" icon="Download" @click="handleProductExport">导出商品数据</el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>
      
      <el-divider />
      
      <div class="export-section">
        <div class="section-title">用户数据</div>
        <div class="export-form">
          <el-form :model="userExportForm" label-width="120px">
            <el-form-item label="注册时间">
              <el-date-picker
                v-model="userExportForm.dateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                style="width: 360px"
              />
            </el-form-item>
            
            <el-form-item label="用户等级">
              <el-select
                v-model="userExportForm.level"
                placeholder="请选择用户等级"
                clearable
                style="width: 360px"
              >
                <el-option v-for="item in userLevelOptions" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="导出字段">
              <el-checkbox-group v-model="userExportForm.fields">
                <el-checkbox label="id">用户ID</el-checkbox>
                <el-checkbox label="username">用户名</el-checkbox>
                <el-checkbox label="phone">手机号</el-checkbox>
                <el-checkbox label="email">邮箱</el-checkbox>
                <el-checkbox label="level">等级</el-checkbox>
                <el-checkbox label="points">积分</el-checkbox>
                <el-checkbox label="balance">余额</el-checkbox>
                <el-checkbox label="orderCount">订单数</el-checkbox>
                <el-checkbox label="lastLogin">最后登录</el-checkbox>
                <el-checkbox label="registerTime">注册时间</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            
            <el-form-item label="文件格式">
              <el-radio-group v-model="userExportForm.fileFormat">
                <el-radio label="excel">Excel</el-radio>
                <el-radio label="csv">CSV</el-radio>
                <el-radio label="pdf">PDF</el-radio>
              </el-radio-group>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" icon="Download" @click="handleUserExport">导出用户数据</el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>
      
      <el-divider />
      
      <div class="export-section">
        <div class="section-title">导出记录</div>
        <el-table
          :data="exportRecords"
          border
          style="width: 100%"
        >
          <el-table-column prop="id" label="ID" width="80" align="center" />
          <el-table-column prop="fileName" label="文件名称" min-width="180" />
          <el-table-column prop="fileType" label="文件类型" width="100" align="center" />
          <el-table-column prop="dataType" label="数据类型" width="120" align="center" />
          <el-table-column prop="createTime" label="导出时间" width="160" align="center" />
          <el-table-column prop="size" label="文件大小" width="100" align="center" />
          <el-table-column prop="createBy" label="操作人" width="120" align="center" />
          <el-table-column label="操作" width="120" align="center">
            <template #default="scope">
              <el-button type="primary" size="small" @click="handleDownload(scope.row)">下载</el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <div class="pagination-container">
          <el-pagination
            background
            layout="total, sizes, prev, pager, next, jumper"
            :total="total"
            :page-sizes="[10, 20, 30, 50]"
            :page-size="listQuery.limit"
            :current-page="listQuery.page"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { defineComponent, ref, reactive, onMounted } from 'vue'

export default defineComponent({
  name: 'DataExport',
  setup() {
    const orderExportForm = reactive({
      dateRange: [],
      status: '',
      fields: ['orderNo', 'customer', 'amount', 'status', 'createTime'],
      fileFormat: 'excel'
    })
    
    const productExportForm = reactive({
      category: [],
      fields: ['id', 'name', 'category', 'price', 'stock', 'sales'],
      fileFormat: 'excel'
    })
    
    const userExportForm = reactive({
      dateRange: [],
      level: '',
      fields: ['id', 'username', 'phone', 'level', 'registerTime'],
      fileFormat: 'excel'
    })
    
    const orderStatusOptions = [
      { value: 'all', label: '全部' },
      { value: 'pending', label: '待付款' },
      { value: 'paid', label: '已付款' },
      { value: 'shipping', label: '已发货' },
      { value: 'completed', label: '已完成' },
      { value: 'cancelled', label: '已取消' },
      { value: 'refunded', label: '已退款' }
    ]
    
    const categoryOptions = [
      {
        value: 1,
        label: '手机数码',
        children: [
          { value: 11, label: '手机' },
          { value: 12, label: '平板' },
          { value: 13, label: '笔记本' },
          { value: 14, label: '智能穿戴' }
        ]
      },
      {
        value: 2,
        label: '家用电器',
        children: [
          { value: 21, label: '电视' },
          { value: 22, label: '冰箱' },
          { value: 23, label: '洗衣机' },
          { value: 24, label: '空调' }
        ]
      },
      {
        value: 3,
        label: '服装鞋包',
        children: [
          { value: 31, label: '男装' },
          { value: 32, label: '女装' },
          { value: 33, label: '童装' },
          { value: 34, label: '鞋靴' },
          { value: 35, label: '箱包' }
        ]
      }
    ]
    
    const userLevelOptions = [
      { value: 'all', label: '全部' },
      { value: 'normal', label: '普通会员' },
      { value: 'silver', label: '白银会员' },
      { value: 'gold', label: '黄金会员' },
      { value: 'platinum', label: '铂金会员' },
      { value: 'diamond', label: '钻石会员' }
    ]
    
    const exportRecords = ref([
      { id: 1, fileName: '订单数据_20230512', fileType: 'xlsx', dataType: '订单数据', createTime: '2023-05-12 15:30:45', size: '1.2MB', createBy: 'admin' },
      { id: 2, fileName: '商品库存_20230510', fileType: 'xlsx', dataType: '商品数据', createTime: '2023-05-10 09:45:23', size: '2.5MB', createBy: 'admin' },
      { id: 3, fileName: '用户信息_20230505', fileType: 'csv', dataType: '用户数据', createTime: '2023-05-05 14:18:36', size: '0.8MB', createBy: 'manager' },
      { id: 4, fileName: '销售统计_20230501', fileType: 'pdf', dataType: '销售数据', createTime: '2023-05-01 08:56:12', size: '3.1MB', createBy: 'admin' }
    ])
    
    const total = ref(4)
    const listQuery = reactive({
      page: 1,
      limit: 10
    })
    
    const handleOrderExport = () => {
      // 处理订单数据导出
      const loadingInstance = ElLoading.service({ fullscreen: true, text: '正在导出数据...' })
      setTimeout(() => {
        loadingInstance.close()
        ElMessage.success('订单数据导出成功')
      }, 2000)
    }
    
    const handleProductExport = () => {
      // 处理商品数据导出
      const loadingInstance = ElLoading.service({ fullscreen: true, text: '正在导出数据...' })
      setTimeout(() => {
        loadingInstance.close()
        ElMessage.success('商品数据导出成功')
      }, 2000)
    }
    
    const handleUserExport = () => {
      // 处理用户数据导出
      const loadingInstance = ElLoading.service({ fullscreen: true, text: '正在导出数据...' })
      setTimeout(() => {
        loadingInstance.close()
        ElMessage.success('用户数据导出成功')
      }, 2000)
    }
    
    const handleDownload = (row) => {
      // 处理下载
      window.open(`/api/export/download?id=${row.id}`)
    }
    
    const handleSizeChange = (val) => {
      listQuery.limit = val
      fetchRecords()
    }
    
    const handleCurrentChange = (val) => {
      listQuery.page = val
      fetchRecords()
    }
    
    const fetchRecords = () => {
      // 获取导出记录
    }
    
    onMounted(() => {
      fetchRecords()
    })
    
    return {
      orderExportForm,
      productExportForm,
      userExportForm,
      orderStatusOptions,
      categoryOptions,
      userLevelOptions,
      exportRecords,
      total,
      listQuery,
      handleOrderExport,
      handleProductExport,
      handleUserExport,
      handleDownload,
      handleSizeChange,
      handleCurrentChange
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

.export-section {
  margin-bottom: 20px;
}

.section-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #303133;
}

.export-form {
  max-width: 800px;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style> 