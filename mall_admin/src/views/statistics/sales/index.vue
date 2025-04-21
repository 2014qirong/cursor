<template>
  <div class="sales-statistics">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>销售统计</span>
          <div class="right-actions">
            <el-button type="primary" @click="exportData">导出数据</el-button>
          </div>
        </div>
      </template>
      
      <el-form :inline="true" :model="queryParams" class="form-inline">
        <el-form-item label="时间范围">
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
        <el-form-item label="统计类型">
          <el-select v-model="queryParams.type" placeholder="请选择统计类型">
            <el-option label="日" value="day" />
            <el-option label="周" value="week" />
            <el-option label="月" value="month" />
            <el-option label="年" value="year" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
          <el-button @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>

      <div class="statistics-summary">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card shadow="hover" class="summary-card">
              <div class="summary-item">
                <div class="summary-title">总销售额</div>
                <div class="summary-value">¥ {{ summary.totalAmount || 0 }}</div>
                <div class="summary-compare" :class="summary.amountRatio >= 0 ? 'up' : 'down'">
                  <el-icon v-if="summary.amountRatio >= 0"><ArrowUp /></el-icon>
                  <el-icon v-else><ArrowDown /></el-icon>
                  {{ Math.abs(summary.amountRatio || 0) }}%
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover" class="summary-card">
              <div class="summary-item">
                <div class="summary-title">订单数量</div>
                <div class="summary-value">{{ summary.totalOrders || 0 }}</div>
                <div class="summary-compare" :class="summary.ordersRatio >= 0 ? 'up' : 'down'">
                  <el-icon v-if="summary.ordersRatio >= 0"><ArrowUp /></el-icon>
                  <el-icon v-else><ArrowDown /></el-icon>
                  {{ Math.abs(summary.ordersRatio || 0) }}%
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover" class="summary-card">
              <div class="summary-item">
                <div class="summary-title">客单价</div>
                <div class="summary-value">¥ {{ summary.averageOrderValue || 0 }}</div>
                <div class="summary-compare" :class="summary.averageOrderRatio >= 0 ? 'up' : 'down'">
                  <el-icon v-if="summary.averageOrderRatio >= 0"><ArrowUp /></el-icon>
                  <el-icon v-else><ArrowDown /></el-icon>
                  {{ Math.abs(summary.averageOrderRatio || 0) }}%
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover" class="summary-card">
              <div class="summary-item">
                <div class="summary-title">退款率</div>
                <div class="summary-value">{{ summary.refundRate || 0 }}%</div>
                <div class="summary-compare" :class="summary.refundRateRatio <= 0 ? 'up' : 'down'">
                  <el-icon v-if="summary.refundRateRatio <= 0"><ArrowUp /></el-icon>
                  <el-icon v-else><ArrowDown /></el-icon>
                  {{ Math.abs(summary.refundRateRatio || 0) }}%
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
      
      <div class="statistics-charts">
        <el-row :gutter="20">
          <el-col :span="24">
            <el-card shadow="hover" class="chart-card">
              <div class="chart-title">销售趋势</div>
              <div ref="salesTrendChart" class="chart"></div>
            </el-card>
          </el-col>
        </el-row>
        <el-row :gutter="20" class="mt-20">
          <el-col :span="12">
            <el-card shadow="hover" class="chart-card">
              <div class="chart-title">商品分类销售占比</div>
              <div ref="categoriesChart" class="chart"></div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card shadow="hover" class="chart-card">
              <div class="chart-title">支付方式分布</div>
              <div ref="paymentMethodsChart" class="chart"></div>
            </el-card>
          </el-col>
        </el-row>
      </div>
      
      <div class="statistics-tables mt-20">
        <el-tabs v-model="activeTab">
          <el-tab-pane label="畅销商品" name="topProducts">
            <el-table 
              :data="topProducts" 
              style="width: 100%"
              v-loading="loading.topProducts">
              <el-table-column prop="rank" label="排名" width="80" />
              <el-table-column prop="productId" label="商品ID" width="100" />
              <el-table-column prop="name" label="商品名称" />
              <el-table-column prop="sales" label="销量" width="120" />
              <el-table-column prop="amount" label="销售额" width="120">
                <template #default="scope">
                  ¥ {{ scope.row.amount }}
                </template>
              </el-table-column>
              <el-table-column prop="ratio" label="占比" width="120">
                <template #default="scope">
                  {{ scope.row.ratio }}%
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
          <el-tab-pane label="销售明细" name="salesDetail">
            <el-table
              :data="salesDetails"
              style="width: 100%"
              v-loading="loading.salesDetails">
              <el-table-column prop="date" label="日期" width="120" />
              <el-table-column prop="orderCount" label="订单数" width="120" />
              <el-table-column prop="salesAmount" label="销售额" width="120">
                <template #default="scope">
                  ¥ {{ scope.row.salesAmount }}
                </template>
              </el-table-column>
              <el-table-column prop="refundAmount" label="退款额" width="120">
                <template #default="scope">
                  ¥ {{ scope.row.refundAmount }}
                </template>
              </el-table-column>
              <el-table-column prop="netAmount" label="净销售额" width="120">
                <template #default="scope">
                  ¥ {{ scope.row.netAmount }}
                </template>
              </el-table-column>
              <el-table-column prop="averageOrderValue" label="客单价" width="120">
                <template #default="scope">
                  ¥ {{ scope.row.averageOrderValue }}
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { getSalesStatistics, exportSalesData } from '@/api/statistics'
import { ArrowUp, ArrowDown } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

const dateRange = ref([])
const queryParams = reactive({
  startDate: '',
  endDate: '',
  type: 'day'
})

const summary = reactive({
  totalAmount: 0,
  totalOrders: 0,
  averageOrderValue: 0,
  refundRate: 0,
  amountRatio: 0,
  ordersRatio: 0,
  averageOrderRatio: 0,
  refundRateRatio: 0
})

const topProducts = ref([])
const salesDetails = ref([])
const activeTab = ref('topProducts')

const loading = reactive({
  summary: false,
  topProducts: false,
  salesDetails: false
})

const salesTrendChart = ref(null)
const categoriesChart = ref(null)
const paymentMethodsChart = ref(null)

let salesTrendChartInstance = null
let categoriesChartInstance = null
let paymentMethodsChartInstance = null

onMounted(() => {
  fetchData()
})

const handleDateRangeChange = (val) => {
  if (val) {
    queryParams.startDate = val[0]
    queryParams.endDate = val[1]
  } else {
    queryParams.startDate = ''
    queryParams.endDate = ''
  }
}

const fetchData = async () => {
  loading.summary = true
  loading.topProducts = true
  loading.salesDetails = true
  
  try {
    const res = await getSalesStatistics(queryParams)
    
    // 填充统计摘要
    Object.assign(summary, res.data.summary)
    
    // 填充畅销商品数据
    topProducts.value = res.data.topProducts
    
    // 填充销售明细数据
    salesDetails.value = res.data.salesDetails
    
    // 渲染图表
    nextTick(() => {
      renderSalesTrendChart(res.data.salesTrend)
      renderCategoriesChart(res.data.categoriesSales)
      renderPaymentMethodsChart(res.data.paymentMethods)
    })
    
  } catch (error) {
    console.error('获取销售统计数据失败', error)
  } finally {
    loading.summary = false
    loading.topProducts = false
    loading.salesDetails = false
  }
}

const resetQuery = () => {
  dateRange.value = []
  queryParams.startDate = ''
  queryParams.endDate = ''
  queryParams.type = 'day'
  fetchData()
}

const exportData = async () => {
  try {
    const res = await exportSalesData(queryParams)
    
    // 创建下载链接并点击
    const blob = new Blob([res.data], { type: 'application/vnd.ms-excel' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    
    // 生成文件名
    const fileName = `销售统计_${new Date().toISOString().split('T')[0]}.xlsx`
    link.download = fileName
    
    link.click()
    URL.revokeObjectURL(link.href)
  } catch (error) {
    console.error('导出数据失败', error)
  }
}

// 渲染销售趋势图表
const renderSalesTrendChart = (data) => {
  if (salesTrendChartInstance) {
    salesTrendChartInstance.dispose()
  }
  
  salesTrendChartInstance = echarts.init(salesTrendChart.value)
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        crossStyle: {
          color: '#999'
        }
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    legend: {
      data: ['销售额', '订单数', '退款额']
    },
    xAxis: [
      {
        type: 'category',
        data: data.dates,
        axisPointer: {
          type: 'shadow'
        }
      }
    ],
    yAxis: [
      {
        type: 'value',
        name: '金额',
        min: 0,
        axisLabel: {
          formatter: '¥{value}'
        }
      },
      {
        type: 'value',
        name: '订单数',
        min: 0,
        axisLabel: {
          formatter: '{value}'
        }
      }
    ],
    series: [
      {
        name: '销售额',
        type: 'bar',
        data: data.amounts
      },
      {
        name: '订单数',
        type: 'line',
        yAxisIndex: 1,
        data: data.orders
      },
      {
        name: '退款额',
        type: 'line',
        data: data.refunds
      }
    ]
  }
  
  salesTrendChartInstance.setOption(option)
  
  // 自适应窗口大小
  window.addEventListener('resize', () => {
    salesTrendChartInstance.resize()
  })
}

// 渲染商品分类销售占比图表
const renderCategoriesChart = (data) => {
  if (categoriesChartInstance) {
    categoriesChartInstance.dispose()
  }
  
  categoriesChartInstance = echarts.init(categoriesChart.value)
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 10,
      data: data.map(item => item.name)
    },
    series: [
      {
        name: '商品分类销售',
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
            fontSize: '15',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: data.map(item => ({
          value: item.amount,
          name: item.name
        }))
      }
    ]
  }
  
  categoriesChartInstance.setOption(option)
  
  // 自适应窗口大小
  window.addEventListener('resize', () => {
    categoriesChartInstance.resize()
  })
}

// 渲染支付方式分布图表
const renderPaymentMethodsChart = (data) => {
  if (paymentMethodsChartInstance) {
    paymentMethodsChartInstance.dispose()
  }
  
  paymentMethodsChartInstance = echarts.init(paymentMethodsChart.value)
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 10,
      data: data.map(item => item.name)
    },
    series: [
      {
        name: '支付方式',
        type: 'pie',
        radius: '50%',
        data: data.map(item => ({
          value: item.amount,
          name: item.name
        })),
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
  
  paymentMethodsChartInstance.setOption(option)
  
  // 自适应窗口大小
  window.addEventListener('resize', () => {
    paymentMethodsChartInstance.resize()
  })
}
</script>

<style lang="scss" scoped>
.sales-statistics {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .form-inline {
    margin-bottom: 20px;
  }
  
  .statistics-summary {
    margin-bottom: 20px;
    
    .summary-card {
      .summary-item {
        padding: 10px;
        
        .summary-title {
          font-size: 14px;
          color: #909399;
          margin-bottom: 10px;
        }
        
        .summary-value {
          font-size: 24px;
          font-weight: bold;
          margin-bottom: 10px;
        }
        
        .summary-compare {
          font-size: 12px;
          display: flex;
          align-items: center;
          
          &.up {
            color: #67c23a;
          }
          
          &.down {
            color: #f56c6c;
          }
          
          .el-icon {
            margin-right: 5px;
          }
        }
      }
    }
  }
  
  .statistics-charts {
    .chart-card {
      .chart-title {
        font-size: 16px;
        margin-bottom: 20px;
      }
      
      .chart {
        height: 300px;
      }
    }
  }
  
  .mt-20 {
    margin-top: 20px;
  }
}
</style> 