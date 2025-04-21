<template>
  <div class="app-container">
    <div class="dashboard-header">
      <div class="time-range">
        <el-radio-group v-model="timeRange" @change="handleTimeRangeChange">
          <el-radio-button label="today">今日</el-radio-button>
          <el-radio-button label="week">本周</el-radio-button>
          <el-radio-button label="month">本月</el-radio-button>
          <el-radio-button label="year">本年</el-radio-button>
        </el-radio-group>
        <el-date-picker
          v-model="customDateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          @change="handleDateRangeChange"
        />
      </div>
      <el-button type="primary" icon="Refresh" @click="refreshData">刷新数据</el-button>
    </div>
    
    <div class="dashboard-summary">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="6">
          <el-card shadow="hover" class="summary-card">
            <div class="summary-header">
              <span class="summary-title">销售总额</span>
              <el-tooltip content="包含所有已支付订单的总金额" placement="top">
                <el-icon><InfoFilled /></el-icon>
              </el-tooltip>
            </div>
            <div class="summary-content">
              <div class="summary-value">¥{{ formatNumber(summary.sales) }}</div>
              <div class="summary-trend" :class="{ 'is-increase': summary.salesTrend > 0, 'is-decrease': summary.salesTrend < 0 }">
                <span>{{ summary.salesTrend > 0 ? '+' : '' }}{{ summary.salesTrend }}%</span>
                <el-icon v-if="summary.salesTrend > 0"><CaretTop /></el-icon>
                <el-icon v-else-if="summary.salesTrend < 0"><CaretBottom /></el-icon>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6">
          <el-card shadow="hover" class="summary-card">
            <div class="summary-header">
              <span class="summary-title">订单数</span>
              <el-tooltip content="包含所有已支付订单的数量" placement="top">
                <el-icon><InfoFilled /></el-icon>
              </el-tooltip>
            </div>
            <div class="summary-content">
              <div class="summary-value">{{ formatNumber(summary.orders) }}</div>
              <div class="summary-trend" :class="{ 'is-increase': summary.ordersTrend > 0, 'is-decrease': summary.ordersTrend < 0 }">
                <span>{{ summary.ordersTrend > 0 ? '+' : '' }}{{ summary.ordersTrend }}%</span>
                <el-icon v-if="summary.ordersTrend > 0"><CaretTop /></el-icon>
                <el-icon v-else-if="summary.ordersTrend < 0"><CaretBottom /></el-icon>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6">
          <el-card shadow="hover" class="summary-card">
            <div class="summary-header">
              <span class="summary-title">用户数</span>
              <el-tooltip content="包含所有注册用户数量" placement="top">
                <el-icon><InfoFilled /></el-icon>
              </el-tooltip>
            </div>
            <div class="summary-content">
              <div class="summary-value">{{ formatNumber(summary.users) }}</div>
              <div class="summary-trend" :class="{ 'is-increase': summary.usersTrend > 0, 'is-decrease': summary.usersTrend < 0 }">
                <span>{{ summary.usersTrend > 0 ? '+' : '' }}{{ summary.usersTrend }}%</span>
                <el-icon v-if="summary.usersTrend > 0"><CaretTop /></el-icon>
                <el-icon v-else-if="summary.usersTrend < 0"><CaretBottom /></el-icon>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6">
          <el-card shadow="hover" class="summary-card">
            <div class="summary-header">
              <span class="summary-title">转化率</span>
              <el-tooltip content="访问转化为订单的比率" placement="top">
                <el-icon><InfoFilled /></el-icon>
              </el-tooltip>
            </div>
            <div class="summary-content">
              <div class="summary-value">{{ summary.conversionRate }}%</div>
              <div class="summary-trend" :class="{ 'is-increase': summary.conversionRateTrend > 0, 'is-decrease': summary.conversionRateTrend < 0 }">
                <span>{{ summary.conversionRateTrend > 0 ? '+' : '' }}{{ summary.conversionRateTrend }}%</span>
                <el-icon v-if="summary.conversionRateTrend > 0"><CaretTop /></el-icon>
                <el-icon v-else-if="summary.conversionRateTrend < 0"><CaretBottom /></el-icon>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <div class="dashboard-charts">
      <el-row :gutter="20">
        <el-col :xs="24" :lg="12">
          <el-card shadow="hover" class="chart-card">
            <template #header>
              <div class="chart-header">
                <span>销售趋势</span>
                <el-select v-model="salesChartType" size="small">
                  <el-option label="销售额" value="amount" />
                  <el-option label="订单量" value="count" />
                </el-select>
              </div>
            </template>
            <div ref="salesTrendChart" class="chart"></div>
          </el-card>
        </el-col>
        <el-col :xs="24" :lg="12">
          <el-card shadow="hover" class="chart-card">
            <template #header>
              <div class="chart-header">
                <span>销售分布</span>
                <el-select v-model="distributionType" size="small">
                  <el-option label="商品分类" value="category" />
                  <el-option label="支付方式" value="payment" />
                </el-select>
              </div>
            </template>
            <div ref="salesDistributionChart" class="chart"></div>
          </el-card>
        </el-col>
      </el-row>
      
      <el-row :gutter="20" class="dashboard-row">
        <el-col :xs="24" :lg="12">
          <el-card shadow="hover" class="chart-card">
            <template #header>
              <div class="chart-header">
                <span>用户增长</span>
              </div>
            </template>
            <div ref="userGrowthChart" class="chart"></div>
          </el-card>
        </el-col>
        <el-col :xs="24" :lg="12">
          <el-card shadow="hover" class="chart-card">
            <template #header>
              <div class="chart-header">
                <span>热门商品</span>
              </div>
            </template>
            <div ref="hotProductsChart" class="chart"></div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <div class="dashboard-tables">
      <el-row :gutter="20" class="dashboard-row">
        <el-col :xs="24" :lg="12">
          <el-card shadow="hover">
            <template #header>
              <div class="chart-header">
                <span>最近订单</span>
                <router-link to="/order/list">查看更多</router-link>
              </div>
            </template>
            <el-table :data="recentOrders" style="width: 100%" size="small">
              <el-table-column prop="orderNo" label="订单编号" width="150" />
              <el-table-column prop="customer" label="客户" width="120" />
              <el-table-column prop="amount" label="金额" width="100">
                <template #default="scope">¥{{ scope.row.amount }}</template>
              </el-table-column>
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <el-tag :type="getOrderStatusType(scope.row.status)">{{ scope.row.status }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="createTime" label="创建时间" />
            </el-table>
          </el-card>
        </el-col>
        <el-col :xs="24" :lg="12">
          <el-card shadow="hover">
            <template #header>
              <div class="chart-header">
                <span>库存预警</span>
                <router-link to="/product/list">查看更多</router-link>
              </div>
            </template>
            <el-table :data="lowStockProducts" style="width: 100%" size="small">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="商品名称" min-width="200" />
              <el-table-column prop="stock" label="库存" width="100">
                <template #default="scope">
                  <span class="low-stock">{{ scope.row.stock }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="threshold" label="阈值" width="100" />
              <el-table-column label="操作" width="100">
                <template #default="scope">
                  <el-button type="primary" size="small" @click="handleStockUpdate(scope.row)">补货</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, reactive, onMounted, watch } from 'vue'
import * as echarts from 'echarts'

export default defineComponent({
  name: 'StatisticsDashboard',
  setup() {
    const timeRange = ref('today')
    const customDateRange = ref([])
    const salesChartType = ref('amount')
    const distributionType = ref('category')
    
    const salesTrendChart = ref(null)
    const salesDistributionChart = ref(null)
    const userGrowthChart = ref(null)
    const hotProductsChart = ref(null)
    
    const summary = reactive({
      sales: 186752.35,
      salesTrend: 12.8,
      orders: 2367,
      ordersTrend: 5.2,
      users: 45892,
      usersTrend: 3.7,
      conversionRate: 3.2,
      conversionRateTrend: -0.5
    })
    
    const recentOrders = ref([
      { orderNo: 'OR202305120001', customer: '张三', amount: 299.99, status: '已完成', createTime: '2023-05-12 10:23:45' },
      { orderNo: 'OR202305110023', customer: '李四', amount: 1599.00, status: '待发货', createTime: '2023-05-11 16:44:12' },
      { orderNo: 'OR202305100045', customer: '王五', amount: 459.90, status: '已发货', createTime: '2023-05-10 09:12:34' },
      { orderNo: 'OR202305090078', customer: '赵六', amount: 89.90, status: '已完成', createTime: '2023-05-09 20:36:55' },
      { orderNo: 'OR202305080102', customer: '孙七', amount: 2399.00, status: '待付款', createTime: '2023-05-08 15:28:17' }
    ])
    
    const lowStockProducts = ref([
      { id: 1, name: 'iPhone 14 Pro Max 256GB 暗夜紫', stock: 5, threshold: 10 },
      { id: 2, name: 'MacBook Pro 14英寸 M2 Pro', stock: 3, threshold: 5 },
      { id: 3, name: '华为 Mate 50 Pro', stock: 8, threshold: 15 },
      { id: 4, name: 'Sony WH-1000XM5 耳机', stock: 7, threshold: 10 },
      { id: 5, name: 'Nintendo Switch OLED', stock: 2, threshold: 8 }
    ])
    
    const formatNumber = (num) => {
      return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
    }
    
    const getOrderStatusType = (status) => {
      const statusMap = {
        '待付款': 'warning',
        '待发货': 'info',
        '已发货': 'primary',
        '已完成': 'success',
        '已取消': 'danger'
      }
      return statusMap[status] || 'info'
    }
    
    const initCharts = () => {
      // 销售趋势图
      const salesTrend = echarts.init(salesTrendChart.value)
      const salesTrendOption = {
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'shadow' }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '销售额',
            type: 'line',
            smooth: true,
            data: [18600, 22400, 19800, 28900, 32000, 37000, 28000],
            areaStyle: {
              opacity: 0.2
            },
            itemStyle: {
              color: '#409EFF'
            }
          }
        ]
      }
      salesTrend.setOption(salesTrendOption)
      
      // 销售分布图
      const salesDistribution = echarts.init(salesDistributionChart.value)
      const salesDistributionOption = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          right: 10,
          top: 'center',
          data: ['手机数码', '家用电器', '电脑办公', '服装鞋包', '食品生鲜']
        },
        series: [
          {
            name: '销售额',
            type: 'pie',
            radius: ['50%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2
            },
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '20',
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: [
              { value: 78600, name: '手机数码' },
              { value: 45200, name: '家用电器' },
              { value: 36000, name: '电脑办公' },
              { value: 18500, name: '服装鞋包' },
              { value: 8400, name: '食品生鲜' }
            ]
          }
        ]
      }
      salesDistribution.setOption(salesDistributionOption)
      
      // 用户增长图
      const userGrowth = echarts.init(userGrowthChart.value)
      const userGrowthOption = {
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'shadow' }
        },
        legend: {
          data: ['新用户', '活跃用户']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: ['1月', '2月', '3月', '4月', '5月', '6月']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '新用户',
            type: 'bar',
            data: [320, 302, 341, 374, 390, 450],
            itemStyle: {
              color: '#67C23A'
            }
          },
          {
            name: '活跃用户',
            type: 'line',
            data: [820, 932, 901, 934, 1290, 1330],
            itemStyle: {
              color: '#E6A23C'
            }
          }
        ]
      }
      userGrowth.setOption(userGrowthOption)
      
      // 热门商品图
      const hotProducts = echarts.init(hotProductsChart.value)
      const hotProductsOption = {
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'shadow' }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value'
        },
        yAxis: {
          type: 'category',
          data: ['iPhone 14 Pro', 'MacBook Pro', 'Apple Watch', 'AirPods Pro', 'iPad Air']
        },
        series: [
          {
            name: '销量',
            type: 'bar',
            data: [284, 187, 326, 412, 253],
            itemStyle: {
              color: function(params) {
                const colorList = ['#F56C6C', '#E6A23C', '#67C23A', '#409EFF', '#909399']
                return colorList[params.dataIndex]
              }
            }
          }
        ]
      }
      hotProducts.setOption(hotProductsOption)
      
      // 窗口大小变化时自动调整图表大小
      window.addEventListener('resize', () => {
        salesTrend.resize()
        salesDistribution.resize()
        userGrowth.resize()
        hotProducts.resize()
      })
    }
    
    const handleTimeRangeChange = (value) => {
      // 处理时间范围变化
      fetchData()
    }
    
    const handleDateRangeChange = () => {
      // 处理自定义日期范围变化
      if (customDateRange.value && customDateRange.value.length > 0) {
        timeRange.value = 'custom'
      }
      fetchData()
    }
    
    const refreshData = () => {
      // 刷新数据
      fetchData()
    }
    
    const fetchData = () => {
      // 获取数据
    }
    
    const handleStockUpdate = (row) => {
      // 处理库存更新
    }
    
    watch(salesChartType, () => {
      // 更新销售趋势图表
    })
    
    watch(distributionType, () => {
      // 更新销售分布图表
    })
    
    onMounted(() => {
      fetchData()
      // 延迟初始化图表，确保DOM已经渲染
      setTimeout(() => {
        initCharts()
      }, 100)
    })
    
    return {
      timeRange,
      customDateRange,
      salesChartType,
      distributionType,
      salesTrendChart,
      salesDistributionChart,
      userGrowthChart,
      hotProductsChart,
      summary,
      recentOrders,
      lowStockProducts,
      formatNumber,
      getOrderStatusType,
      handleTimeRangeChange,
      handleDateRangeChange,
      refreshData,
      handleStockUpdate
    }
  }
})
</script>

<style scoped>
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.time-range {
  display: flex;
  align-items: center;
  gap: 15px;
}

.dashboard-summary {
  margin-bottom: 20px;
}

.summary-card {
  margin-bottom: 20px;
  height: 120px;
}

.summary-header {
  display: flex;
  align-items: center;
  gap: 5px;
  margin-bottom: 8px;
}

.summary-title {
  font-size: 16px;
  color: #606266;
}

.summary-content {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}

.summary-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.summary-trend {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
}

.is-increase {
  color: #67C23A;
}

.is-decrease {
  color: #F56C6C;
}

.dashboard-charts {
  margin-bottom: 20px;
}

.dashboard-row {
  margin-top: 20px;
}

.chart-card {
  margin-bottom: 20px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart {
  height: 350px;
}

.low-stock {
  color: #F56C6C;
  font-weight: bold;
}
</style> 