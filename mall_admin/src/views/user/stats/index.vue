<template>
  <div class="app-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>用户统计</span>
          <div>
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              @change="handleDateChange"
            ></el-date-picker>
            <el-button type="primary" @click="fetchData" style="margin-left: 10px">查询</el-button>
          </div>
        </div>
      </template>
      
      <div class="stats-overview">
        <el-row :gutter="20">
          <el-col :span="6">
            <div class="stats-card">
              <div class="stats-card-title">总用户数</div>
              <div class="stats-card-value">{{ statistics.totalUsers }}</div>
              <div class="stats-card-compare">
                较上周:
                <span :class="statistics.userGrowth >= 0 ? 'text-success' : 'text-danger'">
                  {{ statistics.userGrowth >= 0 ? '+' : '' }}{{ statistics.userGrowth }}%
                </span>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stats-card">
              <div class="stats-card-title">新增用户</div>
              <div class="stats-card-value">{{ statistics.newUsers }}</div>
              <div class="stats-card-compare">
                较上周:
                <span :class="statistics.newUserGrowth >= 0 ? 'text-success' : 'text-danger'">
                  {{ statistics.newUserGrowth >= 0 ? '+' : '' }}{{ statistics.newUserGrowth }}%
                </span>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stats-card">
              <div class="stats-card-title">活跃用户</div>
              <div class="stats-card-value">{{ statistics.activeUsers }}</div>
              <div class="stats-card-compare">
                较上周:
                <span :class="statistics.activeUserGrowth >= 0 ? 'text-success' : 'text-danger'">
                  {{ statistics.activeUserGrowth >= 0 ? '+' : '' }}{{ statistics.activeUserGrowth }}%
                </span>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stats-card">
              <div class="stats-card-title">付费用户</div>
              <div class="stats-card-value">{{ statistics.paidUsers }}</div>
              <div class="stats-card-compare">
                较上周:
                <span :class="statistics.paidUserGrowth >= 0 ? 'text-success' : 'text-danger'">
                  {{ statistics.paidUserGrowth >= 0 ? '+' : '' }}{{ statistics.paidUserGrowth }}%
                </span>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
      
      <div class="chart-container">
        <div class="chart-header">
          <span>用户增长趋势</span>
          <el-radio-group v-model="chartType" size="small" @change="handleChartTypeChange">
            <el-radio-button label="daily">日报</el-radio-button>
            <el-radio-button label="weekly">周报</el-radio-button>
            <el-radio-button label="monthly">月报</el-radio-button>
          </el-radio-group>
        </div>
        <div class="chart-content" v-loading="chartLoading">
          <div ref="userGrowthChart" style="width: 100%; height: 400px;"></div>
        </div>
      </div>
      
      <div class="chart-container">
        <div class="chart-header">
          <span>用户分布</span>
        </div>
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="chart-box" v-loading="chartLoading">
              <div class="chart-title">用户等级分布</div>
              <div ref="userLevelChart" style="width: 100%; height: 300px;"></div>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="chart-box" v-loading="chartLoading">
              <div class="chart-title">用户地区分布</div>
              <div ref="userRegionChart" style="width: 100%; height: 300px;"></div>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

// 统计数据
const statistics = reactive({
  totalUsers: 12345,
  userGrowth: 5.2,
  newUsers: 321,
  newUserGrowth: 7.8,
  activeUsers: 5621,
  activeUserGrowth: -2.1,
  paidUsers: 1850,
  paidUserGrowth: 3.5
})

// 加载状态
const chartLoading = ref(false)

// 日期范围
const dateRange = ref([])

// 图表类型
const chartType = ref('daily')

// 图表DOM引用
const userGrowthChart = ref(null)
const userLevelChart = ref(null)
const userRegionChart = ref(null)

// 加载数据
const fetchData = () => {
  chartLoading.value = true
  setTimeout(() => {
    chartLoading.value = false
    // 模拟数据获取后渲染图表
    renderCharts()
  }, 500)
}

// 渲染图表
const renderCharts = () => {
  // 这里实际项目中使用 echarts 进行图表渲染
  console.log('渲染图表')
}

// 日期变化
const handleDateChange = (val) => {
  console.log('日期范围变化:', val)
}

// 图表类型变化
const handleChartTypeChange = (val) => {
  console.log('图表类型变化:', val)
  fetchData()
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stats-overview {
  margin-bottom: 20px;
}

.stats-card {
  background-color: #f8f9fa;
  border-radius: 4px;
  padding: 20px;
  text-align: center;
  height: 120px;
}

.stats-card-title {
  color: #606266;
  font-size: 14px;
  margin-bottom: 10px;
}

.stats-card-value {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}

.stats-card-compare {
  font-size: 12px;
  color: #909399;
}

.text-success {
  color: #67c23a;
}

.text-danger {
  color: #f56c6c;
}

.chart-container {
  margin-bottom: 20px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding: 0 10px;
}

.chart-content {
  background-color: #fff;
  border-radius: 4px;
  padding: 10px;
}

.chart-box {
  background-color: #fff;
  border-radius: 4px;
  padding: 10px;
  height: 350px;
}

.chart-title {
  font-size: 14px;
  margin-bottom: 10px;
  padding-left: 10px;
  color: #606266;
}
</style> 