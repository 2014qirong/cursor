<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="12" :lg="6" :xl="6">
          <el-card shadow="hover" class="data-card">
            <div class="card-header">
              <div class="card-title">总销售额</div>
              <el-icon :size="24" color="#409EFF"><Money /></el-icon>
            </div>
            <div class="card-value">¥ 126,560</div>
            <div class="card-footer">
              <div class="trend up">
                <el-icon><CaretTop /></el-icon>
                <span>12.5%</span>
              </div>
              <div class="desc">较上周</div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="12" :lg="6" :xl="6">
          <el-card shadow="hover" class="data-card">
            <div class="card-header">
              <div class="card-title">访问量</div>
              <el-icon :size="24" color="#67C23A"><View /></el-icon>
            </div>
            <div class="card-value">88,846</div>
            <div class="card-footer">
              <div class="trend up">
                <el-icon><CaretTop /></el-icon>
                <span>16.2%</span>
              </div>
              <div class="desc">较上周</div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="12" :lg="6" :xl="6">
          <el-card shadow="hover" class="data-card">
            <div class="card-header">
              <div class="card-title">订单量</div>
              <el-icon :size="24" color="#E6A23C"><ShoppingCart /></el-icon>
            </div>
            <div class="card-value">1,280</div>
            <div class="card-footer">
              <div class="trend up">
                <el-icon><CaretTop /></el-icon>
                <span>8.7%</span>
              </div>
              <div class="desc">较上周</div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="12" :lg="6" :xl="6">
          <el-card shadow="hover" class="data-card">
            <div class="card-header">
              <div class="card-title">新增用户</div>
              <el-icon :size="24" color="#F56C6C"><User /></el-icon>
            </div>
            <div class="card-value">1,846</div>
            <div class="card-footer">
              <div class="trend down">
                <el-icon><CaretBottom /></el-icon>
                <span>3.8%</span>
              </div>
              <div class="desc">较上周</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <el-row :gutter="20" class="dashboard-content">
      <el-col :xs="24" :sm="24" :md="16" :lg="16" :xl="16">
        <el-card class="chart-card">
          <template #header>
            <div class="chart-header">
              <span>销售趋势</span>
              <el-radio-group v-model="chartTimeRange" size="small">
                <el-radio-button label="week">本周</el-radio-button>
                <el-radio-button label="month">本月</el-radio-button>
                <el-radio-button label="year">全年</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div class="chart-container" ref="salesChartRef"></div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
        <el-card class="chart-card">
          <template #header>
            <div class="chart-header">
              <span>销售分类占比</span>
            </div>
          </template>
          <div class="chart-container" ref="pieChartRef"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="dashboard-footer">
      <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
        <el-card class="table-card">
          <template #header>
            <div class="card-header">
              <span>最近订单</span>
              <el-button type="primary" size="small" text>查看更多</el-button>
            </div>
          </template>
          <el-table :data="latestOrders" stripe style="width: 100%">
            <el-table-column prop="id" label="订单号" width="180" />
            <el-table-column prop="customer" label="客户" />
            <el-table-column prop="amount" label="金额" />
            <el-table-column prop="status" label="状态">
              <template #default="scope">
                <el-tag :type="getOrderStatusType(scope.row.status)">
                  {{ scope.row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="date" label="日期" />
          </el-table>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
        <el-card class="table-card">
          <template #header>
            <div class="card-header">
              <span>热销商品</span>
              <el-button type="primary" size="small" text>查看更多</el-button>
            </div>
          </template>
          <el-table :data="hotProducts" stripe style="width: 100%">
            <el-table-column prop="id" label="商品ID" width="100" />
            <el-table-column prop="name" label="商品名称" />
            <el-table-column prop="sales" label="销量" />
            <el-table-column prop="price" label="价格" />
            <el-table-column prop="stock" label="库存" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'

// 图表时间范围
const chartTimeRange = ref('month')

// 图表DOM引用
const salesChartRef = ref(null)
const pieChartRef = ref(null)

// 图表实例
let salesChart = null
let pieChart = null

// 模拟数据 - 最近订单
const latestOrders = [
  { id: 'ORDER2023112001', customer: '张三', amount: '¥128.00', status: '已完成', date: '2023-11-20' },
  { id: 'ORDER2023112002', customer: '李四', amount: '¥356.00', status: '待付款', date: '2023-11-20' },
  { id: 'ORDER2023111901', customer: '王五', amount: '¥89.90', status: '待发货', date: '2023-11-19' },
  { id: 'ORDER2023111801', customer: '赵六', amount: '¥459.00', status: '待收货', date: '2023-11-18' },
  { id: 'ORDER2023111701', customer: '钱七', amount: '¥239.00', status: '已取消', date: '2023-11-17' }
]

// 模拟数据 - 热销商品
const hotProducts = [
  { id: 'P001', name: '时尚T恤', sales: 235, price: '¥99.00', stock: 1200 },
  { id: 'P002', name: '牛仔裤', sales: 186, price: '¥199.00', stock: 800 },
  { id: 'P003', name: '运动鞋', sales: 165, price: '¥299.00', stock: 600 },
  { id: 'P004', name: '休闲衬衫', sales: 132, price: '¥159.00', stock: 400 },
  { id: 'P005', name: '时尚帽子', sales: 98, price: '¥59.00', stock: 350 }
]

// 订单状态对应的标签类型
const getOrderStatusType = (status) => {
  const statusMap = {
    '已完成': 'success',
    '待付款': 'warning',
    '待发货': 'info',
    '待收货': '',
    '已取消': 'danger'
  }
  return statusMap[status] || 'info'
}

// 初始化销售趋势图表
const initSalesChart = () => {
  const chartDom = salesChartRef.value
  salesChart = echarts.init(chartDom)
  
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['销售额', '订单量']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    },
    yAxis: [
      {
        type: 'value',
        name: '销售额',
        position: 'left',
        axisLine: {
          show: true,
          lineStyle: {
            color: '#409EFF'
          }
        },
        axisLabel: {
          formatter: '{value} 元'
        }
      },
      {
        type: 'value',
        name: '订单量',
        position: 'right',
        axisLine: {
          show: true,
          lineStyle: {
            color: '#E6A23C'
          }
        },
        axisLabel: {
          formatter: '{value} 单'
        }
      }
    ],
    series: [
      {
        name: '销售额',
        type: 'line',
        smooth: true,
        emphasis: {
          focus: 'series'
        },
        yAxisIndex: 0,
        color: '#409EFF',
        data: [12000, 13200, 10100, 13400, 19000, 23000, 21000]
      },
      {
        name: '订单量',
        type: 'line',
        smooth: true,
        emphasis: {
          focus: 'series'
        },
        yAxisIndex: 1,
        color: '#E6A23C',
        data: [120, 132, 101, 134, 190, 230, 210]
      }
    ]
  }
  
  salesChart.setOption(option)
}

// 初始化销售分类占比图表
const initPieChart = () => {
  const chartDom = pieChartRef.value
  pieChart = echarts.init(chartDom)
  
  const option = {
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '销售占比',
        type: 'pie',
        radius: '70%',
        center: ['50%', '60%'],
        data: [
          { value: 35, name: '服装' },
          { value: 20, name: '鞋类' },
          { value: 15, name: '配饰' },
          { value: 10, name: '箱包' },
          { value: 20, name: '其他' }
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
  
  pieChart.setOption(option)
}

// 窗口大小变化时重新调整图表大小
const handleResize = () => {
  salesChart && salesChart.resize()
  pieChart && pieChart.resize()
}

onMounted(() => {
  // 初始化图表
  initSalesChart()
  initPieChart()
  
  // 监听窗口大小变化
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  // 移除监听器
  window.removeEventListener('resize', handleResize)
  
  // 销毁图表实例
  salesChart && salesChart.dispose()
  pieChart && pieChart.dispose()
})
</script>

<style lang="scss" scoped>
.dashboard-container {
  padding: 15px;

  .dashboard-header, .dashboard-content, .dashboard-footer {
    margin-bottom: 20px;
  }

  .data-card {
    height: 130px;
    position: relative;
    margin-bottom: 20px;

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;

      .card-title {
        font-size: 16px;
        color: #606266;
      }
    }

    .card-value {
      font-size: 28px;
      font-weight: bold;
      color: #303133;
      margin-bottom: 20px;
    }

    .card-footer {
      display: flex;
      align-items: center;
      color: #909399;
      font-size: 14px;

      .trend {
        display: flex;
        align-items: center;
        margin-right: 10px;

        &.up {
          color: #f56c6c;
        }

        &.down {
          color: #67c23a;
        }
      }
    }
  }

  .chart-card {
    margin-bottom: 20px;

    .chart-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .chart-container {
      height: 350px;
    }
  }

  .table-card {
    margin-bottom: 20px;

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  }
}
</style> 