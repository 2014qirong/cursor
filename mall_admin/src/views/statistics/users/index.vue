<template>
  <div class="app-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>用户统计</span>
        </div>
      </template>
      <div class="filter-container">
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
      
      <div class="chart-container">
        <div ref="userGrowthChart" class="chart" />
        <div ref="userActivationChart" class="chart" />
      </div>
      
      <el-table
        v-loading="listLoading"
        :data="tableData"
        element-loading-text="加载中..."
        border
        fit
        highlight-current-row
      >
        <el-table-column label="日期" align="center">
          <template #default="scope">
            <span>{{ scope.row.date }}</span>
          </template>
        </el-table-column>
        <el-table-column label="新增用户" align="center">
          <template #default="scope">
            <span>{{ scope.row.newUsers }}</span>
          </template>
        </el-table-column>
        <el-table-column label="活跃用户" align="center">
          <template #default="scope">
            <span>{{ scope.row.activeUsers }}</span>
          </template>
        </el-table-column>
        <el-table-column label="累计用户" align="center">
          <template #default="scope">
            <span>{{ scope.row.totalUsers }}</span>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-container">
        <el-pagination
          v-show="total > 0"
          :current-page="listQuery.page"
          :page-sizes="[10, 20, 30, 50]"
          :page-size="listQuery.limit"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script>
import { defineComponent, ref, reactive, onMounted } from 'vue'
import * as echarts from 'echarts'

export default defineComponent({
  name: 'UserStatistics',
  setup() {
    const userGrowthChart = ref(null)
    const userActivationChart = ref(null)
    const dateRange = ref([])
    const listLoading = ref(false)
    const total = ref(0)
    
    const listQuery = reactive({
      page: 1,
      limit: 10
    })
    
    const tableData = ref([
      { date: '2023-01-01', newUsers: 120, activeUsers: 500, totalUsers: 5000 },
      { date: '2023-01-02', newUsers: 110, activeUsers: 480, totalUsers: 5110 },
      { date: '2023-01-03', newUsers: 130, activeUsers: 510, totalUsers: 5240 }
    ])
    
    const initCharts = () => {
      // 用户增长趋势图
      const growthChart = echarts.init(userGrowthChart.value)
      growthChart.setOption({
        title: { text: '用户增长趋势' },
        tooltip: { trigger: 'axis' },
        legend: { data: ['新增用户', '累计用户'] },
        xAxis: { type: 'category', data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月'] },
        yAxis: { type: 'value' },
        series: [
          { name: '新增用户', type: 'bar', data: [120, 110, 130, 90, 100, 80, 70] },
          { name: '累计用户', type: 'line', data: [5000, 5110, 5240, 5330, 5430, 5510, 5580] }
        ]
      })
      
      // 用户活跃度图
      const activationChart = echarts.init(userActivationChart.value)
      activationChart.setOption({
        title: { text: '用户活跃度分析' },
        tooltip: { trigger: 'axis' },
        legend: { data: ['活跃用户', '活跃率'] },
        xAxis: { type: 'category', data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月'] },
        yAxis: [
          { type: 'value', name: '用户数' },
          { type: 'value', name: '百分比', min: 0, max: 100, position: 'right', axisLabel: { formatter: '{value}%' } }
        ],
        series: [
          { name: '活跃用户', type: 'bar', data: [500, 480, 510, 450, 470, 420, 400] },
          { name: '活跃率', type: 'line', yAxisIndex: 1, data: [10, 9.4, 9.7, 8.4, 8.7, 7.6, 7.2] }
        ]
      })
      
      window.addEventListener('resize', () => {
        growthChart.resize()
        activationChart.resize()
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
    
    const handleSizeChange = (val) => {
      listQuery.limit = val
      fetchData()
    }
    
    const handleCurrentChange = (val) => {
      listQuery.page = val
      fetchData()
    }
    
    return {
      userGrowthChart,
      userActivationChart,
      dateRange,
      listLoading,
      total,
      listQuery,
      tableData,
      fetchData,
      handleDateChange,
      handleSizeChange,
      handleCurrentChange
    }
  }
})
</script>

<style scoped>
.filter-container {
  padding-bottom: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.chart-container {
  margin: 20px 0;
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.chart {
  height: 350px;
  width: 100%;
  margin-bottom: 20px;
}

@media (min-width: 992px) {
  .chart {
    width: calc(50% - 10px);
  }
}

.pagination-container {
  padding: 10px 0;
}
</style> 