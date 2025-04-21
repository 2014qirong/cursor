<template>
  <div class="app-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>商品统计</span>
        </div>
      </template>
      
      <div class="filter-container">
        <el-select
          v-model="listQuery.categoryId"
          placeholder="商品分类"
          clearable
          class="filter-item"
          style="width: 200px"
        >
          <el-option v-for="item in categoryOptions" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
        <el-select
          v-model="listQuery.sortBy"
          placeholder="排序方式"
          clearable
          class="filter-item"
          style="width: 200px"
        >
          <el-option v-for="item in sortOptions" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          @change="handleDateChange"
        />
        <el-button type="primary" icon="Search" @click="fetchData">查询</el-button>
      </div>
      
      <div class="statistics-overview">
        <el-row :gutter="20">
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-title">商品总数</div>
              <div class="stat-value">{{ overview.totalProducts }}</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-title">已售商品</div>
              <div class="stat-value">{{ overview.soldProducts }}</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-title">库存预警</div>
              <div class="stat-value warning">{{ overview.lowStockProducts }}</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-title">销售额</div>
              <div class="stat-value">¥{{ overview.totalSales }}</div>
            </div>
          </el-col>
        </el-row>
      </div>
      
      <div class="chart-container">
        <div ref="topProductsChart" class="chart" />
        <div ref="categoryDistributionChart" class="chart" />
      </div>
      
      <div class="table-title">畅销商品TOP10</div>
      <el-table
        v-loading="listLoading"
        :data="tableData"
        element-loading-text="加载中..."
        border
        fit
        highlight-current-row
      >
        <el-table-column label="排名" align="center" width="80">
          <template #default="scope">
            <span>{{ scope.$index + 1 }}</span>
          </template>
        </el-table-column>
        <el-table-column label="商品图片" width="100" align="center">
          <template #default="scope">
            <el-image 
              style="width: 50px; height: 50px"
              :src="scope.row.image"
              :preview-src-list="[scope.row.image]">
            </el-image>
          </template>
        </el-table-column>
        <el-table-column label="商品名称" align="center">
          <template #default="scope">
            <span>{{ scope.row.name }}</span>
          </template>
        </el-table-column>
        <el-table-column label="商品分类" align="center" width="120">
          <template #default="scope">
            <span>{{ scope.row.category }}</span>
          </template>
        </el-table-column>
        <el-table-column label="销量" align="center" width="100">
          <template #default="scope">
            <span>{{ scope.row.salesVolume }}</span>
          </template>
        </el-table-column>
        <el-table-column label="销售额" align="center" width="120">
          <template #default="scope">
            <span>¥{{ scope.row.salesAmount }}</span>
          </template>
        </el-table-column>
        <el-table-column label="单价" align="center" width="100">
          <template #default="scope">
            <span>¥{{ scope.row.price }}</span>
          </template>
        </el-table-column>
        <el-table-column label="库存" align="center" width="100">
          <template #default="scope">
            <span>{{ scope.row.stock }}</span>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { defineComponent, ref, reactive, onMounted } from 'vue'
import * as echarts from 'echarts'

export default defineComponent({
  name: 'ProductStatistics',
  setup() {
    const topProductsChart = ref(null)
    const categoryDistributionChart = ref(null)
    const dateRange = ref([])
    const listLoading = ref(false)
    
    const listQuery = reactive({
      categoryId: '',
      sortBy: 'sales'
    })
    
    const overview = reactive({
      totalProducts: 1286,
      soldProducts: 867,
      lowStockProducts: 28,
      totalSales: '256,789.35'
    })
    
    const categoryOptions = [
      { value: '1', label: '手机数码' },
      { value: '2', label: '家用电器' },
      { value: '3', label: '电脑办公' },
      { value: '4', label: '服装鞋包' },
      { value: '5', label: '食品生鲜' }
    ]
    
    const sortOptions = [
      { value: 'sales', label: '按销量排序' },
      { value: 'amount', label: '按销售额排序' },
      { value: 'price', label: '按单价排序' }
    ]
    
    const tableData = ref([
      { 
        id: 1, 
        image: 'https://placeholder.pics/svg/50x50',
        name: 'iPhone 14 Pro Max 256GB 暗夜紫', 
        category: '手机数码',
        salesVolume: 284, 
        salesAmount: 3127651.16,
        price: 10998.42, 
        stock: 156 
      },
      { 
        id: 2, 
        image: 'https://placeholder.pics/svg/50x50',
        name: 'MacBook Pro 14英寸 M2 Pro', 
        category: '电脑办公',
        salesVolume: 187, 
        salesAmount: 2804686.13,
        price: 14998.32, 
        stock: 84 
      },
      { 
        id: 3, 
        image: 'https://placeholder.pics/svg/50x50',
        name: 'Apple Watch Series 8', 
        category: '手机数码',
        salesVolume: 326, 
        salesAmount: 1466694.74,
        price: 4499.37, 
        stock: 224 
      },
      { 
        id: 4, 
        image: 'https://placeholder.pics/svg/50x50',
        name: 'AirPods Pro 第二代', 
        category: '手机数码',
        salesVolume: 412, 
        salesAmount: 784636.88,
        price: 1904.46, 
        stock: 378 
      },
      { 
        id: 5, 
        image: 'https://placeholder.pics/svg/50x50',
        name: '华为 Mate 50 Pro', 
        category: '手机数码',
        salesVolume: 245, 
        salesAmount: 1519519.55,
        price: 6202.12, 
        stock: 132 
      }
    ])
    
    const initCharts = () => {
      // 销量前10商品图表
      const topProducts = echarts.init(topProductsChart.value)
      const topProductsOption = {
        title: { text: '销量前10商品' },
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        legend: {},
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
        xAxis: { type: 'value' },
        yAxis: {
          type: 'category',
          data: ['AirPods Pro 第二代', 'Apple Watch Series 8', '华为 Mate 50 Pro', 'MacBook Pro 14英寸', 'iPhone 14 Pro Max']
        },
        series: [
          {
            name: '销量',
            type: 'bar',
            data: [412, 326, 245, 187, 284]
          }
        ]
      }
      topProducts.setOption(topProductsOption)
      
      // 商品分类占比
      const categoryDistribution = echarts.init(categoryDistributionChart.value)
      const categoryOption = {
        title: { text: '商品分类销量占比' },
        tooltip: { trigger: 'item' },
        legend: { orient: 'vertical', right: 10, top: 'center' },
        series: [
          {
            name: '销量占比',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2
            },
            label: { show: false, position: 'center' },
            emphasis: {
              label: { show: true, fontSize: '40', fontWeight: 'bold' }
            },
            labelLine: { show: false },
            data: [
              { value: 1267, name: '手机数码' },
              { value: 735, name: '家用电器' },
              { value: 580, name: '电脑办公' },
              { value: 484, name: '服装鞋包' },
              { value: 300, name: '食品生鲜' }
            ]
          }
        ]
      }
      categoryDistribution.setOption(categoryOption)
      
      window.addEventListener('resize', () => {
        topProducts.resize()
        categoryDistribution.resize()
      })
    }
    
    onMounted(() => {
      initCharts()
    })
    
    const fetchData = () => {
      listLoading.value = true
      // 这里应该添加实际的API调用
      setTimeout(() => {
        listLoading.value = false
      }, 500)
    }
    
    const handleDateChange = () => {
      // 处理日期变化
    }
    
    return {
      topProductsChart,
      categoryDistributionChart,
      dateRange,
      listLoading,
      listQuery,
      overview,
      categoryOptions,
      sortOptions,
      tableData,
      fetchData,
      handleDateChange
    }
  }
})
</script>

<style scoped>
.filter-container {
  padding-bottom: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.statistics-overview {
  margin: 20px 0;
}

.stat-card {
  background-color: #f5f7fa;
  border-radius: 4px;
  padding: 20px;
  text-align: center;
  height: 100px;
}

.stat-title {
  font-size: 16px;
  color: #606266;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.stat-value.warning {
  color: #e6a23c;
}

.chart-container {
  margin: 30px 0;
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.chart {
  height: 400px;
  width: 100%;
  margin-bottom: 20px;
}

@media (min-width: 992px) {
  .chart {
    width: calc(50% - 10px);
  }
}

.table-title {
  font-size: 18px;
  font-weight: bold;
  margin: 15px 0;
}
</style> 