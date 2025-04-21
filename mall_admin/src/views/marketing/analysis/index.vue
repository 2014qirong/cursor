<template>
  <div class="app-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>营销效果分析</span>
        </div>
      </template>
      
      <div class="filter-container">
        <el-select
          v-model="activityType"
          placeholder="活动类型"
          clearable
          style="width: 200px;"
          class="filter-item"
        >
          <el-option v-for="item in activityTypeOptions" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
        
        <el-select
          v-model="timeRange"
          placeholder="时间范围"
          style="width: 180px;"
          class="filter-item"
        >
          <el-option v-for="item in timeRangeOptions" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
        
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          style="width: 340px;"
          class="filter-item"
          v-show="timeRange === 'custom'"
        />
        
        <el-button type="primary" icon="Search" @click="fetchData">查询</el-button>
        <el-button icon="Refresh" @click="resetFilter">重置</el-button>
      </div>
      
      <!-- 营销活动概览 -->
      <div class="data-overview">
        <el-row :gutter="20">
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-title">总活动数</div>
              <div class="stat-value">{{ overview.totalActivities }}</div>
              <div class="stat-trend up">
                <el-icon><CaretTop /></el-icon>
                <span>{{ overview.activityTrend }}%</span>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-title">参与用户数</div>
              <div class="stat-value">{{ overview.participants }}</div>
              <div class="stat-trend up">
                <el-icon><CaretTop /></el-icon>
                <span>{{ overview.participantsTrend }}%</span>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-title">新增用户数</div>
              <div class="stat-value">{{ overview.newUsers }}</div>
              <div class="stat-trend up">
                <el-icon><CaretTop /></el-icon>
                <span>{{ overview.newUsersTrend }}%</span>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-title">总销售额</div>
              <div class="stat-value">¥{{ overview.totalSales }}</div>
              <div class="stat-trend up">
                <el-icon><CaretTop /></el-icon>
                <span>{{ overview.salesTrend }}%</span>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
      
      <!-- 图表区域 -->
      <div class="chart-container">
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="chart-card">
              <div class="chart-title">活动销售趋势</div>
              <div ref="salesTrendChart" class="chart"></div>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="chart-card">
              <div class="chart-title">活动类型分布</div>
              <div ref="activityTypeChart" class="chart"></div>
            </div>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="chart-card">
              <div class="chart-title">用户参与度</div>
              <div ref="userParticipationChart" class="chart"></div>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="chart-card">
              <div class="chart-title">转化漏斗图</div>
              <div ref="conversionChart" class="chart"></div>
            </div>
          </el-col>
        </el-row>
      </div>
      
      <!-- 活动排行 -->
      <div class="ranking-section">
        <div class="section-header">
          <span class="section-title">活动效果排行</span>
          <el-select v-model="rankingMetric" size="small" style="width: 150px;">
            <el-option label="按销售额" value="sales" />
            <el-option label="按参与人数" value="participants" />
            <el-option label="按转化率" value="conversion" />
          </el-select>
        </div>
        
        <el-table :data="rankingData" border style="width: 100%;" :max-height="400">
          <el-table-column prop="rank" label="排名" width="80" align="center" />
          <el-table-column prop="name" label="活动名称" min-width="180" />
          <el-table-column prop="type" label="活动类型" width="120" />
          <el-table-column prop="startDate" label="开始日期" width="120" align="center" />
          <el-table-column prop="endDate" label="结束日期" width="120" align="center" />
          <el-table-column prop="participants" label="参与人数" width="120" align="center" />
          <el-table-column prop="sales" label="销售额" width="150" align="center">
            <template #default="scope">¥{{ formatNumber(scope.row.sales) }}</template>
          </el-table-column>
          <el-table-column prop="conversion" label="转化率" width="100" align="center">
            <template #default="scope">{{ scope.row.conversion }}%</template>
          </el-table-column>
          <el-table-column prop="roi" label="投资回报率" width="120" align="center">
            <template #default="scope">{{ scope.row.roi }}%</template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script>
import { defineComponent, ref, reactive, onMounted } from 'vue'
import * as echarts from 'echarts'

export default defineComponent({
  name: 'MarketingAnalysis',
  setup() {
    // 图表引用
    const salesTrendChart = ref(null)
    const activityTypeChart = ref(null)
    const userParticipationChart = ref(null)
    const conversionChart = ref(null)
    
    // 过滤条件
    const activityType = ref('')
    const timeRange = ref('last30')
    const dateRange = ref([])
    
    // 排行榜过滤
    const rankingMetric = ref('sales')
    
    // 下拉选项
    const activityTypeOptions = [
      { label: '全部类型', value: '' },
      { label: '满减活动', value: 'discount' },
      { label: '限时折扣', value: 'flash' },
      { label: '优惠券', value: 'coupon' },
      { label: '积分兑换', value: 'points' },
      { label: '拼团活动', value: 'group' }
    ]
    
    const timeRangeOptions = [
      { label: '今日', value: 'today' },
      { label: '昨日', value: 'yesterday' },
      { label: '近7天', value: 'last7' },
      { label: '近30天', value: 'last30' },
      { label: '近90天', value: 'last90' },
      { label: '自定义', value: 'custom' }
    ]
    
    // 数据概览
    const overview = reactive({
      totalActivities: 24,
      activityTrend: 15.8,
      participants: 25648,
      participantsTrend: 8.3,
      newUsers: 5831,
      newUsersTrend: 12.5,
      totalSales: formatNumber(1568943.25),
      salesTrend: 18.2
    })
    
    // 排行榜数据
    const rankingData = ref([
      { rank: 1, name: '618电器促销', type: '限时折扣', startDate: '2023-06-15', endDate: '2023-06-18', participants: 12564, sales: 658934.58, conversion: 8.6, roi: 352.4 },
      { rank: 2, name: '五一特惠', type: '满减活动', startDate: '2023-04-29', endDate: '2023-05-03', participants: 9872, sales: 425631.92, conversion: 7.8, roi: 286.3 },
      { rank: 3, name: '新品首发', type: '优惠券', startDate: '2023-05-15', endDate: '2023-05-20', participants: 8954, sales: 325487.65, conversion: 6.9, roi: 215.7 },
      { rank: 4, name: '会员专享日', type: '积分兑换', startDate: '2023-05-25', endDate: '2023-05-25', participants: 5687, sales: 256391.45, conversion: 9.5, roi: 198.6 },
      { rank: 5, name: '春季上新', type: '拼团活动', startDate: '2023-03-01', endDate: '2023-03-15', participants: 7865, sales: 198754.36, conversion: 5.8, roi: 175.2 }
    ])
    
    // 格式化数字
    function formatNumber(num) {
      return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    }
    
    // 初始化图表
    const initCharts = () => {
      // 销售趋势图
      const salesTrend = echarts.init(salesTrendChart.value)
      const salesTrendOption = {
        title: { text: '' },
        tooltip: { trigger: 'axis' },
        legend: { data: ['销售额', '订单量'] },
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
        xAxis: { type: 'category', boundaryGap: false, data: ['1月', '2月', '3月', '4月', '5月', '6月'] },
        yAxis: [
          { type: 'value', name: '销售额', axisLabel: { formatter: '¥{value}' } },
          { type: 'value', name: '订单量', position: 'right' }
        ],
        series: [
          {
            name: '销售额',
            type: 'line',
            smooth: true,
            data: [120000, 132000, 101000, 134000, 190000, 230000],
            itemStyle: { color: '#409EFF' },
            areaStyle: { opacity: 0.2 }
          },
          {
            name: '订单量',
            type: 'line',
            smooth: true,
            yAxisIndex: 1,
            data: [820, 932, 901, 934, 1290, 1330],
            itemStyle: { color: '#67C23A' }
          }
        ]
      }
      salesTrend.setOption(salesTrendOption)
      
      // 活动类型分布图
      const activityType = echarts.init(activityTypeChart.value)
      const activityTypeOption = {
        title: { text: '' },
        tooltip: { trigger: 'item', formatter: '{a} <br/>{b} : {c} ({d}%)' },
        legend: { orient: 'vertical', left: 'left' },
        series: [
          {
            name: '活动类型',
            type: 'pie',
            radius: '60%',
            center: ['50%', '50%'],
            data: [
              { value: 35, name: '限时折扣' },
              { value: 25, name: '满减活动' },
              { value: 20, name: '优惠券' },
              { value: 15, name: '拼团活动' },
              { value: 5, name: '积分兑换' }
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
      activityType.setOption(activityTypeOption)
      
      // 用户参与度图
      const userParticipation = echarts.init(userParticipationChart.value)
      const userParticipationOption = {
        title: { text: '' },
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        legend: { data: ['新用户', '老用户'] },
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
        xAxis: { type: 'category', data: ['限时折扣', '满减活动', '优惠券', '拼团活动', '积分兑换'] },
        yAxis: { type: 'value' },
        series: [
          {
            name: '新用户',
            type: 'bar',
            stack: 'total',
            emphasis: { focus: 'series' },
            data: [320, 302, 301, 334, 390]
          },
          {
            name: '老用户',
            type: 'bar',
            stack: 'total',
            emphasis: { focus: 'series' },
            data: [820, 832, 901, 934, 1290]
          }
        ]
      }
      userParticipation.setOption(userParticipationOption)
      
      // 转化漏斗图
      const conversion = echarts.init(conversionChart.value)
      const conversionOption = {
        title: { text: '' },
        tooltip: { trigger: 'item', formatter: '{a} <br/>{b} : {c}%' },
        legend: { data: ['展示', '点击', '加购', '下单', '支付'] },
        series: [
          {
            name: '转化率',
            type: 'funnel',
            left: '10%',
            top: 60,
            bottom: 60,
            width: '80%',
            min: 0,
            max: 100,
            minSize: '0%',
            maxSize: '100%',
            sort: 'descending',
            gap: 2,
            label: { show: true, position: 'inside' },
            labelLine: { length: 10, lineStyle: { width: 1, type: 'solid' } },
            itemStyle: { borderColor: '#fff', borderWidth: 1 },
            emphasis: { label: { fontSize: 20 } },
            data: [
              { value: 100, name: '展示' },
              { value: 45, name: '点击' },
              { value: 25, name: '加购' },
              { value: 18, name: '下单' },
              { value: 12, name: '支付' }
            ]
          }
        ]
      }
      conversion.setOption(conversionOption)
      
      // 窗口大小变化时自动调整图表大小
      window.addEventListener('resize', () => {
        salesTrend.resize()
        activityType.resize()
        userParticipation.resize()
        conversion.resize()
      })
    }
    
    // 获取数据
    const fetchData = () => {
      // 根据筛选条件获取数据
      console.log('获取数据:', {
        activityType: activityType.value,
        timeRange: timeRange.value,
        dateRange: dateRange.value
      })
    }
    
    // 重置筛选条件
    const resetFilter = () => {
      activityType.value = ''
      timeRange.value = 'last30'
      dateRange.value = []
      fetchData()
    }
    
    onMounted(() => {
      fetchData()
      // 延迟初始化图表，确保DOM已经渲染
      setTimeout(() => {
        initCharts()
      }, 100)
    })
    
    return {
      salesTrendChart,
      activityTypeChart,
      userParticipationChart,
      conversionChart,
      activityType,
      timeRange,
      dateRange,
      rankingMetric,
      activityTypeOptions,
      timeRangeOptions,
      overview,
      rankingData,
      formatNumber,
      fetchData,
      resetFilter
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

.filter-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.filter-item {
  margin-right: 10px;
}

.data-overview {
  margin: 20px 0;
}

.stat-card {
  background-color: #f5f7fa;
  border-radius: 4px;
  padding: 20px;
  text-align: center;
  height: 120px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-bottom: 20px;
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
  margin-bottom: 10px;
}

.stat-trend {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}

.stat-trend.up {
  color: #67C23A;
}

.stat-trend.down {
  color: #F56C6C;
}

.chart-container {
  margin: 20px 0;
}

.chart-card {
  background-color: #fff;
  border-radius: 4px;
  margin-bottom: 20px;
  padding: 15px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.chart-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #303133;
}

.chart {
  height: 350px;
}

.ranking-section {
  margin-top: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.section-title {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}
</style> 